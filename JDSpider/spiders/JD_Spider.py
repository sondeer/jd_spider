# - * - coding: utf-8 - * -
import time

__author__ = "放养的小爬虫"

from scrapy.spiders import CrawlSpider
from JDSpider.items import JdspiderItem
from scrapy.selector import Selector
from scrapy.http import Request
import requests
import re, json


class JdSpider(CrawlSpider):
    name = "JDSpider"
    redis_key = "JDSpider:start_urls"
    start_urls = ['https://list.jd.com/list.html?cat=12218,13591&page=1&sort=sort_rank_asc&trans=1&JL=6_0_0#J_main']

    def parse(self, response):
        item = JdspiderItem()
        selector = Selector(response)
        # gl_items = selector.xpath('//li/div[@class="gl-i-wrap j-sku-item"]')
        gl_items = selector.xpath('//li[@class="gl-item"]')
        # print('得到网页的内容')
        for each in gl_items:
            print('开始解析得到的数据')
            # 得到物品名称
            name = each.xpath('div/div[@class="p-name"]/a/em/text()').extract()[0].strip()
            # print(name)
            # 得到店铺的链接
            name_link = 'http:' + str(each.xpath('div/div[@class="p-name"]/a/@href').extract()[0])
            # print(name_link)

            temphref = each.xpath('div/div[@class="p-name"]/a/@href').extract()
            temphref = str(temphref)
            skuId = str(re.search('com/(.*?)\.html', temphref).group(1))
            # print(skuId)

            # 得到价格信息
            price_url = 'https://p.3.cn/prices/mgets?&skuIds=J_' + skuId
            print(price_url)
            price_text = requests.get(price_url).text
            data = json.loads(price_text)[0]
            o_price = data['m']
            c_price = data['p']
            print(o_price, c_price)

            # 得到评论信息
            commit_url = 'https://club.jd.com/comment/productCommentSummaries.action?&referenceIds=' + skuId
            print(commit_url)
            try:
                commit_text = requests.get(commit_url).text
                comment_count = json.loads(commit_text)['CommentsCount'][0]['CommentCountStr']
                print(comment_count)
            except Exception as ex:
                print('request commit_url failed')
                print(ex)

            # 得到店铺名称
            shopId = each.xpath('div/@venderid').extract()[0]
            shop_url = 'https://rms.shop.jd.com/json/pop/shopInfo.action?ids=' + str(shopId)
            print(shop_url)
            try:
                shop_text = requests.get(shop_url).text
                data = json.loads(shop_text)
                shop_name = data[0]['name']
                print(shop_name)
            except Exception as ex:
                print('get shop id failed')
                print(ex)

            item['name'] = name
            item['ori_price'] = o_price
            item['cur_price'] = c_price
            item['commit'] = comment_count
            item['shop'] = shop_name
            item['ItemID'] = skuId
            item['shop_href'] = name_link

            yield item
            time.sleep(0.2)

        # nextLink = selector.xpath('/html/body/div[8]/div[2]/div[4]/div/div/span/a[7]/@href').extract()
        print('开始得到下一页的地址')
        nextLink = selector.xpath('//div[@class="page clearfix"]/div/span/a[@class="pn-next"]/@href').extract()
        print(nextLink)
        if nextLink:
            nextLink = 'https://list.jd.com'+ nextLink[0]
            print(nextLink)
            yield Request(nextLink,callback=self.parse)
