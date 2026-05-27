from config import link_end


class product:
    def __init__(self, item) -> None:
        name_container = item.find("div", {'data-cy': 'title-recipe'})
        if not name_container or not name_container.find('span'):
            return
        self.name = name_container.find('span').text[:25]

        rating_container = item.find("i", {'data-cy': 'reviews-ratings-slot'})
        if not rating_container or not rating_container.find("span"):
            return
        self.rating = rating_container.find("span").text[:3]  # ratings are at most 3 chars ("4.5")

        asin = item.get('data-asin')
        if not asin:
            return
        self.link = f'https://www.amazon.{link_end}/dp/{asin}'

        price_container = item.find("div", {'data-cy': 'price-recipe'})
        if not price_container or len(price_container.find_all("span")) < 2:
            return
        price_span = price_container.find("span", {'class': 'a-offscreen'})
        if not price_span:
            return
        self.price = price_span.text

        self.listable = True


def list_products(products) -> None:
    for i, item in enumerate(products, start=1):
        print(f"{i}. Name: {item.name} \nPrice: {item.price} \nRating: {item.rating}/5 \nLink: {item.link} \n ")
