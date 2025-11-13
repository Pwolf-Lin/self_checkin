#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_doGoldbeans.py(金融金豆)
Author: pwolf
Date: 2022/9/19 22:00
cron: 30 0 0 * * *
new Env('金融金豆');
ActivityEntry: 首页排行榜-宝藏榜
"""

import requests, sys, os, re, time, json
from datetime import datetime
from urllib.parse import quote, quote_plus, unquote_plus
from functools import partial
print = partial(print, flush=True)
import warnings
# from selenium import webdriver
warnings.filterwarnings("ignore", category=DeprecationWarning)

# try:
#     from jd_sign import *
# except ImportError as e:
#     print(e)
#     if "No module" in str(e):
#         print("请先运行HarbourJ库依赖一键安装脚本(jd_check_dependent.py)，安装jd_sign.so依赖")
try:
    from jdCookie import get_cookies
    getCk = get_cookies()
except:
    print("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")
    sys.exit(3)

def encode_data(str):
    a=":"
    b="," 
    c=quote_plus(a)
    d=quote_plus(b)
    str = str.replace(c,a)
    str = str.replace(d,b)
    return str

def dailyBeans(cookie):
    deviceInfo = {
        "eid":"2JOOEKCLFZ72UHOPO4QE3ISY6JJYJSM5QP7BFXYH7CMREKO6RPZJUABBRDCSPQXRYD6IR5EMV2AS5SRON2KHTGG5JI",
        "fp":"842891f421fa79092716ea45da4f6cb0",
        "sdkToken":"jdd01QGKVK35HW2AADSQ3USRTQ5YNL3Z5YPBCXZCKKMZ2HRWU57DLCZKR274Q47EKH5ADMSKWSTCYAVSDZX5VLDM6YRQA64IKUQ2GQ3WIR6A01234567",
        "token":"UNUTEQQM5NIM5TZILYZESHYTRB735XQSE3DLANNBKFZTNVWM5V3CIXKOLUUZBFIBAF4KVRWSVVUJI",
        "jstub":"DO6CISXLYV2WBMLCKHCXMF3H5MD4A6AP7ITETMMIARJ6UMVVQKC2JKFIVQS2UN5OAODYRPCSJEBEVWSOIJHXRIY6KKAXCAL7RRD2ZUY"
    }
    deviceInfo = json.dumps(deviceInfo).replace('"','\\"')
    deviceInfo = deviceInfo.replace(" ","")
    reqData={
        "actKey":"SIGN_ACT_NO_002",
       # "scene":"GoldenBeanJr11",
        "deviceInfo":f'{deviceInfo}',
        "nonce":"13141466761675826699",
        "signature":"c003fc54e1c2b184b41201bb0915e89d6bf27a87894071f54c66ed43debee09d"
    }
    reqData=json.dumps(reqData).replace(' ','')
    reqData="reqData=" + quote(reqData).replace('%5C%5C','')
    url = "https://ms.jr.jd.com/gw/generic/hyqy/h5/m/signInV2"
    headers={
        "Host": "ms.jr.jd.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": f"https://member.jr.jd.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie":cookie,
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": ua,
        "Referer": f"https://member.jr.jd.com/",
        "Content-Length": "805",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9"
    }
    dailyRes=requests.request("POST", url = url, headers=headers, data=reqData).json()
    if(dailyRes['resultData']['code']==200):
        if(dailyRes['resultData']['data']['signInYn']):
            award = dailyRes['resultData']["data"]["awardList"][0]["amount"]
            msg = " 签到成功：获得{0}黄金豆\n".format(award)
    elif(dailyRes['resultData']['code']==7011):
        msg = "今日 " + dailyRes['resultData']['message']
    else:
        msg = "日常签到错误，请检查相关参数！"
    return msg

def taskList(cookie):
    url = "https://ms.jr.jd.com/gw2/generic/goldenbean/h5/m/queryTaskInfo"
    payload = f'reqData=%7B%22scene%22%3A%22GoldenBeanJr11%22%2C%22deviceInfo%22%3A%22%7B%5C%22eid%5C%22%3A%5C%22V3SCVUNZ3TSGTJ45KA546QTKCHDKGWYPQVDW7IOCA6MNMVQHWMRMF6GJH2TVVXDYRQQQP6UWUPZRZ5VQF2T5SLPEGE%5C%22%2C%5C%22fp%5C%22%3A%5C%22ce80db7b7f705abc9aa8a37adbb5e082%5C%22%2C%5C%22sdkToken%5C%22%3A%5C%22jdd01XWV4MVVPIAF5E7SMI235DSVCGDALUUCHQXFYU2YNR6TINHJE22AHGX6KCPP7G3FBZRBEXTB7L3UXF6C56UVZ6XWCH57UTDBBTUEM26A01234567%5C%22%2C%5C%22token%5C%22%3A%5C%226U45I6TGE5N53TZIGTNWGD5QZHSJHBJ5MHOFO3TXFTQYJ22CIVCBO5BKIZZJLLIVF35ZS4RZKE3HI%5C%22%2C%5C%22jstub%5C%22%3A%5C%22YMJUV2FEM2SLYBZ5PYRCJTIXJIOEFF7OJLAEHI4B7L6ZLP7XHP3XJ3RIIBVW2J7EPNLTO3ESLH7NANCEBJOQMFQIMNDCKKI54L2AHBI%5C%22%7D%22%7D'
    headers = {
        "Host": "ms.jr.jd.com",
        "Connection": "keep-alive",
        "Content-Length": "670",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://member.jr.jd.com",
        "User-Agent": ua,
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://member.jr.jd.com/activity/goldBean/homeV2/?scene\u003dGoldenBeanJr11\u0026fundUtmSource\u003d1088\u0026fundUtmParam\u003dGoldenBean_assetcardicon\u0026sid\u003d49d1932a9d058d677b482c6b7ff8986w",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q\u003d0.9",
        "Cookie": cookie
    }
    response = requests.request("POST", url = url, headers=headers, data=payload)
    # try:
    res = response.json()
    finMsg = " "
    doMsg = " "
    if res['success']:
        taskList=res['resultData']['data']['taskListInfo']['newTasks']
        for i in range(-1, 1):
            for itask in taskList:
                task_status=itask['status']
                taskId=itask['taskId']
                detail = itask['detail']
                taskName=itask['taskName']
                if("确认" in detail) or ("体验" in detail):
                    continue 
                # taskChannel=itask['taskChannel']
                jumpUrl = itask['jumpUrl']
                jumpUrl = jumpUrl + " " #加个空格防止最后的正则表达式匹配不到
                if task_status==1 :
                    msg = finishTask(jumpUrl,taskId,taskName,cookie)
                    finMsg = finMsg + msg
                # elif task_status==0  :
                #     continue
                elif task_status==-1 or task_status==0 :
                    if ("浏览" in detail) or ("逛" in detail) or ("完成" in detail) or ("1V1" in taskName) :
                        doMsg = doMsg + doTask(jumpUrl,taskId,taskName,cookie)
                    else:
                        continue
        return doMsg,finMsg
    else:
        print(res['success'])
    # except:
    #     msg = "任务失败，请检查脚本！"
    #     print(msg)

def getReqData(channelCode,missionId):
    deviceInfo = {
        "eid":"2JOOEKCLFZ72UHOPO4QE3ISY6JJYJSM5QP7BFXYH7CMREKO6RPZJUABBRDCSPQXRYD6IR5EMV2AS5SRON2KHTGG5JI",
        "fp":"842891f421fa79092716ea45da4f6cb0",
        "sdkToken":"jdd01QGKVK35HW2AADSQ3USRTQ5YNL3Z5YPBCXZCKKMZ2HRWU57DLCZKR274Q47EKH5ADMSKWSTCYAVSDZX5VLDM6YRQA64IKUQ2GQ3WIR6A01234567",
        "token":"UNUTEQQM5NIM5TZILYZESHYTRB735XQSE3DLANNBKFZTNVWM5V3CIXKOLUUZBFIBAF4KVRWSVVUJI",
        "jstub":"DO6CISXLYV2WBMLCKHCXMF3H5MD4A6AP7ITETMMIARJ6UMVVQKC2JKFIVQS2UN5OAODYRPCSJEBEVWSOIJHXRIY6KKAXCAL7RRD2ZUY"
    }
    reqData={
        "channelCode":f"{channelCode}",
        "missionId":f"{missionId}",
        "deviceInfo":deviceInfo
    }
    return reqData

def commData(jumpUrl,missionId,cookie):
    channelCode = re.findall(r"channelCode=(.*?) ",jumpUrl)[0]
    reqData = getReqData(channelCode,missionId)
    query = quote(json.dumps(reqData).replace(" ",""))
    query = encode_data(query)
    headers={
        "Host": "ms.jr.jd.com",
        "Origin": f"https://member.jr.jd.com",
        "Cookie":cookie,
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": ua,
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Referer": f"https://member.jr.jd.com/",
        "Accept-Encoding": "gzip, deflate, br"
    }
    return query,reqData,headers


def doTask(jumpUrl,missionId,taskName,cookie):
    msg = ""
    if("readTime" in jumpUrl):
        readTime = re.findall(r'readTime=(.*?)&', jumpUrl)[0]
        query,reqData,missionHeaders=commData(jumpUrl,missionId,cookie)
        receiveUrl="https://ms.jr.jd.com/gw/generic/mission/h5/m/receiveMission?reqData=" + query
        receiveRes = requests.request("GET", url=receiveUrl, headers=missionHeaders,data = json.dumps(reqData).replace(" ","")).json()
        if receiveRes['resultMsg']=="操作成功":
            jumpRes=requests.request("GET", url=jumpUrl)
            reqData={"missionId":missionId}
            reqData=encode_data(json.dumps(reqData))
            queryUrl="https://ms.jr.jd.com/gw/generic/mission/h5/m/queryMissionReceiveAfterStatus?reqData=" + reqData 
            queryRes=requests.request("GET", url=queryUrl,headers=missionHeaders).json()
            if queryRes['resultData']['success']:
                time.sleep(int(readTime))
                reqData={
                    "missionId":missionId,
                    "readTime":readTime,
                    "nonce":"04796889981672399118",
                    "signature":"180ef99af2c96c1bcdd48c6c7de8dcf4d94887d5109e35cc6a7d35d6372ce2d101"
                }
                reqData = encode_data(json.dumps(reqData))
                finishUrl="https://ms.jr.jd.com/gw/generic/mission/h5/m/finishReadMission?reqData="+ reqData
                finishRes=requests.request("GET", url=finishUrl,headers=missionHeaders).json()
                if finishRes['resultData']['success']:
                    msg = "完成 " + taskName
                else:
                    print("finishRes请求出现问题")
            else:
                print("queryRes请求出现问题")
        else:
            print("receiveRes请求出现问题")
    else:
        host = re.findall(r'//(.*?)/',jumpUrl)[0]
        juid = re.findall(r'juid=(.*?)&',jumpUrl)[0]
        channelCode = re.findall(r"channelCode=(.*?) ",jumpUrl)[0]
        query={
            "juid":juid,
            "channelCode":channelCode
        }
        headers= {
            "Host":host,
            "Cookie":cookie,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": ua,
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.9",
            "Connection": "keep-alive"
        }
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # browser = webdriver.Chrome(chrome_options=chrome_options)
        # browser.get(jumpUrl)
        finishRes=requests.request("GET", url=jumpUrl,headers=headers,data=json.dumps(query))
        if(finishRes==200):
            msg = msg + taskName + " 任务完成"
        else:
            msg = msg + taskName + " 任务未完成"
    return msg

def finishTask(jumpUrl,missionId,taskName,cookie):
    query,reqData,missionHeaders=commData(jumpUrl,missionId,cookie)
    url = "https://ms.jr.jd.com/gw/generic/mission/h5/m/awardMission?reqData=" + query
    res = requests.request("GET",url = url, headers=missionHeaders , data = json.dumps(reqData).replace(" ","")).json()
    if res['resultData']['success']:
        msg = taskName + " " + res["resultData"]["msg"] + "\n" 
    else:
        msg = res["resultData"]["msg"] + "\n" 
    print("领取任务 {0} 成功".format(taskName))
    return msg

if __name__ == '__main__':
    try:
        cks = getCk
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
        ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/application=JDJR-App&clientType=ios&iosType=iphone&clientVersion=6.5.90&HiClVersion=6.5.90&isUpdate=0&osVersion=15.6.1&osName=iOS&screen=896*414&src=App Store&netWork=1&netWorkType=1&CpayJS=UnionPay/1.0 JDJR&stockSDK=stocksdk-iphone_4.2.3&sPoint=MTAwMDcjI2RpYW9xaTQwMDI%3D&jdPay=(*#@jdPaySDK*#@jdPayChannel=jdfinance&jdPayChannelVersion=6.5.90&jdPaySdkVersion=4.00.64.00&jdPayClientName=iOS*#@jdPaySDK*#@)'
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        except IndexError:
            pt_pin = f'用户{num}'
        print(f'\n******开始【京东账号{num}】{pt_pin} *********\n')
        print(datetime.now())
        dailyMsg = dailyBeans(cookie)
        print(dailyMsg)
        taskList(cookie)
        # time.sleep(2)
