from scraper.common import ScrapeResult, Scraper, ScraperFactory


class BolScrapeResult(ScrapeResult):
    def parse(self):
        alert_subject = 'Op voorraad'
        alert_content = ''

        # get name of product
        tag = self.soup.body.find('h1', class_='page-heading')
        if tag:
            alert_content += tag.text.strip() + '\n'
        else:
            self.logger.warning(f'missing title: {self.url}')

        # get listed price
        tag = self.soup.body.find('span', class_='promo-price')
        [s.extract() for s in tag('sup')]
        price_str = self.set_price(tag)
        if price_str:
            alert_subject = f'In Stock for €{price_str}'
        else:
            self.logger.warning(f'missing price: {self.url}')

        # check for add to cart button
        tag = self.soup.body.find('div', class_='buy-block__options js_basket_button_row js_multiple_basket_buttons_page')
        if tag:
            self.alert_subject = alert_subject
            self.alert_content = f'{alert_content.strip()}\n{self.url}'


@ScraperFactory.register
class BolScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'bol'

    @staticmethod
    def get_driver_type():
        return 'lean_and_mean'

    @staticmethod
    def get_result_type():
        return BolScrapeResult
