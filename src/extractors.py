from os import PathLike
from ebooklib import epub
from PIL import Image
from io import BytesIO

import bs4
import ebooklib


class EpubExtractor:
  HTML_STRIP_TAGS = ['style', 'script', 'code', 'link', 'title']
  HTML_NEWLINE_TAGS = ['p', 'br', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']

  def __init__(self, src: str | PathLike):
    self.__src = src
    self.__book = epub.read_epub(self.__src)

  def get_book_title(self) -> str:
    return self.__book.get_metadata('DC', 'title')[0][0]

  def get_book_cover(self) -> Image.Image | None:
    if len(covers := list(self.__book.get_items_of_type(ebooklib.ITEM_COVER))):
      image_bytes = covers[0].content
      return Image.open(BytesIO(image_bytes))

  def extract(self, dst: str | PathLike):

    for i, doc in enumerate(self.__book.get_items_of_type(ebooklib.ITEM_DOCUMENT)):
      text = self.__html_to_text(doc.content)

      if not text:
        continue

      with open(f"{dst}/{i}.txt", "w") as file:
        file.write(text)

  def __html_to_text(self, html: str):
    soup = bs4.BeautifulSoup(html, 'html.parser')

    for el in self.HTML_STRIP_TAGS:
      if (tag := soup.find(el)) is not None:
        tag.extract()

    for tag in soup.find_all(self.HTML_NEWLINE_TAGS):
      if tag.name == "p":
        new_p = soup.new_tag("p")
        new_p.string = tag.get_text().replace("\n", " ")
        tag.replace_with(new_p)
      tag.append('\n')
      text = soup.get_text()
      text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())

    return text
