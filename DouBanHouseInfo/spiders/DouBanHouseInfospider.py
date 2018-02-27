from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from DouBanHouseInfo.items import DoubanhouseinfoItem


class douban_house_info(CrawlSpider):
    name = 'doubanhouseinfo'
    start_urls = ['https://www.douban.com/group/zhufang/discussion?start=1']
    title_dict = {}

    def parse(self, response):
        selector = Selector(response)
        divs = selector.xpath('//*[@id="content"]/div/div[1]/div[2]/table/tr')
        for div in divs:
            title_list = div.xpath('./td[1]/a/text()').extract()
            href_list = div.xpath('./td[1]/a/@href').extract()
            time_list = div.xpath('./td[4]/text()').extract()
            title = ''
            href = ''
            get_time = ''
            if len(title_list) > 0:
                title = title_list[0].replace('\n', "").replace(' ', '')
            if len(time_list) > 0:
                get_time = time_list[0]
            if len(href_list) > 0:
                href = href_list[0]
                if title != "" and href != "":
                    # 去重
                    if title not in self.title_dict.keys():
                        self.title_dict[title] = '1'
                        item = DoubanhouseinfoItem()
                        item['title'] = title
                        item['link'] = href
                        item['time'] = get_time
                        yield item
                    else:
                        print(title)
