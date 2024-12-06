from contextlib import suppress
from typing import Iterable, Iterator, NamedTuple, Optional, Tuple

class ButtonEvent(NamedTuple):
    button: str
    pressed: bool
    seconds_since_last_event: float
    coordinates: Optional[Tuple[int, int]]

class ButtonEventInput(Iterable[ButtonEvent]):
    def __iter__(self) -> Iterator[ButtonEvent]:
        with suppress(EOFError):
            while event := input():
                yield ButtonEvent(*eval(event))
