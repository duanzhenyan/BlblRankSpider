# -*- coding: utf-8 -*-
import scrapy
import json
import math
import time
import datetime
from scrapy.selector import Selector
from BlblRankSpider.orm.dao.top_list import TopListDao
from BlblRankSpider.orm.dao.user_info_Dao import UserInfoDao
from BlblRankSpider.orm.dao.user_video_info_Dao import UserVideoInfoDao
from BlblRankSpider.orm.model.financial_db_model import TopList
from BlblRankSpider.orm.model.financial_db_model import UserInfo
from BlblRankSpider.orm.model.financial_db_model import UserVideoInfo

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
}


def get_now_date_time_str():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def timeStamp_to_unix_time(timeStamp):
    """
    1381419600 ---> 2013-10-10 23:40:00
    :param timeStamp: 时间戳
    :return:
    """
    timeArray = time.localtime(int(timeStamp))
    unix_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return unix_time


class BilibiliRankingSpider(scrapy.Spider):
    name = 'bilibili_ranking'
    allowed_domains = ['bilibili.com']
    # 全站 动画 国创相关 音乐 舞蹈 游戏 科技 数码 生活 鬼畜 时尚 娱乐 影视
    start_urls = [
        'https://www.bilibili.com/ranking/all/0/0/1',
        'https://www.bilibili.com/ranking/all/1/0/1',
        'https://www.bilibili.com/ranking/all/168/0/1',
        'https://www.bilibili.com/ranking/all/3/0/1',
        'https://www.bilibili.com/ranking/all/129/0/1',
        'https://www.bilibili.com/ranking/all/4/0/1',
        'https://www.bilibili.com/ranking/all/36/0/1',
        'https://www.bilibili.com/ranking/all/188/0/1',
        'https://www.bilibili.com/ranking/all/160/0/1',
        'https://www.bilibili.com/ranking/all/119/0/1',
        'https://www.bilibili.com/ranking/all/155/0/1',
        'https://www.bilibili.com/ranking/all/5/0/1',
        'https://www.bilibili.com/ranking/all/181/0/1'
    ]

    def parse(self, response):
        sel = Selector(response)
        rank_tab = sel.xpath('.//li[@class="active"]/text()').extract()[0]
        print('当前爬取榜单为:', rank_tab)
        rank_lists = sel.xpath('//ul[@class="rank-list"]/li')
        top_list_db = TopListDao()
        # 获取榜单基本信息
        for rank_list in rank_lists:
            title = rank_list.xpath('.//div[@class="info"]/a/text()').get()
            video_source_url = rank_list.xpath('.//div[@class="info"]/a/@href').get().split('/av')[-1]
            mid = rank_list.xpath('.//div[@class="info"]/div[@class="detail"]/a/@href').get().split('/')[-1]
            rank_num = rank_list.xpath('.//div[@class="num"]//text()').get()
            score = rank_list.xpath('.//div[@class="info"]/div[@class="pts"]/div/text()').get()

            try:
                if top_list_db.query_data_by_title(title):
                    pass
                else:
                    # 入库数据
                    item = TopList()
                    item.create_time = get_now_date_time_str()
                    item.list_tag = rank_tab
                    item.rank_id = rank_num
                    item.video_source_url = video_source_url
                    item.title = title
                    item.score = score
                    item.mid = mid
                    top_list_db.insert_data(item)
            finally:
                top_list_db.close()

            User_Base_Info_Link = f'https://api.bilibili.com/x/space/acc/info?mid={mid}&jsonp=jsonp'
            yield scrapy.Request(url=User_Base_Info_Link, callback=self.get_user_base_info, headers=headers,
                                 meta={'mid': mid}, dont_filter=True)

    def get_user_base_info(self, response):
        mid = response.meta['mid']
        html = json.loads(response.body)
        data = html['data']
        user_info_db = UserInfoDao()
        try:
            if user_info_db.query_data_mid(mid):
                pass
            else:
                # 入库数据
                item = UserInfo()
                item.user_name = data['name']
                item.user_sex = data['sex']
                item.user_head_url = data['face']
                item.user_level = data['level']
                item.user_fans_badge = data['fans_badge']
                item.user_sign = data['sign']
                item.mid = mid
                user_info_db.insert_data(item)
        finally:
            user_info_db.close()

        # 获取用户视频信息
        page = 1
        user_video = f'https://api.bilibili.com/x/space/arc/search?' \
                     f'mid={mid}&ps=30&tid=0&pn={page}&keyword=&order=pubdate&jsonp=jsonp'
        yield scrapy.Request(url=user_video, callback=self.get_user_video_info,
                             meta={'mid': mid, 'page': page}, dont_filter=True)

    def get_user_video_info(self, response):
        mid = response.meta['mid']
        page = response.meta['page']
        html = json.loads(response.body)
        total_page = math.ceil(html['data']['page']['count'] / 30)
        res_json = json.loads(response.body)
        for vlist in res_json['data']['list']['vlist']:
            bvid = vlist["bvid"]
            video_detail_url = f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
            yield scrapy.Request(url=video_detail_url, callback=self.get_detail,
                                 meta={'mid': mid, 'bvid': bvid}, dont_filter=True)
        if page < total_page:
            page += 1
            user_video = f'https://api.bilibili.com/x/space/arc/search?' \
                         f'mid={mid}&ps=30&tid=0&pn={page}&keyword=&order=pubdate&jsonp=jsonp'
            yield scrapy.Request(url=user_video, callback=self.get_user_video_info,
                                 meta={'mid': mid, 'page': page}, dont_filter=True)

    def get_detail(self, response):
        mid = response.meta['mid']
        bvid = response.meta['bvid']
        # 解析json对象
        html = json.loads(response.body)
        data = html['data']
        user_video_info_db = UserVideoInfoDao()
        try:
            if user_video_info_db.query_data_bvid(bvid):
                pass
            else:
                # 入库数据
                item = UserVideoInfo()
                item.mid = mid
                item.bvid = bvid
                item.video_url = f'https://www.bilibili.com/video/{bvid}'
                item.video_source_url = data['pic']  # 视频缩略图
                item.video_title = data['title']
                item.video_reply = data['stat']['reply']  # 视频评论数量
                item.video_favorite = data['stat']['favorite']  # 视频收藏数量
                item.video_ctime = timeStamp_to_unix_time(data['ctime'])  # 视频创建时间
                user_video_info_db.insert_data(item)
        finally:
            user_video_info_db.close()
