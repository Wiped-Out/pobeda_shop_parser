import requests
from bs4 import BeautifulSoup
from models import Good
from exceptions import CantGetPage


class PobedaParser:
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }

    def _get_page(self, url: str) -> str:
        try:
            response = requests.get(url=url, headers=self.headers)
        except Exception as e:
            raise CantGetPage(e)
        return response.text

    def get_goods(self, url: str) -> list[Good]:
        page_text = self._get_page(url=url)
        soup = BeautifulSoup(page_text, "lxml")

        goods = []
        for item in soup.find_all("div", class_="card"):
            title = item.find("a", class_="card-title").text.strip()
            url = item.find("a", class_="card-title")["href"]
            barcode = int(item.find("div", class_="card-wrapper")["data-barcode"])
            price = self.clear_price(price=item.find("div", class_="card-price").text)
            goods.append(Good(title=title, price=price, barcode=barcode, url=url))
        return goods

    @staticmethod
    def clear_price(price: str) -> int:
        new_price = ""
        for symbol in price:
            if symbol.isnumeric():
                new_price += symbol

        return int(new_price)
