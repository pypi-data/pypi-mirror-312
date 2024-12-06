from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field, is_dataclass
from functools import partial, wraps
from inspect import iscoroutinefunction, signature
from pathlib import Path
from sys import exc_info
from textwrap import indent
from traceback import FrameSummary, TracebackException
from typing import TYPE_CHECKING, Any, Generic, NoReturn, Self, TypeVar, cast, overload

from utilities.dataclasses import yield_field_names
from utilities.functions import ensure_not_none, get_class_name, get_func_name
from utilities.iterables import one
from utilities.rich import yield_pretty_repr_args_and_kwargs
from utilities.text import ensure_str

if TYPE_CHECKING:
    from collections.abc import Iterator
    from types import FrameType, TracebackType

    from utilities.typing import StrMapping

_F = TypeVar("_F", bound=Callable[..., Any])
_T = TypeVar("_T")
_Ignore = type[Exception] | tuple[type[Exception], ...]
_MAX_WIDTH = 80
_INDENT_SIZE = 4


@overload
def trace(func: _F, /, *, ignore: _Ignore | None = ...) -> _F: ...
@overload
def trace(
    func: None = None, /, *, ignore: _Ignore | None = ...
) -> Callable[[_F], _F]: ...
def trace(
    func: _F | None = None, /, *, ignore: _Ignore | None = None
) -> _F | Callable[[_F], _F]:
    """Trace a function call."""
    if func is None:
        result = partial(trace, ignore=ignore)
        return cast(Callable[[_F], _F], result)
    if not iscoroutinefunction(func):

        @wraps(func)
        def trace_sync(*args: Any, **kwargs: Any) -> Any:
            call_args = _CallArgs.create(func, *args, **kwargs)
            try:
                return func(*args, **kwargs)
            except Exception as error:  # noqa: BLE001
                _trace_build_and_raise_trace_mixin(
                    error, func, call_args, ignore=ignore
                )

        return cast(_F, trace_sync)

    @wraps(func)
    async def log_call_async(*args: Any, **kwargs: Any) -> Any:
        call_args = _CallArgs.create(func, *args, **kwargs)
        try:
            return await func(*args, **kwargs)
        except Exception as error:  # noqa: BLE001
            _trace_build_and_raise_trace_mixin(error, func, call_args, ignore=ignore)

    return cast(_F, log_call_async)


def _trace_build_and_raise_trace_mixin(
    error: Exception,
    func: Callable[..., Any],
    call_args: _CallArgs,
    /,
    *,
    ignore: _Ignore | None = None,
) -> NoReturn:
    """Build and raise a TraceMixin exception."""
    if (ignore is not None) and isinstance(error, ignore):
        raise error

    def extra(_: FrameSummary, frame: FrameType) -> _CallArgs | None:
        return frame.f_locals.get("call_args")

    frames = list(yield_extended_frame_summaries(error, extra=extra))
    matches = (
        f for f in frames if (f.name == get_func_name(func)) and (f.code_line != "")
    )
    frame = next(matches)
    trace_frame = _RawTraceMixinFrame(call_args=call_args, ext_frame_summary=frame)
    if isinstance(error, TraceMixin):
        raw_frames = [*error.raw_frames, trace_frame]
    else:
        raw_frames = [trace_frame]
    base = error
    while isinstance(base, TraceMixin):
        base = base.error
    native = type(base)
    new_cls = type(
        native.__name__,
        (native, TraceMixin),
        {"error": error, "raw_frames": raw_frames},
    )
    if is_dataclass(base):
        kwargs = {f: getattr(error, f) for f in yield_field_names(base)}
    else:
        kwargs = {}
    new_error = new_cls(*error.args, **kwargs)
    raise new_error from error


