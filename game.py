#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#  tanyewei@gmail.com
#  2014/01/16 14:55
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector,Selector

from baidu.items import BaiduGameUrlItem

from scrapy import log

#HTTP请求
from scrapy.http import FormRequest,Request

import re
import pprint

class AppstoreSpider(CrawlSpider):
    name = 'baidu'
    allowed_domains = ["as.baidu.com"]
    #
    start_urls = [
                "http://as.baidu.com/a/asgame?f=web_alad%40next%40rank_3000_1", 
                  ]

    #创建rules
    #   ---拉取游戏列表
    
    # 抓评分，抓下载
    
    rules = (
        #只抓链接
        #Rule(SgmlLinkExtractor(allow=r'(https://itunes.apple.com/cn/genre/ios-[\w-]+/id\d+\?mt=8)', tags='a',)), 
                                     #deny=())),
        Rule(SgmlLinkExtractor(allow=('http://as.baidu.com/a/asgame\?cid=\d+\&s=1\&f=web_alad\%40next')),callback="parse_page",follow=True), 
        #,deny=()),
    )
    
    #查询游戏分类种类
    #       游戏类型
    def parse_page(self, response):
        
        log.msg("===============================================", level=log.INFO)
        log.msg('''My Parse url= %s''' %response.url, level=log.INFO)
        #如果是全部
        if str(response.url).find("cid=102") != -1:
            log.msg(">>>all game not to crawl Pass!!!")
        else:
            log.msg(">>>need to crawl , so going on ... ...")
            sel = Selector(response)
            #
            #game类型
            game_store = BaiduGameUrlItem()
            game_store["game_type_name"] = sel.xpath('//span[@class="gray"]/text()').extract()[0].encode('utf8', 'ignore')
            #game内容
            for game in sel.xpath('//ul[@class="filter-app-list cls"]//li'):
                game_store["game_name"] = game.xpath('div[@class="normal-show"]/h4/span/text()').extract()[0].encode('utf8', 'ignore')
                game_store["game_url"] = game.xpath('div[@class="hover-show"]/a[@class="hover-link"]/@href').extract()[0]
                game_store["game_id"] = str(game_store["game_url"]).split("docid=")[1].split("&")[0]
                game_download_times = game.xpath('div[@class="normal-show"]/div[@class="down-num"]/text()').extract()[0].encode('utf8', 'ignore')
                game_download_times = self.convent_string_to_num(game_download_times)
                log.msg('''>>>game_download_times = [%s]''' %(str(game_download_times)))
                game_store["game_download_times"] = game_download_times
                #迭代请求，请求游戏内容
                #
                #
                if game_store["game_url"]:
                    log.msg('''@@@>>>get game_url = [%s]''' %(game_store["game_url"]))
                    req = Request(game_store["game_url"], callback=self.get_game_content)
                    req.meta['game_type_name'] = game_store['game_type_name']
                    req.meta['game_url'] = game_store['game_url']
                    req.meta['game_name'] = game_store['game_name']
                    req.meta['game_id'] = game_store['game_id']
                    req.meta['game_download_times'] = game_store['game_download_times']
                    yield req
                else:
                    yield game_store
                    
    
    #获取游戏内容
    #
    #
    def get_game_content(self,response):
        log.msg("get_game_content ... ...")
        sel = Selector(response)
        game_store = BaiduGameUrlItem()
        
        game_store['game_type_name'] = response.meta['game_type_name']
        game_store['game_url'] = response.meta['game_url']
        game_store['game_name'] = response.meta['game_name']
        game_store['game_id'] = response.meta['game_id']
        game_store['game_download_times'] = response.meta['game_download_times']

        game_store["game_lastupdate"] = sel.xpath('//div[@class="info-top"]/dl/dd[@class="info-params"]//span[@class="params-updatetime"]/text()').extract()[0].encode('utf8', 'ignore')
        game_store["game_stars"] = sel.xpath('//b[@id="score-num"]/text()').extract()[0].encode('utf8', 'ignore').split("分")[0]
        game_store["game_mark_num"] = sel.xpath('//span[@id="score-participants"]/text()').extract()[0].encode('utf8', 'ignore').split("有")[1].split("人")[0]
        
        return game_store
    
    #转化数据字符串到数字
    #   1.1亿
    #   6300万
    #   2365
    def convent_string_to_num(self, s):
        log.msg('''>>input string is [%s]''' %(s))
        if s.isdigit():
            return str
        elif s.find("万") != -1:
            log.msg("is 万！！！")
            base = float(s.split("万")[0])
            return str(base*10000)
        elif s.find("亿") != -1:
            log.msg("is 亿！！！")
            base = float(s.split("亿")[0])
            return str(base*100000000)
        elif s.find("下") != -1:
            log.msg("is 个！！！")
            base = float(s.split("下")[0])
            return str(base)
        else:
            return str(0)

    
        

