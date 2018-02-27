import requests
import time
from lxml import etree
import os
import zipfile

# 北京无中介租房（寻天使投资）
db_angel_start_url = "https://www.douban.com/group/zhufang/discussion?start={}"
# 豆瓣租房小组
db_all_start_url = "https://www.douban.com/group/fangzi/discussion?start={}"
# 北京租房（密探）
db_spy_start_url = "https://www.douban.com/group/sweethome/discussion?start={}"
# 北京个人租房 （真房源|无中介）
db_person_start_url = "https://www.douban.com/group/opking/discussion?start={}"
# 北京租房
db_bj_start_url = "https://www.douban.com/group/beijingzufang/discussion?start={}"
# 北京租房豆瓣
db_bj_db_start_url = "https://www.douban.com/group/26926/discussion?start={}"

url_list = [db_angel_start_url, db_all_start_url, db_spy_start_url, db_person_start_url, db_bj_start_url,
            db_bj_db_start_url]
save_origin_path_list = ['angle/', 'all/', 'spy/', 'person/', 'bj/', 'bj_db/']

savePath = '/Users/majichun/Desktop/houseInfo/{}_{}.csv'
keyword = ['金台夕照', '团结湖', '呼家楼', '劲松', '潘家园', '大望路', '四惠']
zip_Path = '/Users/majichun/Desktop/abc.txt.zip'
# 是否打包
is_package = False
# 是否写入文档
is_write_doc = False
# 爬取页数
page_number = 3
# list
my_list = []
# title_dict 保证title唯一
title_dict = dict()


class Complex:
    def __init__(self, my_title, my_time, my_href):
        self.my_title = my_title
        self.my_time = my_time
        self.my_href = my_href


# 打包目录为zip文件（未压缩）
def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirNames, filenames in os.walk(source_dir):
        for filename_item in filenames:
            pathfile = os.path.join(parent, filename_item)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()


for index in range(len(url_list)):
    origin_url = url_list[index]
    # 获取数据
    for i in range(page_number):
        url = origin_url.format(i * 25)
        print(url)
        data = requests.get(url).text
        time.sleep(1)
        data.encode('utf-8')
        if '检测到有异常请求从你的 IP 发出' in data:
            raise Exception('被封了0.0')
        files = etree.HTML(data)
        path = files.xpath('//*[@id="content"]/div/div[1]/div[2]/table/tr')

        for div in path:
            title_list = div.xpath('./td[1]/a/text()')
            href_list = div.xpath('./td[1]/a/@href')
            time_list = div.xpath('./td[4]/text()')
            title = ''
            href = ''
            get_time = ''
            if len(title_list) > 0:
                title = title_list[0].replace('\n', "")
            if len(time_list) > 0:
                get_time = time_list[0]
            if len(href_list) > 0:
                href = href_list[0]
                if title != "" and href != "":
                    if title not in title_dict.keys():
                        # 去重
                        title_dict[title] = '1'
                        my_complex = Complex(title, get_time, href)
                        my_list.append(my_complex)
                    else:
                        print(title)
# 输出结果
for k in range(len(keyword)):
    # 写入文档或打印输出
    if is_write_doc:
        filename = savePath.format(keyword[k], time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()))
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('title\ttime\turl\n')
            for j in range(len(my_list)):
                if keyword[k] in my_list[j].my_title:
                    f.write('{}\t{}\t{}\n'.format(my_list[j].my_title, my_list[j].my_time, my_list[j].my_href))
    else:
        for j in range(len(my_list)):
            if keyword[k] in my_list[j].my_title:
                print('{},{},{}\n'.format(my_list[j].my_title, my_list[j].my_time, my_list[j].my_href))
# 打包
if is_package:
    make_zip('/Users/majichun/Desktop/houseInfo/', zip_Path)
else:
    print("不打包")
