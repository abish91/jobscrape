from scrapy.spiders import Spider
from jobscrape.items import JobscrapeItem
from jobscrape.tech_corpus import tech_corpus
from scrapy.http import Request
import html2text
import urllib
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import nltk


class MySpider(Spider):
    name            = "jobscrape"
    start_urls      = ["https://www.indeed.co.uk/Data-Scientist-jobs"]

    def parse(self, response):
        anchors = response.xpath('//a[contains(@class, "jobtitle turnstileLink")]')
        for anchors in anchors:
            title = anchors.xpath('@title').extract()
            link = anchors.xpath('@href').extract()[0]

            item = JobscrapeItem()
            item["title"] = title

            request = Request(response.urljoin(link), callback=self.parse_body)
            request.meta['item'] = item
            yield request

        next_page = response.xpath('//a//span[contains(text(), "Next")]/../../@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield Request(next_page, callback=self.parse)


    def parse_body(self, response):
        html = response.text

        # h = html2text.HTML2Text()
        # h.ignore_links = True
        # body = h.handle(html)
        body = html
        tokenizer = RegexpTokenizer(r'\w+')
        body = tokenizer.tokenize(body)
        words = set(w.title() for w in body if w.lower() in tech_corpus())

        item = response.meta['item']
        item["body"] = words
        item["link"] = response.url
        print(item)

        yield item
