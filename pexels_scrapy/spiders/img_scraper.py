# -*- coding: utf-8 -*-
import scrapy

from pexels_scrapy.items import PexelsScrapyItem


class ImgScraperSpider(scrapy.Spider):
    name = 'img_scraper'
    allowed_domains = ['pexels.com']
    start_urls = ['http://pexels.com/']

    def parse(self, response):
        urls = response.css('div.photos > article.photo-item photo-item--overlay > a::attr(href)').extract()
        urls = response.xpath('//div[contains(@class, "photos")]//article[contains(@class, "photo-item photo-item--overlay")]/a[contains(@class, "js-photo-link")]//@href').extract()

        print(urls)
        for url in urls:
            url = response.urljoin(url)
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_image)

    def parse_image(self, response):
        item = PexelsScrapyItem()
        # item['image_urls'] = response.css('picture.image-section__picture > image.image-section__image js-photo-zoom::attr(src)').extract_first()
        item['title'] = response.xpath('//img[contains(@class, "image-section__thumb")]//@alt').extract_first()
        item['image_urls'] = response.xpath('//img[contains(@class, "image-section__image js-photo-zoom")]//@src').extract()
        # item['try_it'] = response.xpath('//img[contains(@class, "image-section__image js-photo-zoom")]//@src').extract()
        print(item['image_urls'])
        yield item
