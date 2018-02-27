# -*- coding: utf-8 -*-

# Define your item pipelines here
# 保存数据到excel里面
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlwt


class DoubanhouseinfoPipeline(object):

    def validation_data(self, src_data):
        # todo 自定义关键字(满足条件的关键字数据将入文件保存)
        keyword_list = ['金台夕照', '团结湖', '呼家楼', '劲松', '潘家园', '大望路', '四惠']
        for keyword in keyword_list:
            if keyword in src_data:
                return True
        return False

    def open_spider(self, spider):
        self.index = 1
        self.book = xlwt.Workbook()
        self.sheet = self.book.add_sheet('sheet1')
        self.sheet.write(0, 0, 'title')
        self.sheet.write(0, 1, 'time')
        self.sheet.write(0, 2, 'link')
        pass

    def close_spider(self, spider):
        # todo 文件输出路径
        self.book.save('/Users/majichun/Desktop/reuslt_house.xls')
        pass

    def process_item(self, item, spider):
        title = item['title']
        # 清洗数据对合法数据进行输出保存
        if self.validation_data(title):
            self.sheet.write(self.index, 0, item['title'])
            self.sheet.write(self.index, 1, item['time'])
            self.sheet.write(self.index, 2, item['link'])
            self.index += 1
        return item
