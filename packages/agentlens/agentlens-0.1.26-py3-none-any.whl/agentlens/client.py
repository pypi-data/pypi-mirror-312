from contextlib import contextmanager
from dataclasses import dataclass
from functools import wraps
from logging import getLogger
from pathlib import Path
from typing import (
    Any,
    Callable,
    Coroutine,
    Generator,
    ParamSpec,
    Type,
    TypeVar,
    cast,
    overload,
)

from agentlens.constants import RUNS_DIR
from agentlens.context import Run, Task
from agentlens.evaluation import Hook, HookGenerator, Mock, MockMiss, convert_to_kwargs
from agentlens.serialization import serialize_value, write_json

T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R", covariant=True)
F = TypeVar("F", bound=Callable[..., Any])


@contextmanager
def provide(
    *contexts: Any,
    hooks: list[Hook] = [],
    mocks: list[Mock] = [],
) -> Generator[None, None, None]:
    run = Run.current()
    if run is None:
        raise ValueError(
            "No active run context. Use @task decorator or _provide_run() to create one."
        )

    # Create context dictionary
    context_map = {type(context).__name__: context for context in contexts}

    # Check for existing contexts
    current = run.contexts.current
    if current:
        for key in context_map:
            if key in current:
                raise ValueError(f"Context {key} already provided")

    with run.contexts.push(context_map):
        # Create hook dictionary grouped by target
        hook_map: dict[str, list[Hook]] = {}
        for hook in hooks:
            target_name = hook.target.__name__
            if target_name not in hook_map:
                hook_map[target_name] = []
            hook_map[target_name].append(hook)

        # Create mock dictionary grouped by target
        mock_map: dict[str, Mock] = {}
        for mock in mocks:
            if mock.target_name in mock_map:
                raise ValueError(f"Multiple mocks provided for function {mock.target_name}")
            mock_map[mock.target_name] = mock

        with run.hooks.push(hook_map):
            with run.mocks.push(mock_map):
                yield


@contextmanager
def _provide_run(task_name: str) -> Generator[Run, None, None]:
    run = Run.current()
    if run is None:
        run = Run.start(RUNS_DIR, task_name)
        print(f"[agentlens] run directory: {run.dir}")
        yield run
        Run.end()
    else:
        yield run


@overload
def task(fn: F) -> F: ...


@overload
def task(
    *,
    name: str | None = None,
    capture_input: bool = True,
    capture_output: bool = True,
) -> Callable[[Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]]: ...


def task(
    fn: Callable[P, Coroutine[Any, Any, R]] | None = None,
    *,
    name: str | None = None,
    capture_input: bool = True,
    capture_output: bool = True,
) -> Callable[[Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]]:
    def decorator(
        fn: Callable[P, Coroutine[Any, Any, R]],
    ) -> Callable[P, Coroutine[Any, Any, R]]:
        if name:
            fn.__name__ = name

        @wraps(fn)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with _provide_run(fn.__name__) as run:
                with run.create_observation(fn.__name__) as observation:
                    # Convert args to kwargs
                    all_kwargs = convert_to_kwargs(fn, args, kwargs)

                    # Save input if requested
                    if capture_input:
                        input_data = {k: serialize_value(v) for k, v in all_kwargs.items()}
                        write_json(input_data, observation.dir / "input.json")

                    # Get hooks for this function
                    hooks = run.hooks.current.get(fn.__name__, []) if run.hooks.current else []

                    # run pre-hooks
                    generators: list[HookGenerator] = []
                    injected_kwargs: dict[str, Any] = {}
                    for hook in hooks:
                        gen = hook(args, kwargs)
                        if isinstance(gen, Generator):
                            generators.append(gen)  # type: ignore[arg-type]
                            new_injected_kwargs = next(gen)
                            injected_kwargs.update(new_injected_kwargs)

                    # rewrite task args/kwargs
                    all_kwargs = convert_to_kwargs(fn, args, kwargs)
                    all_kwargs.update(injected_kwargs)

                    # execute task
                    mock_fn = run.mocks.current.get(fn.__name__) if run.mocks.current else None
                    try:
                        if mock_fn is not None:
                            result = await mock_fn(**all_kwargs)
                        else:
                            raise MockMiss
                    except MockMiss:
                        result = await fn(**all_kwargs)

                    # Save output if requested
                    if capture_output:
                        output_data = {"result": serialize_value(result)}
                        write_json(output_data, observation.dir / "output.json")

                    cost = observation.cost
                    if cost.input > 0 or cost.output > 0:
                        (observation.dir / "cost.txt").write_text(str(cost))

                    # send result to generator hooks
                    for gen in generators:
                        try:
                            gen.send(result)
                        except StopIteration:
                            pass

                    return result

        return wrapper

    if fn is not None:
        return decorator(fn)  # type: ignore[return-value]
    else:
        return decorator


@dataclass
class Lens:
    _log = getLogger("agentlens")
    _runs_dir: Path = RUNS_DIR

    def __bool__(self) -> bool:
        return Run.current() is not None

    @property
    def run(self) -> Run:
        run = Run.current()
        if run is None:
            raise ValueError("No run context found")
        return run

    @property
    def task(self) -> Task:
        return Run.current_task()

    def __getitem__(self, context_type: Type[T]) -> T:
        key = context_type.__name__
        contexts = self.run.contexts.current
        if contexts is None:
            raise ValueError(
                f"No context value provided for type {context_type.__name__}. "
                "Use 'with lens.provide(value):' to provide one."
            )
        try:
            return cast(T, contexts[key])
        except KeyError:
            raise ValueError(
                f"No context value provided for type {context_type.__name__}. "
                "Use 'with lens.provide(value):' to provide one."
            )

    def __setitem__(self, context_type: Type[T], value: T) -> None:
        """Set a new value for an existing context."""
        key = context_type.__name__
        contexts = self.run.contexts.current
        if contexts is None:
            raise ValueError(
                f"No context value provided for type {context_type.__name__}. "
                "Use 'with lens.provide(value):' to provide one."
            )
        if key not in contexts:
            raise ValueError(
                f"No context value provided for type {context_type.__name__}. "
                "Use 'with lens.provide(value):' to provide one."
            )
        contexts[key] = value

    def increase_cost(self, *, input: float = 0.0, output: float = 0.0) -> None:
        """Increase cost for current observation and all parent observations"""
        run = self.run
        # Get all observations in the stack, from current to root
        for observation in run.observations.stack:
            observation.cost.input += input
            observation.cost.output += output


lens = Lens()
