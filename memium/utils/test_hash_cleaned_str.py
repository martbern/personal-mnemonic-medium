import pytest

from .hash_cleaned_str import clean_str, hash_str_to_int


def hash_cleaned_str(input_str: str) -> int:
    return hash_str_to_int(clean_str(input_str))


def test_hash_cleaned_str_should_ignore_punctuation():
    strings_should_hash_to_identical = ["this", "This"]

    punctuation = r"!().,:;/"
    strings_should_hash_to_identical += [
        f"{s}{punctuation}" for s in strings_should_hash_to_identical
    ]

    assert (
        len(
            {
                hash_str_to_int(clean_str(s))
                for s in strings_should_hash_to_identical
            }
        )
        == 1
    )


@pytest.mark.parametrize(
    ("input_str", "hash_identical_str"), [("<p>Test</p>", "Test"), ("å", "å")]
)
def test_hash_cleaned_str_should_remove_html_tags(
    input_str: str, hash_identical_str: str
):
    assert hash_cleaned_str(input_str) == hash_cleaned_str(hash_identical_str)


@pytest.mark.parametrize(
    ("input_str", "expected"), [("Is <2, but >4", "is2but4")]
)
def test_str_cleaner(input_str: str, expected: str):
    assert clean_str(input_str) == clean_str(expected)
