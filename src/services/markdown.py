'''
Кастомный конвертер для markdown, ориентированный
на форматирование текста сущностей из YouGile.
'''
from markdownify import MarkdownConverter


class CustomMarkdownConverter(MarkdownConverter):
    def convert_p(self, el, text, convert_as_inline):
        # убираем лишние пробелы и добавляем перенос строки
        return text.strip() + '\n\n'

    def convert_br(self, el, text, convert_as_inline):
        # обрабатываем теги <br> как переносы строки
        return '\n'

    def convert_a(self, el, text, convert_as_inline):
        # обработка ссылок с учётом встроенных изображений
        href = el.get('href', '')
        if el.find('img'):
            img = el.find('img')
            img_src = img.get('src', '')
            return f'![{text or "image"}]({img_src})'
        return f'[{text}]({href})'

    def convert_code(self, el, text, convert_as_inline):
        # кодовый блок обрабатывается корректно
        return f'```\n{text.strip()}\n```\n\n'

    def convert_pre(self, el, text, convert_as_inline):
        # для тега <pre> вставляем как блок кода
        return f'```\n{text.strip()}\n```\n\n'

    def convert_img(self, el, text, convert_as_inline):
        # Обработка изображений
        src = el.get('src', '')
        alt = el.get('alt', 'image')
        return f'![{alt}]({src})'

    def convert_ul(self, el, text, convert_as_inline):
        # обрабатываем списки с добавлением пустых строк для Markdown
        return f'\n{text.strip()}\n'

    def convert_li(self, el, text, convert_as_inline):
        # каждый пункт списка начинается с '-'
        return f'- {text.strip()}\n'

    def convert_blockquote(self, el, text, convert_as_inline):
        # обрабатываем цитаты
        return f'> {text.strip()}\n\n'


def html_to_markdown(html_input):
    md = CustomMarkdownConverter().convert(html_input)
    # убираем лишние escape-символы
    md = (
        md.replace("\\.", ".")
          .replace("\\-", "-")
          .replace("\\#", "#")
          .replace("\n\n\n", "\n\n")  # убираем лишние пустые строки
    )
    return md
