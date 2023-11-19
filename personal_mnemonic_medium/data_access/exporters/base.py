from abc import ABC, abstractmethod
from collections.abc import Sequence

from personal_mnemonic_medium.data_access.exporters.anki.card_types.base import (
    AnkiCard,
)
from personal_mnemonic_medium.domain.prompt_extractors.prompt import (
    Prompt,
)


class CardExporter(ABC):
    @abstractmethod
    def prompts_to_cards(
        self, prompts: Sequence[Prompt]
    ) -> list[AnkiCard]:
        pass
