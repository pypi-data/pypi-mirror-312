from typing import Any, Callable

class InteractsWithEvents:
    @classmethod
    def booted(cls, callback: Callable[[Any], Any]): ...
    @classmethod
    def serving(cls, callback: Callable[[Any], Any]): ...
