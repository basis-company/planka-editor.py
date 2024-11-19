'''
Кастомный конвертер для markdown, ориентированный под форматирование из
YouGile. Работает с конкретным пулом тегов, которые есть в текущих данных.
Теги не входящие в этот пул игнорируются.
'''
from bs4 import BeautifulSoup


def html_to_markdown(html_input):
    # TODO: Does't tested yet, need to review
    # html tags settings
    tag_handlers = {
        "p": lambda el: f"{el.get_text(strip=True)}\n\n",
        "br": lambda el: "  \n",
        "a": lambda el: f"[{el.get_text(strip=True)}]({el.get('href', '#')})",
        "strong": lambda el: f"**{el.get_text(strip=True)}**",
        "b": lambda el: f"**{el.get_text(strip=True)}**",
        "em": lambda el: f"*{el.get_text(strip=True)}*",
        "i": lambda el: f"*{el.get_text(strip=True)}*",
        "code": lambda el: f"`{el.get_text(strip=True)}`",
        "ul": lambda el: (
            "\n".join(
                f"- {li.get_text(strip=True)}" 
                for li in el.find_all("li")
            ) + "\n"
        ),
        "ol": lambda el: (
            "\n".join(
                f"1. {li.get_text(strip=True)}" 
                for li in el.find_all("li")
            ) + "\n"
        ),
        "img": lambda el: f"![{el.get('alt', 'image')}]({el.get('src', '')})",
        "hr": lambda el: "\n---\n",
        "blockquote": lambda el: f"> {el.get_text(strip=True)}\n",
        "h1": lambda el: f"# {el.get_text(strip=True)}\n\n",
        "h2": lambda el: f"## {el.get_text(strip=True)}\n\n",
        "h4": lambda el: f"### {el.get_text(strip=True)}\n\n",
        "div": lambda el: el.get_text(strip=True),
        "span": lambda el: el.get_text(strip=True),
    }

    def parse_element(element):
        if element.name in tag_handlers:  # html
            return tag_handlers[element.name](element)
        else:  # text
            return element if isinstance(element, str) else element.get_text(strip=True)

    soup = BeautifulSoup(html_input, "html.parser")
    return "".join(parse_element(el) for el in soup.contents)

