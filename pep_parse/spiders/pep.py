import scrapy
from scrapy import Selector

from constans import PATTERN
from pep_parse.items import PepParseItem
from scrapy.utils.project import get_project_settings


class PepSpider(scrapy.Spider):
    name = 'pep'
    start_urls = ['https://peps.python.org/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = get_project_settings()
        self.allowed_domains = settings.get('ALLOWED_DOMAINS')

    def parse(self, response):
        peps_table: Selector = response.css(
            "section[id='numerical-index']"
        ).css('tbody')[0]
        links: list[str] = peps_table.css("a::attr(href)").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        pep_info: Selector = response.css("section[id='pep-content']")
        title = PATTERN.search(pep_info.css("h1::text").get())
        status: str = pep_info.css("dt:contains('Status') + dd::text").get()
        if title:
            number, name = title.group('number', 'name')
            context = {
                'number': number,
                'name': name,
                'status': status
            }
            yield PepParseItem(context)
