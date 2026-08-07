from langchain_text_splitters import RecursiveCharacterTextSplitter, Language


text = """

class CharacterTextSplitter(TextSplitter):
    ""Splitting text that looks at characters.""

    def __init__(
        self,
        separator: str = "\n\n",
        is_separator_regex: bool = False,  # noqa: FBT001,FBT002
        **kwargs: Any,
    ) -> None:
        # Create a new TextSplitter.
        super().__init__(**kwargs)
        self._separator = separator
        self._is_separator_regex = is_separator_regex

    def split_text(self, text: str) -> list[str]:
        ""Split into chunks without re-inserting lookaround separators.""
        # 1. Determine split pattern: raw regex or escaped literal
        sep_pattern = (
            self._separator if self._is_separator_regex else re.escape(self._separator)
        )

        # 2. Initial split (keep separator if requested)
        splits = _split_text_with_regex(
            text, sep_pattern, keep_separator=self._keep_separator
        )
"""


splitter = RecursiveCharacterTextSplitter.from_language(
    
    language=Language.PYTHON,
    chunk_size=400,
    chunk_overlap=0,
)

chunks = splitter.split_text(text=text)

print(chunks[1])
print(len(chunks))