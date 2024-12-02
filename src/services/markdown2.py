from bs4 import BeautifulSoup


def html_to_markdown(html_input):
    """
    Кастомный конвертер для markdown, ориентированный под форматирование из
    YouGile. Работает с конкретным пулом тегов, которые есть в текущих данных.
    Теги не входящие в этот пул игнорируются.
    """
    tag_handlers = {
        "p": lambda el: "".join(parse_element(child) for child in el.contents) + "\n\n",
        "br": lambda el: "  \n",
        "a": lambda el: f"[{el.get_text(strip=True) or 'ссылка'}]({el.get('href', '#')})",
        "strong": lambda el: f"**{el.get_text(strip=True)}** ",
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
        "div": lambda el: "".join(parse_element(child) for child in el.contents),
        "span": lambda el: "".join(parse_element(child) for child in el.contents),
    }

    def parse_element(element):
        if element.name in tag_handlers:  # html-tags found
            result = tag_handlers[element.name](element)
            return result if result is not None else ""
        elif isinstance(element, str):  # simple text
            return element.strip() + " "
        return ""  # return empty string when element doesn't have any value

    soup = BeautifulSoup(html_input, "html.parser")
    return "".join(parse_element(el) for el in soup.contents)
