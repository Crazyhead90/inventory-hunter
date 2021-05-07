from scraper.common import ScrapeResult, Scraper, ScraperFactory


class CoolblueScrapeResult(ScrapeResult):
    def parse(self):
        alert_subject = 'Op voorraad'
        alert_content = ''

        # get name of product
        tag = self.soup.body.find('h1', class_='js-product-name')
        if tag:
            alert_content += tag.text.strip() + '\n'
        else:
            self.logger.warning(f'missing title: {self.url}')

        # get listed price
        tag = self.soup.body.find('span', class_='sales-price js-sales-price')
        [s.extract() for s in tag('sup')]
        price_str = self.set_price(tag)
        if price_str:
            alert_subject = f'In Stock for €{price_str}'
        else:
            self.logger.warning(f'missing price: {self.url}')

        # check for add to cart button
        tag = self.soup.body.find('div', class_='section--5@md')
        if tag:
            self.alert_subject = alert_subject
            self.alert_content = f'{alert_content.strip()}\n{self.url}'


@ScraperFactory.register
class CoolblueScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'coolblue'

    @staticmethod
    def get_driver_type():
        return 'lean_and_mean'

    @staticmethod
    def get_result_type():
        return CoolblueScrapeResult
