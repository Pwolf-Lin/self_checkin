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
            if(itask['status']==0):continue
            if int(itask['awardNumber']['text'])>1:continue
            taskList.append(itask)
        for itask in taskList:
            # if(int(itask['awardNumber']['text'])>1):
            #     print("跳过任务："+itask['title']['text'])
            #     continue
            title=itask['title']['text']
            receiveUrl="https://ms.jr.jd.com/gw2/generic/mission/newh5/m/receiveMissionForNa"
            req_Data={"environment":"2","missionId":"29869","channelCode":"xjfrwzx",
                     "nonce":"19474417291764269427","signature":"e1c596776f9a501cb3225ab02a6cbb8503e114d5fb0257f4980e9a4c977a282601",
                     "deviceInfo1":{"jsToken":"jdd03MZLLBO3B56DCKXG2PMSOWGGLYXOZ3DL4I5WZF77LXWGSDGBLL4LUNS7XWU4MCJDMGNPFZI6WJ26IDW5JJB6VMVAAPMAAAAM2Y2TPZWYAAAAACFUUHGCMRSDFGIX",
                                    "fp":"1cc0ec2c9d56327da00d36f365daf812","sdkToken":"jdd01IPLEFAU7KQ3BXHXOQL5OFIINBRD2ZDPNOSPNTAF7THTGISGPPUC25SR2NJ2226DHODTAQQFNJSVXYINDRF2Y4ILJRUMZAUVAB2UH5EY01234567",
                                    "eid":"MZLLBO3B56DCKXG2PMSOWGGLYXOZ3DL4I5WZF77LXWGSDGBLL4LUNS7XWU4MCJDMGNPFZI6WJ26IDW5JJB6VMVAAPM",
                                    "token":"jdd01IPLEFAU7KQ3BXHXOQL5OFIINBRD2ZDPNOSPNTAF7THTGISGPPUC25SR2NJ2226DHODTAQQFNJSVXYINDRF2Y4ILJRUMZAUVAB2UH5EY01234567"},
                     "clientType":"h5","clientVersion":"8.0.50"}
            reqData="reqData=" + quote(json.dumps(req_Data, separators=(',', ':')))
            res = requests.request("POST", url = receiveUrl, headers=headers, data=reqData.encode('utf-8')).json()
            if res['resultData']['success']:
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
                    jumpdeaders=headers
                    remove=['x-rp-client','Content-Type',"x-referer-page"]
                    jumpdeaders={k: v for k, v in jumpdeaders.items() if k not in remove}
                    jumpdeaders['Origin']=re.match(r'(https?://[^/]+)', url).group(1)
                    jumpdeaders['Referer']=jumpUrl
                    jumpinfo=f'https://ms.jr.jd.com/gw2/generic/mission/h5/m/getJumpInfo?juid={re.findall(r"juid=([^&#]+)",jumpUrl)[0]}&signature=22358920A036807EA0FB65F39B536E45A142A6869403326C41CDECB9E5BC027281&nonce=32607695931764427669&jrAppVersion=8.0.50&systemEnv=IOS'
                    jumpres=requests.request("GET", jumpinfo, headers=jumpdeaders, timeout=5)
                    
                    requests.request("POST", url = url, headers=headers, data=payload.encode('utf-8')).json()
                    
                    popurl=f'https://ms.jr.jd.com/gw2/generic/legogw/h5/m/getPopTemplateData?timekey={int(time.time() * 1000)}'
                    popres=requests.request("POST", url = popurl, headers=headers, data=payload.encode('utf-8')).json()
                    if popres['success']:
                        qyurl='https://ms.jr.jd.com/gw/generic/jj/newna/m/legoServerExecute?choiseTemplate=QY'
                        body={
                          "channelEncrypt" : 1,
                          "bodyEncrypt" : "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"
                        }
                        # body=json.dumps(body, ensure_ascii=False)
                        qyres=requests.request("POST", url = qyurl, headers=headers, json=body).json()
                        print(qyres)
                except requests.exceptions.RequestException:
                    pass                 
                    time.sleep(5)
#还是有一些问题，但是没找到原因！
#不想写了！！！
# git add .
# git commit -m "问题依然存在"
# git push
###############

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