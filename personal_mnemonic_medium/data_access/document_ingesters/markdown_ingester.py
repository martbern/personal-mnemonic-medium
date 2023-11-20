from collections.abc import Callable, Sequence
from pathlib import Path

from tqdm import tqdm

from personal_mnemonic_medium.data_access.document_ingesters.base import (
    DocumentIngester,
)
from personal_mnemonic_medium.data_access.document_ingesters.document import (
    Document,
)
from personal_mnemonic_medium.data_access.document_ingesters.uuid_handling import (
    append_guid,
)


class MarkdownIngester(DocumentIngester):
    def __init__(
        self,
        uuid_extractor: Callable[[str], str],
        cut_note_after: str,
        uuid_generator: Callable[[], str] | None,
    ):
        """Create a new MarkdownNoteFactory.

        Args:
            uuid_extractor: A function that extracts a UUID string from a note's contents.
            cut_note_after: Cut everything in the note after this string.
            uuid_generator: A function that generates a UUID string. If specified and UUIDs are missing, the UUID will be appended to the note.
        """
        # TODO: https://github.com/MartinBernstorff/personal-mnemonic-medium/issues/247 Remove all state from the MarkdownIngester class
        self._cut_note_after = cut_note_after
        self._uuid_extractor = uuid_extractor
        self._uuid_generator = uuid_generator

    def _cut_contents(self, file_contents: str) -> str:
        return file_contents.split(self._cut_note_after)[0]

    def get_note_from_file(self, file_path: Path) -> Document:
        with file_path.open(encoding="utf8") as f:
            file_contents = f.read()

            try:
                uuid = self._uuid_extractor(file_contents)
            except IndexError as e:
                if self._uuid_generator is None:
                    raise ValueError(
                        f"Could not find UUID in {file_path}"
                    ) from e

                # TODO: https://github.com/MartinBernstorff/personal-mnemonic-medium/issues/248 Make GUID-appending part of the function signature
                uuid = append_guid(
                    file_path=file_path,
                    uuid_generator=self._uuid_generator,
                )
                file_contents += uuid

            if self._cut_note_after in file_contents:
                file_contents = self._cut_contents(file_contents)

            return Document(
                content=file_contents,
                uuid=uuid,
                source_path=file_path,
            )

    def get_notes_from_dir(
        self, dir_path: Path
    ) -> Sequence[Document]:
        notes: list[Document] = []
        md_files = list(dir_path.rglob("*.md"))

        with tqdm(total=len(md_files)) as pbar:
            for filepath in md_files:
                notes.append(self.get_note_from_file(filepath))
                pbar.update(1)

        return notes
