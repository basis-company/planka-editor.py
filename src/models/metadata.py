class Metadata:
    def __init__(self):
        self.metadata = []
        self.parent = {}

    def add_metadata_row(self, row):
        # print(f'[add_metadata_row] Row {row} added...')
        self.metadata.append(row)

    def add_parent(self, parent: dict):
        self.parent = parent

    def get(self) -> str:
        lines = []
        if self.metadata:
            lines.append("```\nmetadata\n")
            lines.extend(f"  {item}\n" for item in self.metadata)
            lines.append("```\n\n")
        if self.parent:
            lines.append(
                f"**Родительская карточка**: [{self.parent['name']}]"
                f"(https://planka.basis.services/cards/"
                f"{self.parent['id']})\n\n---\n"
            )
        result = "".join(lines)
        return result