@dataclass(kw_only=True, slots=True)
class _CallArgs:
    """A collection of call arguments."""

    func: Callable[..., Any]
    args: tuple[Any, ...] = field(default_factory=tuple)
    kwargs: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(cls, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Self:
        """Make the initial trace data."""
        sig = signature(func)
        try:
            bound_args = sig.bind(*args, **kwargs)
        except TypeError as error:
            orig = ensure_str(one(error.args))
            lines: list[str] = [
                f"Unable to bind arguments for {get_func_name(func)!r}; {orig}"
            ]
            lines.extend(yield_pretty_repr_args_and_kwargs(*args, **kwargs))
            new = "\n".join(lines)
            raise _CallArgsError(new) from None
        return cls(func=func, args=bound_args.args, kwargs=bound_args.kwargs)


class _CallArgsError(TypeError):
    """Raised when a set of call arguments cannot be created."""


@dataclass(kw_only=True, slots=False)  # no slots
class TraceMixin:
    """Mix-in for tracking an exception and its call stack."""

    error: Exception
    raw_frames: list[_RawTraceMixinFrame[_CallArgs | None]] = field(
        default_factory=list
    )

    @property
    def frames(self) -> list[_TraceMixinFrame[_CallArgs | None]]:
        raw_frames = self.raw_frames
        return [
            _TraceMixinFrame[_CallArgs | None](
                depth=i, max_depth=len(raw_frames), raw_frame=frame
            )
            for i, frame in enumerate(raw_frames[::-1], start=1)
        ]

    def pretty(
        self,
        *,
        location: bool = True,
        max_width: int = _MAX_WIDTH,
        indent_size: int = _INDENT_SIZE,
        max_length: int | None = None,
        max_string: int | None = None,
        max_depth: int | None = None,
        expand_all: bool = False,
    ) -> str:
        """Pretty print the exception data."""
        return "\n".join(
            self._pretty_yield(
                location=location,
                max_width=max_width,
                indent_size=indent_size,
                max_length=max_length,
                max_string=max_string,
                max_depth=max_depth,
                expand_all=expand_all,
            )
        )

    def _pretty_yield(
        self,
        /,
        *,
        location: bool = True,
        max_width: int = _MAX_WIDTH,
        indent_size: int = _INDENT_SIZE,
        max_length: int | None = None,
        max_string: int | None = None,
        max_depth: int | None = None,
        expand_all: bool = False,
    ) -> Iterable[str]:
        """Yield the rows for pretty printing the exception."""
        from rich.pretty import pretty_repr

        indent = self._indent
        pretty = partial(
            pretty_repr,
            max_width=max_width,
            indent_size=indent_size,
            max_length=max_length,
            max_string=max_string,
            max_depth=max_depth,
            expand_all=expand_all,
        )

        yield "Error running:"
        yield ""
        for frame in self.frames:
            yield indent(f"{frame.depth}. {get_func_name(frame.func)}", 1)
        error = f">> {get_class_name(self.error)}: {self.error}"
        yield indent(error, 1)
        yield ""
        yield "Frames:"
        for frame in self.frames:
            yield ""
            name, filename = get_func_name(frame.func), frame.filename
            desc = f"{name} ({filename}:{frame.first_line_num})" if location else name
            yield indent(f"{frame.depth}/{frame.max_depth}. {desc}", 1)
            yield ""
            yield indent("Inputs:", 2)
            yield ""
            for line in yield_pretty_repr_args_and_kwargs(*frame.args, **frame.kwargs):
                yield indent(line, 3)
            yield ""
            yield indent("Locals:", 2)
            yield ""
            for k, v in frame.locals.items():
                yield indent(f"{k} = {pretty(v)}", 3)
            yield ""
            yield indent(f">> {frame.code_line}", 2)
            if location:  # pragma: no cover
                yield indent(f"   ({filename}:{frame.line_num})", 2)
            if frame.depth == frame.max_depth:
                yield indent(error, 2)

    def _indent(self, text: str, depth: int, /) -> str:
        """Indent the text."""
        return indent(text, 2 * depth * " ")


@dataclass(kw_only=True, slots=True)
class _RawTraceMixinFrame(Generic[_T]):
    """A collection of call arguments and an extended frame summary."""

    call_args: _CallArgs
    ext_frame_summary: _ExtFrameSummary[_T]


@dataclass(kw_only=True, slots=True)
class _TraceMixinFrame(Generic[_T]):
    """A collection of call arguments and an extended frame summary."""

    depth: int
    max_depth: int
    raw_frame: _RawTraceMixinFrame[_T]

    @property
    def func(self) -> Callable[..., Any]:
        return self.raw_frame.call_args.func

    @property
    def args(self) -> tuple[Any, ...]:
        return self.raw_frame.call_args.args

    @property
    def kwargs(self) -> dict[str, Any]:
        return self.raw_frame.call_args.kwargs

    @property
    def filename(self) -> Path:
        return self.raw_frame.ext_frame_summary.filename

    @property
    def module(self) -> str | None:
        return self.raw_frame.ext_frame_summary.module

    @property
    def name(self) -> str:
        return self.raw_frame.ext_frame_summary.name

    @property
    def qualname(self) -> str:
        return self.raw_frame.ext_frame_summary.qualname

    @property
    def code_line(self) -> str | None:
        return self.raw_frame.ext_frame_summary.code_line

    @property
    def first_line_num(self) -> int:
        return self.raw_frame.ext_frame_summary.first_line_num

    @property
    def line_num(self) -> int | None:
        return self.raw_frame.ext_frame_summary.line_num

    @property
    def end_line_num(self) -> int | None:
        return self.raw_frame.ext_frame_summary.end_line_num

    @property
    def col_num(self) -> int | None:
        return self.raw_frame.ext_frame_summary.col_num

    @property
    def end_col_num(self) -> int | None:
        return self.raw_frame.ext_frame_summary.end_col_num

    @property
    def locals(self) -> StrMapping:
        return self.raw_frame.ext_frame_summary.locals

    @property
    def extra(self) -> _T:
        return self.raw_frame.ext_frame_summary.extra


@dataclass(kw_only=True, slots=True)
class _ExtFrameSummary(Generic[_T]):
    """An extended frame summary."""

    filename: Path
    module: str | None = None
    name: str
    qualname: str
    code_line: str
    first_line_num: int
    line_num: int
    end_line_num: int
    col_num: int
    end_col_num: int
    locals: dict[str, Any] = field(default_factory=dict)
    extra: _T


@overload
def yield_extended_frame_summaries(
    error: Exception,
    /,
    *,
    traceback: TracebackType | None = None,
    extra: Callable[[FrameSummary, FrameType], _T],
) -> Iterator[_ExtFrameSummary[_T]]: ...
@overload
def yield_extended_frame_summaries(
    error: Exception, /, *, traceback: TracebackType | None = None, extra: None = None
) -> Iterator[_ExtFrameSummary[None]]: ...
def yield_extended_frame_summaries(
    error: Exception,
    /,
    *,
    traceback: TracebackType | None = None,
    extra: Callable[[FrameSummary, FrameType], _T] | None = None,
) -> Iterator[_ExtFrameSummary[Any]]:
    """Yield the extended frame summaries."""
    tb_exc = TracebackException.from_exception(error, capture_locals=True)
    if traceback is None:
        _, _, traceback_use = exc_info()
    else:
        traceback_use = traceback
    frames = yield_frames(traceback=traceback_use)
    for summary, frame in zip(tb_exc.stack, frames, strict=True):
        if extra is None:
            extra_use: _T | None = None
        else:
            extra_use: _T | None = extra(summary, frame)
        yield _ExtFrameSummary(
            filename=Path(summary.filename),
            module=frame.f_globals.get("__name__"),
            name=summary.name,
            qualname=frame.f_code.co_qualname,
            code_line=ensure_not_none(summary.line),
            first_line_num=frame.f_code.co_firstlineno,
            line_num=ensure_not_none(summary.lineno),
            end_line_num=ensure_not_none(summary.end_lineno),
            col_num=ensure_not_none(summary.colno),
            end_col_num=ensure_not_none(summary.end_colno),
            locals=frame.f_locals,
            extra=extra_use,
        )


def yield_frames(*, traceback: TracebackType | None = None) -> Iterator[FrameType]:
    """Yield the frames of a traceback."""
    while traceback is not None:
        yield traceback.tb_frame
        traceback = traceback.tb_next


__all__ = ["TraceMixin", "trace", "yield_extended_frame_summaries", "yield_frames"]
