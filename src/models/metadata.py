class Metadata:
    def __init__(self):
        self.opening_tag = "```\nmetadata\n"
        self.closing_tag = "```\n\n"
        self.metadata = []
        self.parent = {}

    def add_metadata_row(self, row):
        print(f'[add_metadata_row] Row {row} added...')
        self.metadata.append(row)

    def add_parent(self, parent: dict):
        print(
            f"[add_parent] Parent {parent['name']} "
            f"/ {parent['id']} added..."
        )
        self.parent = parent

    # def get_string(self) -> str:
    #     if self.metadata:
    #         data = self.opening_tag
    #         for item in self.metadata:
    #             data += f"  {item}\n"
    #         data += self.closing_tag
    #         if self.parent:
    #             data += (
    #                 f"**Родительская карточка**: [{self.parent['name']}]"
    #                 f"(https://planka.basis.services/cards/"
    #                 f"{self.parent['id']})\n\n"
    #             )
    #         return data
    #     else:
    #         return ""

    def get_string(self) -> str:
        if self.metadata:
            lines = [self.opening_tag]
            lines.extend(f"  {item}\n" for item in self.metadata)
            lines.append(self.closing_tag)
            if self.parent:
                lines.append(
                    f"**Родительская карточка**: [{self.parent['name']}]"
                    f"(https://planka.basis.services/cards/{self.parent['id']})\n"
                )
            return "\n".join(lines)
        return ""

