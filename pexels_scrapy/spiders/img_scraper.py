# -*- coding: utf-8 -*-
import scrapy

from pexels_scrapy.items import PexelsScrapyItem


class ImgScraperSpider(scrapy.Spider):
    name = 'img_scraper'
    rotate_user_agent = True
    allowed_domains = ['pexels.com']
    start_urls = ['http://pexels.com/']

    def parse(self, response):
        urls = response.xpath('//div[contains(@class, "photos")]//article[contains(@class, "photo-item photo-item--overlay")]/a[contains(@class, "js-photo-link")]//@href').extract()

        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_image)

        next_page_url = response.xpath('//div[contains(@class, "pagination")]/a[contains(@rel, "next")]//@href').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            print('LOOK HERE {}'.format(next_page_url))
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_image(self, response):
        item = PexelsScrapyItem()
        # item['image_urls'] = response.css('picture.image-section__picture > image.image-section__image js-photo-zoom::attr(src)').extract_first()
        item['title'] = response.xpath('//img[contains(@class, "image-section__image js-photo-zoom")]//@alt').extract_first()
        item['image_urls'] = response.xpath('//img[contains(@class, "image-section__image js-photo-zoom")]//@src').extract()
        # item['try_it'] = response.xpath('//img[contains(@class, "image-section__image js-photo-zoom")]//@src').extract()
        print(item['image_urls'])
        yield item
