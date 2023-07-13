import re
import html
from uuid import uuid4

import html2text
from bs4 import BeautifulSoup as Soup

__all__ = ['parse_html_tag', 'remove_tags', 'parse_html_from_text',
           'remove_extra_line', 'remove_starting_and_ending_line', 'parse_html']


def parse_html_tag(parse_string):
    """ Parse HTML tag """

    parse_string = parse_string.replace('<br>', "\n")

    html = Soup(parse_string, 'html.parser')
    replace_list = []
    href_list = []
    for a in html.find_all('a'):
        replace_list.append(a.text + ": " + a['href'])
        href_list.append(str(a))
    for href, repl in zip(href_list, replace_list):
        parse_string = parse_string.replace(href, repl)
    return parse_string


def remove_tags(parse_string):
    """ Remove HTML tags """

    parse_string = parse_html_tag(parse_string)
    escape_string = re.compile(r'<[^>]+>').sub('', parse_string)
    return html.unescape(escape_string)


def parse_html_from_text(response_text):
    """ Parse HTML tags from the given text """

    response_text = remove_extra_line(response_text)
    h = html2text.HTML2Text()
    h.ignore_emphasis = False
    h.ul_item_mark = "-"
    h.strong_mark = "*"
    h.body_width = 0

    # generate the unique id
    unique_id = uuid4().hex.__str__()

    # Replace the semicolon with unique id if string contain semicolon
    replaced_str = response_text.replace(";", unique_id)
    new_html = h.handle(replaced_str)
    # Remove semicolon
    remove_semicolon = new_html.replace(";", "")

    # Replace the unique id with semicolon
    new_html = remove_semicolon.replace(unique_id, ";")
    new_html = new_html.replace("\n\n", "\n")
    new_html = new_html.replace("#new_line#\n", "\n")
    new_html = new_html.replace("#new_line#", "\n")
    new_html = new_html.replace("#newline#", "\n")
    new_html = new_html.replace("#newline#\n", "\n")
    new_html = new_html.replace("_*", "*")
    new_html = new_html.replace("*_", "*")
    new_html = new_html.replace("*_", "_")
    new_html = new_html.replace("_*", "_")
    new_html = new_html.replace("_ *", "*")
    new_html = new_html.replace(" _ *", "*")
    new_html = new_html.replace("  \n*\n", "*\n")
    new_html = new_html.replace("  \n_", "_\n")
    new_html = new_html.replace("\.", ".")
    image_list = []
    # if only image is there
    if new_html.startswith("![]") or new_html.startswith("[![]"):
        str_html = new_html.replace("\n", "")
        if str_html.endswith(")"):
            soup = Soup(response_text)
            images = soup.findAll('img')
            for img in images:
                image_list.append(img['src'])
            return image_list
    if "![]" in new_html:
        new_html = new_html.replace("![]", "")
        new_html = new_html.replace("-\n", "-")
        new_html = new_html.replace("(", "")
        new_html = new_html.replace(")", "")
    else:
        chars = new_html.split("\n")
        new_line = ""
        for item in chars:
            new_line = "{new_line}\n{item}".format(new_line=new_line, item=item.strip())
        new_html = new_line

    new_html = new_html.replace("<", "")
    new_html = new_html.replace(">", "")
    if new_html == "\n\n":
        return ''
    return new_html


def remove_extra_line(text):
    """ Remove Extras lines from the text """

    text = text.replace("\n<p><br></p>\n", "#new_line#")
    text = text.replace("<p><br></p>\n", "#new_line#")
    text = text.replace("<p><br></p>", "#new_line#")
    text = text.replace("</ul>\n", "</ul>")
    text = text.replace("</ol>\n", "</ol>")
    text = text.replace("<br>\n</li>", "</li>")
    return text


def remove_starting_and_ending_line(string):
    """ Remove starting and ending line """

    if string and isinstance(string, str):
        if string.startswith('\n'):
            string = string[1:]
        if string.endswith('\n'):
            string = string[:-1]
    return string


def parse_html(text):
    """ This method is used to parse the HTML

    Steps:
        - Parsing the HTML text from the text using `parse_html_from_text`
        - Remove HTML Tags using `remove_tags`
        - Remove Starting and ending lines `remove_starting_and_ending_line`
    """

    return remove_starting_and_ending_line(remove_tags(parse_html_from_text(text)))
