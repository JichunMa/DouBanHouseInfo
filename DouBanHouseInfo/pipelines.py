# -*- coding: utf-8 -*-

# Define your item pipelines here
# 保存数据到excel里面
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlwt


class DoubanhouseinfoPipeline(object):

    def open_spider(self, spider):
        self.index = 1
        self.book = xlwt.Workbook()
        self.sheet = self.book.add_sheet('sheet1')
        self.sheet.write(0, 0, 'title')
        self.sheet.write(0, 1, 'time')
        self.sheet.write(0, 2, 'link')
        pass

    def close_spider(self, spider):
        self.book.save('reuslt_house.xls')
        pass

    def process_item(self, item, spider):
        self.sheet.write(self.index, 0, item['title'])
        self.sheet.write(self.index, 1, item['time'])
        self.sheet.write(self.index, 2, item['link'])
        self.index += 1
        return item
