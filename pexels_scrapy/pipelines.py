# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline


class PexelsScrapyPipeline(ImagesPipeline):

    def set_file_name(self, response):
        return '/full/{}.jpg'.format(response.meta['title'])

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'title': item['title']})

    def get_images(self, response, request, info):
        for key, image, buffer in super().get_images(response, request, info):
            key = self.set_file_name(response)
            yield key, image, buffer

