# -*- coding: utf-8 -*-
from scrapy import Spider, Request
import re
from uumtu.items import LiuyueerItem


class LiuyuerSpider(Spider):
    name = 'liuyuer'
    allowed_domains = ['uumtu.com']
    start_urls = ['https://www.uumtu.com/mote/liuyuer.html']

    # def start_requests(self):


    def parse(self, response):
        '''
        # 获取本mote最大页数
        max_page = int(response.xpath('//div[contains(@class, "page")]//a[last()]/@href').extract_first().split('/')[-1].split('.')[0])
        base_url = 'https://www.uumtu.com/mote/liuyuer/{}.html'

        # 爬取所有最新图的列表页面链接
        if max_page > 1:
            for page in range(2, max_page + 1):
                # print('------ other url:', base_url.format(page))
                url = base_url.format(page)
                yield response.follow(url, self.parse)

        # 爬取每一页最新专辑列表中的每个专辑的链接
        catelist = response.xpath('//div[contains(@class, "mote-list-body")]//dl/dd/a/@href').extract()
        print('# catelist:', catelist)
        '''

        # 获取cookie
        # cookie = response.headers.getlist('Set-Cookie')
        # print('&& cookie:', cookie)

        base_url = 'https://www.uumtu.com/mote/liuyuer/{}.html'
        atext = response.xpath('//div[contains(@class, "page")]//a[last()]/text()').extract_first()
        # print('-- a text:', atext)

        # 生成当前页面最新专辑列表中每个专辑的链接请求
        if atext == '末页':
            # print('--- 存在‘末页’。继续请求下一页')
            nextpage = int(response.xpath('//div[contains(@class, "page")]//a[last() - 1]/@href').extract_first().split('/')[-1].split('.')[0])
            # print('---- 第 %s 页 ----' % nextpage)
            url = base_url.format(nextpage)
            yield Request(url, self.parse)
        else:
            print('-- 没有更多专辑了！ --')


        # 生成每个页面的所有专辑列表中每个专辑的链接请求
        catelist = response.xpath('//div[contains(@class, "mote-list-body")]//dl/dd/a/@href').extract()
        # print('# catelist:', catelist)

        # 生成每一个专辑的链接请求
        for cate in catelist:
            yield response.follow(cate, self.parse_single_cate)

    def parse_single_cate(self, response):
        # cookie = response.headers.getlist('Set-Cookie')
        # print('&& cookie:', cookie)

        current_src = response.xpath('//div[contains(@class, "imgac")]/a/img/@src').extract_first()
        current_title = response.xpath('//div[contains(@class, "imgac")]/a/img/@alt').extract_first()
        data = {"src": current_src, "title": current_title}
        # print('=== data: ', data)

        # 生成这张图的item
        item = LiuyueerItem()
        item['url'] = current_src
        item['title'] = current_title
        yield item

        # 生成该mote的指定专辑中的所有图的连接请求
        atext = response.xpath('//div[contains(@class, "page")]//a[last()]/text()').extract_first()
        if atext == '末页':
            # print('--- 该专辑存在‘末页’。继续请求下一张图')
            nexturl = response.xpath('//div[contains(@class, "page")]//a[last() - 1]/@href').extract_first()
            # print('---- 下一张图的url:', nexturl)
            yield response.follow(nexturl, self.parse_single_cate)
        else:
            print('-- 该专辑没有下一张图了！ --')

