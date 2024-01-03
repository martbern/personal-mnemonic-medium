from collections.abc import Sequence
from dataclasses import dataclass

from ...utils.hash_cleaned_str import clean_str, hash_str_to_int
from ..document import Document
from .prompt import BasePrompt


@dataclass(frozen=True)
class QAPrompt(BasePrompt):
    question: str
    answer: str

    @property
    def scheduling_uid_str(self) -> str:
        """Str used for generating the update_uid. Super helpful for debugging."""
        return clean_str(f"{self.question}_{self.answer}")

    @property
    def scheduling_uid(self) -> int:
        return hash_str_to_int(self.scheduling_uid_str)

    @property
    def update_uid_str(self) -> str:
        """Str used for generating the update_uid. Super helpful for debugging."""
        return f"{self.question}_{self.answer}_{self.tags}"

    @property
    def update_uid(self) -> int:
        return hash_str_to_int(self.update_uid_str)

    @property
    def tags(self) -> Sequence[str]:
        return ()


@dataclass(frozen=True)
class QAWithoutDoc(QAPrompt):
    add_tags: Sequence[str]

    @property
    def tags(self) -> Sequence[str]:
        return self.add_tags


@dataclass(frozen=True)
class QAFromDoc(QAPrompt):
    parent_doc: Document
    line_nr: int

    @property
    def tags(self) -> Sequence[str]:
        return self.parent_doc.tags
