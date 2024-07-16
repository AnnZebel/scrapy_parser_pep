# scrapy_parser_pep

## Описание
Асинхронный парсер для сайта python.org
Парсер выводит собранную информацию в два файла .csv:
1. первый файл — список всех PEP: номер, название и статус.
2. второй файл — сводку по статусам PEP, сколько найдено документов в каждом статусе (статус, количество).

## Пример работы парсера
- **PepSpider** (файл  pep_parse/spiders/pep.py ): 
  - Парсит главную страницу PEP и собирает ссылки на отдельные PEP. 
  - Переходит по каждой ссылке и собирает информацию о номере, названии и статусе PEP.
 
    ```
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

### Перед использованием
Клонируйте репозиторий к себе на компьютер 
```
git clone git@github.com:AnnZebel/scrapy_parser_pep.git
```
В корневой папке нужно создать и активировать виртуальное окружение и установить зависимости.
```
python -m venv venv
```
```
source venv/bin/activate
```
```
pip install -r requirements.txt
```
### Запуск программы
```
scrapy crawl pep
```

## Автор
Анна Зыбель
