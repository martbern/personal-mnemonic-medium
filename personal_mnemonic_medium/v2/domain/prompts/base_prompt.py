from collections.abc import Sequence
from typing import Protocol


class BasePrompt(Protocol):
    @property
    def uid(self) -> int:
        ...

    @property
    def tags(self) -> Sequence[str]:
        ...


from dataclasses import dataclass


@dataclass(frozen=True)
class RemotePrompt:
    prompt: BasePrompt
    remote_id: str
