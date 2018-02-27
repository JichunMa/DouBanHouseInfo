from scrapy import cmdline

# 作为启动器
if __name__ == '__main__':
    cmdline.execute("scrapy crawl doubanhouseinfo".split())
