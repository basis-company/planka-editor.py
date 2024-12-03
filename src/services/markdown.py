'''
Кастомный конвертер для markdown, ориентированный
на форматирования текста сущностей из YouGile.
'''
from markdownify import MarkdownConverter


class CustomMarkdownConverter(MarkdownConverter):
    def convert_p(self, el, text, convert_as_inline):
        return text.strip() + '\n\n'

    def convert_br(self, el, text, convert_as_inline):
        return '\n'

    def convert_a(self, el, text, convert_as_inline):
        href = el.get('href', '')
        return f'[{text}]({href})'


def html_to_markdown(html_input):
    md = CustomMarkdownConverter().convert(html_input)
    md = md.replace("\\.", ".").replace("\\-", "-").replace("\\#", "#")
    return md
