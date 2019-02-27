# coding:utf-8
import requests
import json
import time

from models.xyproduct import XYProduct, XyproductMethod
from config import *

# TODO: 商品的去重

def make_url(page_num, category_id):
    part_one = 'https://s.2.taobao.com/list/waterfall/waterfall.htm?'
    part_two = 'wp=' + page_num
    part_three = '&_ksTS=1550133630515_142'
    part_four = '&callback=jsonp143&stype=1'
    part_five = '&catid=' + category_id
    part_six = '&st_trust=1'
    part_seven = '&ist=1'
    return part_one + part_two + part_three + part_four + part_five + part_six + part_seven


def get_page(url):
    req = requests.get(url)
    if req.status_code != 200:
        return -1
    if len(req.text) < 100:
        return -1
    return req.text[12:-2]


def page_decoder(json_context):
    return json.loads(json_context)


def xyproduct2db(cid, page, save=True):
    """
    数据入库，save可选 入库/打印
    """
    # 获取到url
    url = make_url(page, cid)
    # 获取界面
    page = get_page(url)
    while page == -1:
        time.sleep(SPIDER_SLEEP_TIME_SEC)
        page = get_page(url)
    product_list = list()
    # 解析界面
    try:
        jsonContent = page_decoder(page)
        # TODO：先判断当前页的商品是否已经在数据库中，用最快的方法截取需要入库的部分
        # 插入数据
        for content in jsonContent['idle']:
            categoryId = cid
            imageUrl = content['item']['imageUrl'][2:]
            itemUrl = content['item']['itemUrl'][2:]
            isBrandNew = content['item']['isBrandNew']
            price = content['item']['price']
            orgPrice = content['item']['orgPrice']
            city = content['item']['provcity']
            description = content['item']['describe']
            commentCount = content['item']['commentCount']
            title = content['item']['title']
            userNick = content['user']['userNick']
            vipLevel = content['user']['vipLevel']
            isSinaV = content['user']['isSinaV']
            userItemsUrl = content['user']['userItemsUrl'][2:]
            product_list.append(XYProduct(
                categoryId = categoryId,
                imageUrl = imageUrl,
                itemUrl = itemUrl,
                isBrandNew = isBrandNew,
                price = price,
                orgPrice = orgPrice,
                city = city,
                description = description,
                commentCount = commentCount,
                title = title,
                userNick = userNick,
                vipLevel = vipLevel,
                isSinaV = isSinaV,
                userItemsUrl = userItemsUrl
            ))
    except:
        pass
    if save:
        XyproductMethod.batch_add_xyproduct(product_list)
    else:
        print(product_list)
    time.sleep(SPIDER_SLEEP_TIME_SEC)

def xy_spider(cid, pages, save=True):
    """ 此爬虫的入口函数
    args:
        cid->Str: 商品分类ID
        pages->Int&None: 爬取商品总页数 为None时则忽略
        save->bool: 是否入库，默认入库。为False时则在控制台打印以便单文件调试
    return: None
    """
    if pages:
        for n in range(1, pages+1):
            xyproduct2db(cid=cid, page=n, save=save)
    else:
        n = 1
        while True:
            xyproduct2db(cid=cid, page=n, save=save)
            n += 1

if __name__ == "__main__":
    xy_spider('50100398', 2, False)

#
#
# url = "https://s.2.taobao.com/list/waterfall/waterfall.htm?wp=2&" \
#       "_ksTS=1550133630515_142&" \
#       "callback=jsonp143&" \
#       "stype=1&" \
#       "catid=50100398&" \
#       "st_trust=1&" \
#       "ist=1"

