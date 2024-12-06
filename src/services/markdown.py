'''
Кастомный конвертер для markdown, ориентированный
на форматирование текста сущностей из YouGile.
'''
from markdownify import MarkdownConverter


class CustomMarkdownConverter(MarkdownConverter):
    def convert_p(self, el, text, convert_as_inline):
        # Убираем лишние пробелы и добавляем перенос строки
        return text.strip() + '\n\n'

    def convert_br(self, el, text, convert_as_inline):
        # Обрабатываем теги <br> как переносы строки
        return '\n'

    def convert_a(self, el, text, convert_as_inline):
        # Обработка ссылок с учётом встроенных изображений
        href = el.get('href', '')
        if el.find('img'):
            img = el.find('img')
            img_src = img.get('src', '')
            return f'![{text or "image"}]({img_src})'
        return f'[{text}]({href})'

    def convert_code(self, el, text, convert_as_inline):
        # Кодовый блок обрабатывается корректно
        return f'```\n{text.strip()}\n```\n\n'

    def convert_pre(self, el, text, convert_as_inline):
        # Для тега <pre> вставляем как блок кода
        return f'```\n{text.strip()}\n```\n\n'

    def convert_img(self, el, text, convert_as_inline):
        # Обработка изображений
        src = el.get('src', '')
        alt = el.get('alt', 'image')
        return f'![{alt}]({src})'

    def convert_ul(self, el, text, convert_as_inline):
        # Обрабатываем списки с добавлением пустых строк для Markdown
        return f'\n{text.strip()}\n'

    def convert_li(self, el, text, convert_as_inline):
        # Каждый пункт списка начинается с '-'
        return f'- {text.strip()}\n'

    def convert_blockquote(self, el, text, convert_as_inline):
        # Обрабатываем цитаты
        return f'> {text.strip()}\n\n'


def html_to_markdown(html_input):
    md = CustomMarkdownConverter().convert(html_input)
    # Убираем лишние escape-символы
    md = (
        md.replace("\\.", ".")
          .replace("\\-", "-")
          .replace("\\#", "#")
          .replace("\n\n\n", "\n\n")  # Убираем лишние пустые строки
    )
    return md
