#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_jr_getBeans.py(赚京豆)
Author: pwolf
Date: 2025/11/14 22:00
cron: 30 0 0 * * *
new Env('金融积分');
ActivityEntry: 京东金融-省钱-做任务领京豆
"""

import requests, sys, os, re, time, json
from datetime import datetime
from urllib.parse import quote, quote_plus, unquote_plus,urlparse
from functools import partial
from utils import get_data
print = partial(print, flush=True)
import warnings
# from selenium import webdriver
warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    from jdCookie import get_cookies
    getCk = get_cookies()
except:
    print("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")
    sys.exit(3)



def finishTaskEveryday(cookie):
    url = "https://ms.jr.jd.com/gw2/generic/legogw/h5/m/getPageInfoSafetyTranslate?pageType=11189"
    req_data = {
        "clientVersion": "8.0.50",
        "clientType": "ios",
        "pageType": 11189,
        "pageId": 11189,
        "ctp": 11189,
        "pageNum": -1,
        "buildCodes": ["common", "topData", "float", "tag"],
        "extParams": {
            "channelCode": "inside",
            "signData": {
                "sdkToken": "jdd01ECXZLXE6OX5YJKJN2U3E5YFD4G6YAJI6E46A32YCEQZRATZ3RD7DB6CQETHEO7ZTMEIQFH7P2J47M52E62JVRYXO2RHNJI6GKIZ2K3A01234567"
            },
            "sdkToken": "jdd01ECXZLXE6OX5YJKJN2U3E5YFD4G6YAJI6E46A32YCEQZRATZ3RD7DB6CQETHEO7ZTMEIQFH7P2J47M52E62JVRYXO2RHNJI6GKIZ2K3A01234567",
            "nonce": "10490295971763087153",
            "signature": "11629B6480B7E92B95C64D5F980CD4180A1D98E6DD916C3D60CBC4AD1B4D709C81",
            "deviceInfos": "{\"sdkToken\":\"jdd01ECXZLXE6OX5YJKJN2U3E5YFD4G6YAJI6E46A32YCEQZRATZ3RD7DB6CQETHEO7ZTMEIQFH7P2J47M52E62JVRYXO2RHNJI6GKIZ2K3A01234567\"}",
            "riskQdPageId": "gainJDbean",
            "riskQdPageName": "赚京豆任务列表页",
            "aarVersion": "2",
            "itemIds": [],
            "pageName": "pageCoinQuest",
            "clientEnv": "2",
            "jumpSource": "001",
            "abTest": "",
            "schemaList": ["sinaweibo://", "imeituan://", "cn.10086.app://"],
            "sourceVersion": "62",
            "reqSource": "0",
            "dynamicReq": True,
            "pageUrl": "https:member.jr.jd.com/member/coinQuest/coin/",
            "urlKey": "/member/coinQuest/coin/",
            "clientName": "web"
        }
    }
    ts17 = (now := datetime.now()).strftime("%Y%m%d%H%M%S") + f"{now.microsecond // 1000:03d}"
    cco_data = {
        "client": "ios",
        "clientVersion": "",
        "h5st": f"{ts17};za9tim3g6djtjt35;73fdb;tk03wb7221c2418nRWOToxC2GutlIupnvQEaVk5V8b6zVRL0yb2eTOmSzUJwM2O14CPCQHaYi-QGBhmxtuWLC1F8lbHz;39d7fe1e4c4d14a64232c64901404c8bb23183688b988dd81d5e870f9d2a5b47;5.2;1763087153156;eVxhk4BZsVeE3Q6H9IuIutLHt8OJnYfZnZfF7YfZB5hWth-T-prJ_YfZB5hW-d7UwVbTxBuJ9EOT_UOTxRuJqdbV7cuUqB_UuFeUu9uJ-h-T-h6Q1E7J8E6ZBh-f1ZvJ-UeUtRLJ_IuU7cLJxZeI7MOVAIuJrV7U-UeVAUbUoZfZnZvFAI6GAU7ZBh-f1ZfV-h-T-ROE-YfZB5hW-V_WvpPUrkMI187ICMeH-h-T-J6ZBh-f1Z-RCY_L5QLWq99ZB5_Z0kbIzc7F-hfZXx-Z8orG5gMH-h-T-JbF-hfZXxPCBh-f-97Q-h-T-VOVsY7ZBhfZB5hWvh-T-dOVsY7ZBhfZB5hWtdeZnZfVwN6J-hfZBh-f1BOWB5_ZvdOE-YfZBhfZXx-ZoZeNvV7E-Y8INYfZnZPGyQ7GAY6ZBhfZB5hWxh-T-BOE-YfZBhfZXxfVB5_ZqN6J-hfZBh-f1Z_VB5_ZrN6J-hfZBh-f1heZnZPUsY7ZBhfZB5hWxh-T-ROE-YfZBhfZXxPVwh-T-VOE-YfZBhfZXx-ZtpPVzh_ZB5_ZwN6J-hfZBh-f1heZnZvHqYfZBhfZXxPUB5_Zuw7ZBhfZB5hWxh-T-x7ZBhfZB5hWxh-T-RrE-hfZBh-fmg-T-R7G8QaD8YfZB5hWkgfZXZPU-UeI-8_IxZOJ9cbUCQ7H-h-T-deF-hfZBh-fmg-T-haF-hfZXx-ZJgvNSgvJAsdZ80LH1gPVCQuKpdeZOkdZ8orG5gMHBNcNegvT8orG5gMH-h-T-dLEuYfZB5xD;817e923c23bf022dff9c0db93b24bc78c6c03d6be29f1cede473376d5d1cfef5;fZRIx8aM8ELJxwPGsoNI6cbF1RLP8ELJxwfFtUbWzkLHuYKILQ6G88bG_wPIx8aMtoLI4wrJ",
        "_stk": "clientType,clientVersion,ctp,pageId,pageNum,pageType",
        "_ste": 1,
        "t": int(time.time() * 1000)
    }
    eid = "jdd01ECXZLXE6OX5YJKJN2U3E5YFD4G6YAJI6E46A32YCEQZRATZ3RD7DB6CQETHEO7ZTMEIQFH7P2J47M52E62JVRYXO2RHNJI6GKIZ2K3A01234567"
    payload = f"reqData={quote(json.dumps(req_data, separators=(',', ':')))}&cco={quote(json.dumps(cco_data, separators=(',', ':')))}&eid={eid}"
    headers = {
        "Host": "ms.jr.jd.com",
        "Accept": "application/json, text/plain, */*",
        "Sec-Fetch-Site": "same-site",
        "x-rp-client": "h5_1.0.0",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Mode": "cors",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": f"https://member.jr.jd.com",
        "User-Agent": ua,
        "x-referer-page": f"https://member.jr.jd.com/member/coinQuest/coin/",
        "Referer": f"https://member.jr.jd.com/",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Cookie": cookie,
    }
    res = requests.request("POST", url = url, headers=headers, data=payload.encode('utf-8')).json()
    # with open('temp_response.json', 'w', encoding='utf-8') as f:
    #     json.dump(res, f, ensure_ascii=False, indent=2)
    # try:
    finMsg = " "
    doMsg = " "
    taskList=[]
    if res['success']:
        getList=res['resultData']['resultList'][2]['templateData']['taskList']
        for itask in getList:
            # if(int(itask['awardNumber']['text'])>1):
            #     print("跳过任务："+itask['title']['text'])
            #     continue
            if(itask['status']==-1):
                title=itask['title']['text']
                jumpUrl = itask['button']['jumpData']['jumpUrl']
                getheaders={
                    "Host":urlparse(url).netloc,
                    "Cookie":cookie,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "User-Agent": ua,
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
                    "Connection": "keep-alive"}
                try:
                    requests.request("GET", jumpUrl, headers=getheaders, timeout=5)
                except requests.exceptions.RequestException:
                    pass                 
                    time.sleep(5)
            else:continue

        return











if __name__ == '__main__':
    try:
        #cks = getCk
        data = get_data()
        _check_items_list = data.get("JD", [])
        cks=[_check_items_list[0]["cookie"]]
        if not cks:
            sys.exit()
    except:
        print("未获取到有效COOKIE,退出程序！")
        sys.exit()
    num = 0
    for cookie in cks[:]:
        num += 1
        global ua
        # ua = userAgent()
        ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/application=JDJR-App&clientType=ios&iosType=iphone&clientVersion=8.0.50&HiClVersion=8.0.50&isUpdate=0&osVersion=18.4.1&osName=iOS&screen=896*414&src=App Store&netWork=2&netWorkType=4&CpayJS=UnionPay/1.0 JDJR&stockSDK=stocksdk-iphone_6.0.0&sPoint=&jdPay=(*#@jdPaySDK*#@jdPayChannel=jdfinance&jdPayChannelVersion=8.0.50&jdPaySdkVersion=4.01.69.00&jdPayClientName=iOS*#@jdPaySDK*#@)'
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        except IndexError:
            pt_pin = f'用户{num}'
        print(f'\n******开始【京东账号{num}】{pt_pin} *********\n')
        print(datetime.now())
        print('每日赚积分任务：')
        finishTaskEveryday(cookie)#每日赚积分