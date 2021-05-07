from scraper.common import ScrapeResult, Scraper, ScraperFactory


class EuevgaScrapeResult(ScrapeResult):
    def parse(self):
        alert_subject = 'Op voorraad'
        alert_content = ''

        # get name of product
        tag = self.soup.body.select_one('h1#product-name')
        if tag:
            alert_content += tag.text.strip() + '\n'
        else:
            self.logger.warning(f'missing title: {self.url}')

        # get listed price
        tag = self.soup.body.select_one('div.price-box > span#ctl00_LFrame_lblPrice')
        if not tag:
            tag = self.soup.body.select_one('div#price span#priceblock_ourprice')
        price_str = self.set_price(tag)
        if price_str:
            alert_subject = f'In Stock for {price_str}'

        # check for add to cart button
        tag = self.soup.body.select_one('div#ctl00_LFrame_pnlBuy')
        if tag:
            self.alert_subject = alert_subject
            self.alert_content = f'{alert_content.strip()}\n{self.url}'


@ScraperFactory.register
class EuevgaScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'euevga'

    @staticmethod
    def get_driver_type():
        return 'lean_and_mean'

    @staticmethod
    def get_result_type():
        return EuevgaScrapeResult
