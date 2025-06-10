from dataclasses import dataclass
import httpx


@dataclass
class WBDataParser:
    """
    Класс для парсинга данных со страницы Wildberries
    """
    url_to_parse: str

    async def get_id_from_url(self) -> str:
        """
        Получаем ID товара из URL
        :return: product_id: str
        """
        product_id = self.url_to_parse.split("https://www.wildberries.ru/catalog/")[1].split("/")[0]
        return product_id

    async def get_json_from_wb(self) -> dict:
        """
        Метод получения респонса со страницы товара.
        :return: data: dict
        """
        product_id = await self.get_id_from_url()
        api_url = "https://card.wb.ru/cards/v2/" \
                  "detail?appType=1&curr=rub&dest=-1255987" \
                  f"&spp=30&hide_dtype=13&ab_testing=false&lang=ru&nm={product_id}"
        headers = {
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://www.wildberries.ru',
            'priority': 'u=1, i',
            'referer': 'https://www.wildberries.ru/catalog/274580840/detail.aspx',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'x-captcha-id': 'Catalog 1|1|1749566654|AA==|fa9edfaf21554ff19b89fd375910b246|AC9qemwx1Sz1I0q5lAGtVzYqvzR1b85FvqWve59Lxyz',
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data

    async def make_data_dict(self) -> dict:
        """
        Метод для формирования словаря с нужными нам данными. (Имя, цена)
        :return: result_dict: dict
        """
        result_dict = {}
        json_data = await self.get_json_from_wb()
        data = json_data.get("data")
        products = data.get("products", None)[0]
        if products:
            result_dict["title"] = products.get("name", None)
        sizes = products.get("sizes", None)[0]
        if sizes:
            price = sizes.get("price", None)
            if price:
                result_dict["price"] = price.get("total") / 100
        return result_dict
