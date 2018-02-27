from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from DouBanHouseInfo.items import DoubanhouseinfoItem


class DouBanHouseInfo(CrawlSpider):
    name = 'doubanhouseinfo'
    start_urls = ['https://www.douban.com/group/zhufang/discussion?start=1']

    # 小组渠道名称
    channel_name_list = ['zhufang', 'fangzi', 'sweethome', 'opking', 'beijingzufang', '26926']
    # todo 爬取页数
    crawl_page = 3
    # 基本格式 url
    base_url = "https://www.douban.com/group/{}/discussion?start={}"
    # 排重使用
    title_dict = {}

    # 构造小组url
    def build_urls(self, channel_names):
        urls = []
        for name in channel_names:
            for index in range(self.crawl_page):
                url = self.base_url.format(name, index * 25)
                urls.append(url)
        return urls

    def __init__(self):
        self.logger.info('init')
        self.start_urls = self.build_urls(self.channel_name_list)

    def parse(self, response):
        selector = Selector(response)
        divs = selector.xpath('//*[@id="content"]/div/div[1]/div[2]/table/tr')
        for div in divs:
            title_list = div.xpath('./td[1]/a/text()').extract()
            href_list = div.xpath('./td[1]/a/@href').extract()
            time_list = div.xpath('./td[4]/text()').extract()
            title = ''
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
                        pass
