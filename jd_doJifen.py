#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_doJifen.py(金融积分)
Author: pwolf
Date: 2022/9/19 22:00
cron: 30 0 0 * * *
new Env('金融积分');
ActivityEntry: 京东金融-每日赚积分
"""

import requests, sys, os, re, time, json
from datetime import datetime
from urllib.parse import quote, quote_plus, unquote_plus
from functools import partial
from utils import get_data
print = partial(print, flush=True)
import warnings
# from selenium import webdriver
warnings.filterwarnings("ignore", category=DeprecationWarning)

#try:
#    from jd_sign import *
#except ImportError as e:
#    print(e)
#    if "No module" in str(e):
#        print("请先运行HarbourJ库依赖一键安装脚本(jd_check_dependent.py)，安装jd_sign.so依赖")
try:
    from jdCookie import get_cookies
    getCk = get_cookies()
except:
    print("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")
    sys.exit(3)

def encode_data(str):
    a=":"
    b=","
    c="{" 
    d="}"
    e=quote(a)
    f=quote(b)
    g=quote(c)
    h=quote(d)
    str = str.replace(e,a)
    str = str.replace(f,b)
    str = str.replace(g,c)
    str = str.replace(h,d)
    return str

def finishTaskEveryday(cookie):
    url = "https://ms.jr.jd.com/gw/generic/mission/h5/m/queryMission"
    payload = f'reqData=%7B%22channelCode%22%3A%22xjfrwzx%22%2C%22deviceInfo%22%3A%7B%22eid%22%3A%22BWNG5ZLWFKFZYAKPP24LRWCCYUZMAEZQHBHOZJ7GT2CKHA753ARV3FKUEFSCMZZU5SMAWVRMHIU65BZSNND7JT42GI%22%2C%22fp%22%3A%222674eff8e27103256ce240431273cd57%22%2C%22sdkToken%22%3A%22jdd01SOIFCTVPITWNPF2J2G35QFENBKGHDBQEGBDBPBVWA6U5OZB6OKBO7WBA4E2PGHPY7INOV6WJEPC2CXQUKIX3POY3XIY4KY3MBRDMG6A01234567%22%2C%22token%22%3A%22XZDILCTEZEY772AYGRVUPLYYXURKAOYRWHR2MTQL66GQZJ22EN5LA3VQ4GBSF4DVGTTHJXWHFPRHS%22%2C%22jstub%22%3A%22PKDUPICYCKBKT4B3OVTRH3PBYM3WFYDEAZQ6IVDW3ZIXL77QXTYLC2IEWJSPCOP7Q26KK4KJMT4HGIQ2PR3CEKFGKCILJBP2P3347GQ%22%7D%7D'
    headers = {
        'Host': 'ms.jr.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': f'https://member.jr.jd.com',
        'Accept-Encoding': 'gzip, deflate, br',
        "Cookie": cookie,
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': ua,
        'Referer': f'https://member.jr.jd.com/',
        'Content-Length': '603',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
    }
    res = requests.request("POST", url = url, headers=headers, data=payload).json()
    # try:
    finMsg = " "
    doMsg = " "
    taskList=[]
    if res['resultData']['success']:
        getList=res['resultData']['data']
        for itask in getList:
            if any("externalCode" in key or 'delayAwardDays' in key for key in itask.keys()):continue
            status=itask['status']
            finishNum=itask['finishNum']
            if(finishNum==1):continue
            awardNum = itask['awards'][0]['awardNum']
            if (awardNum>20):continue
            doLink=itask['doLink'] + ' '
            missionId=itask['missionId']
            name=itask['name']
            if(finishNum==0):
                if(status==1):
                    awardTaskEveryday(doLink,missionId,name,cookie)
                    time.sleep(1)
                elif(status==2):
                    continue
                elif(status==-1):#接取任务
                    reveice(doLink,missionId,name,cookie)
                    time.sleep(1)
                else:
                    taskList.append(itask)
            else:continue
            
        for i in range(1,2):      
            for itask in taskList:
                name=itask['name']
                detail = itask['detail']
                doLink=itask['doLink'] + ' '
                missionId=itask['missionId']            
                status=itask['status']
                # awards=itask['awards']
                if(status==2):
                    msg = name + ' 任务已完成'
                elif(status==1):
                    msg = awardTaskEveryday(doLink,missionId,name,cookie)
                    time.sleep(1)
                elif(status==-1 or status==0):
                    msg = doTask(doLink,missionId,name,cookie)
                    # continue
                # else:
                #     continue
    else:
        print('请求出错，请检查相关参数！')
    # except:
    #     msg = "任务失败，请检查脚本！"
    #     print(msg)

def getReqData(channelCode,missionId):
    deviceInfo = {
        "eid":"BWNG5ZLWFKFZYAKPP24LRWCCYUZMAEZQHBHOZJ7GT2CKHA753ARV3FKUEFSCMZZU5SMAWVRMHIU65BZSNND7JT42GI",
        "fp":"2674eff8e27103256ce240431273cd57",
        "sdkToken":"jdd01UXOHNNTVYDQLXHKJXKT33V2JOZGAJHXI2Y6SGYHWLMNUZVSJPLUCBWHN26QWZ4EGROWGDS2QXZUAMCDWOV62E4ZFETC622YURUE7RLY01234567",
        "token":"FKLENSPDVYJTBVU6E7FQCMPJUJNPHBT2EJA5VHRAPQMQAS73GRHNVB5G7SFMDMPKDMNFIE3D2AJ3Q",
        "jstub":"IVNIEDJTONRFP2TYBNLBJ273XTZQZKAD5OEO3WMAZX5VKRVWGUBEP6GNEL5M5RFPTJ5GFPL2VJUHC7ZRXSF65RFNI5CXBWS3ABGOAKI"
    }
    if(missionId==''):
        reqData={
            "deviceInfo":deviceInfo
        }
    else:
        reqData={
            "channelCode":f"{channelCode}",
            "missionId":int(missionId),
            "deviceInfo":deviceInfo
        }
    return reqData

def commData(doLink,missionId,cookie):
    channelCode = re.findall(r"channelCode=(.*?) ",doLink)[0]
    reqData = getReqData(channelCode,missionId)
    reqData = quote(json.dumps(reqData).replace(" ",""))
    reqData = 'reqData=' + reqData
    headers={
        'Host': 'ms.jr.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': f'https://member.jr.jd.com',
        'Accept-Encoding': 'gzip, deflate, br',
        "Cookie":cookie,
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': ua,
        'Referer': f'https://member.jr.jd.com/',
        'Content-Length': '629',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
    }
    return reqData,headers

def reveice(doLink,missionId,taskName,cookie):
    # readTime = re.findall(r'readTime=(.*?)&', doLink)[0]
    reqData,doHeaders=commData(doLink,missionId,cookie)
    receiveUrl="https://ms.jr.jd.com/gw/generic/mission/h5/m/receiveMission"
    receiveRes = requests.request("POST", url=receiveUrl, headers=doHeaders,data = reqData).json()
    if receiveRes['resultMsg']=="操作成功":
        print("  接取任务 {0} 成功".format(taskName))
    return

def doTask(doLink,missionId,taskName,cookie):
    msg = ""
    try:
        if("readTime" in doLink):
            readTime = re.findall(r'readTime=(.*?)&', doLink)[0]
            jumpRes=requests.request("GET", url=doLink)
            reqData={"missionId":str(missionId)}
            reqData=encode_data(quote(json.dumps(reqData).replace(" ","")))
            queryUrl="https://ms.jr.jd.com/gw/generic/mission/h5/m/queryMissionReceiveAfterStatus?reqData=" + reqData
            doHeaders={
                'Host': 'ms.jr.jd.com',
                'Origin': 'https://member.jr.jd.com',
                "Cookie":cookie,
                "Connection": "keep-alive",
                "Accept": "*/*",
                "User-Agent":ua,
                "Accept-Language": "zh-CN,zh-Hans;q=0.9",
                "Referer": "https://member.jr.jd.com/",
                "Accept-Encoding": "gzip, deflate, br"
            } 
            queryRes=requests.request("GET", url=queryUrl, headers=doHeaders).json()
            if queryRes['success']:
                time.sleep(int(readTime))
                reqData={
                    "missionId":missionId,
                    "readTime":int(readTime),
                    "nonce":"17145849041672798287",
                    "signature":"78eed5ec128c3a3b8fd42495a5c9db9e5f775dbc83bf6f27b5847c55417e693e01"
                }
                # doHeaders['Origin']='https://member.jr.jd.com'
                # doHeaders['Referer']='https://member.jr.jd.com/'
                reqData=encode_data(quote(json.dumps(reqData).replace(" ","")))
                finishUrl="https://ms.jr.jd.com/gw/generic/mission/h5/m/finishReadMission?reqData="+ reqData
                finishRes=requests.request("GET", url=finishUrl,headers=doHeaders).json()
                if finishRes['resultData']['success']:
                    msg = "完成 " + taskName
                else:
                    print("finishRes请求出现问题")
            else:
                print("queryRes请求出现问题")
            # else:
            #     print("receiveRes请求出现问题")
        else:
            signature="&signature=78eed5ec128c3a3b8fd42495a5c9db9e5f775dbc83bf6f27b5847c55417e693e01"
            nonce="&nonce=17145849041672798287"
            if(('juid' in doLink)==False):return 
            host = re.findall(r'//(.*?)/',doLink)[0]
            juid = re.findall(r'juid=(.*?)&',doLink)[0]
            channelCode = re.findall(r"channelCode=(.*?) ",doLink)[0]
            query={
                "juid":juid,
                "channelCode":channelCode
            }
            headers= {
                "Host":host,
                "Cookie":cookie,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "User-Agent": ua,
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,en-US;q=0.9",
                "Connection": "keep-alive"
            }
            finishRes=requests.request("GET", url=doLink,headers=headers,data=json.dumps(query))
            if(finishRes.status_code==200):
                reqData={"juid":juid,
                         "signature":"78eed5ec128c3a3b8fd42495a5c9db9e5f775dbc83bf6f27b5847c55417e693e01",
                         "nonce":"17145849041672798287"
                        }
                # query=quote(json.dumps(reqData)).replace('%3A',':')
                query = "juid={0}&signature={1}&nonce={2}".format(reqData["juid"],reqData["signature"],reqData["nonce"])
                jumpUrl='https://ms.jr.jd.com/gw/generic/mission/h5/m/getJumpInfo?' + query
                headers["Host"] = 'ms.jr.jd.com'
                headers["Origin"] = 'https://' + host
                headers["Accept"] = 'application/json'
                headers["Referer"]= headers["Origin"] +'/'
                getJumpRes= requests.request("GET", url=jumpUrl,headers=headers,data=json.dumps(reqData).replace(' ','')).json()
                if(getJumpRes['resultData']['success']):
                    jumpUrl = getJumpRes['resultData']['data']['jumpUrl'] + " "
                    if("babelChannel" in jumpUrl): babelChannel = re.findall(r"babelChannel=(.*?) ",jumpUrl)[0]
                    header={
                        "Host":"h5.m.jd.com",
                        'Connection': 'keep-alive',
                        'hybridXslAvailableElements': 'hybrid-video;hybrid-image',
                        'Accept': '*/*',
                        'User-Agent': 'jdapp;iPhone;11.4.0;;;M/5.0;JDEbook/openapp.jdreader;appBuild/168411;jdSupportDarkMode/0;ef/1;ep/%7B%22ciphertype%22%3A5%2C%22cipher%22%3A%7B%22ud%22%3A%22ZNc4CJDwDJO3CQYnD2G3DNVvDwY3DWG1CwC2CtK2ZNPwEQPuENZrYG%3D%3D%22%2C%22sv%22%3A%22CJUkDs4n%22%2C%22iad%22%3A%22%22%7D%2C%22ts%22%3A1672625706%2C%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22version%22%3A%221.0.3%22%2C%22appname%22%3A%22com.360buy.jdmobile%22%2C%22ridx%22%3A-1%7D;Mozilla/5.0 (iPhone; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
                        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Request-from': 'htmlpreload'
                    }
                    if("babelChannel" in jumpUrl):query='babelChannel='+babelChannel
                    ##跳转APP似乎有问题，先这样吧，改不动了(来京东医药馆不跳转)
                    res = requests.request("GET", url=jumpUrl,headers=header,data=query)
                    if(res.status_code==200):
                        msg = '  '+ msg + taskName + " 任务完成"
                        print(msg)
                    else:
                        msg = '  '+ msg + taskName + " 任务未完成"
                        print(msg)
            else:
                msg = '  '+ msg + taskName + " 任务未完成"
                print(msg)
    except Exception as err:
        print(msg + taskName + " 任务报错:")
        print(err)
    return msg

def awardTaskEveryday(doLink,missionId,taskName,cookie):
    reqData,awardHeaders=commData(doLink,missionId,cookie)
    url = 'https://ms.jr.jd.com/gw/generic/mission/h5/m/awardMission'
    res = requests.request("POST",url = url, headers=awardHeaders , data = reqData).json()
    if res['resultData']['success']:
        msg = taskName + " " + res["resultData"]["msg"] + "\n" 
    else:
        msg = res["resultData"]["msg"] + "\n" 
    
    print("  领取积分 {0} 积分成功".format(taskName))
    return msg

def sign(cookie):
    taskList = []
    url = 'https://ms.jr.jd.com/gw2/generic/useFission/h5/m/queryAllMissionListByPin' 
    deviceInfos={
            "jsToken":"",
            "fp":"6dc5e5dfe8ccd4244f44ac146fc05d4a",
            "sdkToken":"jdd01Z3K2OQOL53DIYA7DEC4VRVEBWHESCJHLY63W6QDNYSSCMWCU3C4W56YBTMGQXGEMOZT5RB2CGMQLR7GHWLZLHRGUP4HWTMEMXE7LI4Y01234567",
            "eid":"ZHQBTOSEYNXRG65MFPRQTROTVLFGPR3XT7YNPJRRPSQ4WWKC66XPQPB3DJLMXNG425YBGASAKR3TN3RHELIOVMIFA4",
            "qdPageId":"9V7X"
        }
    body = {
        'deviceInfos':deviceInfos,
        "nodeId":"missionList",
        "fissionActivityCode":"Applet_fission","missionQueryWay":"myself",
        "channelCode":"xcxlb-jdjrwddb","xcxAppId":"","clientCode":"JRAPP","client":"h5"
    }
    reqData = "reqData=" + quote(json.dumps(body).replace(' ',''))
    headers={
        'Host': 'ms.jr.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Origin': 'https://eco.jr.jd.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie':cookie,
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent':ua,
        'Referer': 'https://eco.jr.jd.com/',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
    }
    res=requests.request("POST", url=url, headers=headers, data=reqData).json()
    if res['success']:
        InfoList = res['resultData']['data'][0]['couponInfoList']
        for itask in InfoList:
            name = itask['name']
            if ('签到' in name) or('浏览' in name) or ('了解' in name):
                taskList.append(itask)
    for i in range(1,2):
        for itask in taskList:
            status= itask['status']
            name = itask['name']
            if('签到' in name): 
                dosign(deviceInfos,headers)
            else:
                if (status == 2):print(name +' 任务已完成')
                if (status == 0):
                    doLink= itask['doLink'] + ' '
                    missionId = itask['missionId']
                    doTask(doLink,missionId,name,cookie)
    return        

def dosign(deviceInfos,headers):               
    signData = {"channel":"xcxlb","activityNo":"4001"}
    signData = json.dumps(signData).replace(' ','').replace('\"','\\\"')
    aarParam = {
        "nonce":"03537992381678490946",
        "signature":"7fd427c0ed5d6f8ffab5ea15ca21c49e03b63ed12a51292f714317077bedede600",
        "signData":signData,
        "domain":"eco.jr.jd.com",
        "uri":f"https://eco.jr.jd.com/wxmp-fission/task?channel=xcxlb-jdjrwddb&jrcontainer=h5&jrlogin=true"
    }
    reqData= {
        "deviceInfos":deviceInfos,
        "aarParam":aarParam,
        "channel":"xcxlb",
        "activityNo":"4001",
        "channelCode":"xcxlb-jdjrwddb",
        "xcxAppId":"",
        "clientCode":"JRAPP",
        "client":"h5"
    }
    reqData ="reqData=" + quote(json.dumps(reqData).replace(' ','')).replace('%5C%5C','').replace("/","%2F")
    url = 'https://ms.jr.jd.com/gw/generic/mkt/h5/m/sign'
    res = requests.request("POST", url=url, headers=headers, data=reqData).json()
    if res['resultData']['success']:
        print("签到领积分完成")
    else:
        msg = res['resultData']['showMsg']
        print(msg)
    return 

def getExtraHeaders(cookie):
    headers={
        'Host': 'ms.jr.jd.com',
        'Origin': f'https://stock-rs.jd.com',
        'Cookie': cookie,
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': ua,
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Referer': f'https://stock-rs.jd.com/',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    return headers

def finishTaskExtra(cookie):
    channelCode = "1018HYR-2" ; missionId = ''
    reqData = getReqData(channelCode,missionId) ; reqData['channelCode'] = "1018HYR-2"
    reqData = quote(json.dumps(reqData).replace(" ",""))
    url = 'https://ms.jr.jd.com/gw/generic/mission/h5/m/queryMission?reqData=' + reqData
    headers=getExtraHeaders(cookie)
    res = requests.request("GET", url = url, headers=headers).json()
    taskList=[]
    if res['resultData']['success']:
        getList=res['resultData']['data']
        for itask in getList:
            status=itask['status']
            awardNum = itask['awards'][0]['awardNum']
            if (awardNum>20):continue
            doLink=itask['doLink'] + ' '
            missionId=itask['missionId']
            name=itask['name']
            # detail = itask['detail']
            if(status==1):
                awardExtra(missionId,name,cookie)
                time.sleep(1)
            elif(status==2):
                continue
            elif(status==0)or(status==-1):
                taskList.append(itask)
    for i in range(1,2):      
            for itask in taskList:
                name=itask['name']
                doLink=itask['doLink'] + ' '
                missionId=itask['missionId']            
                status=itask['status']
                # awards=itask['awards']
                if(status==2):
                    print('  '+ name + ' 任务已完成')
                elif(status==1):
                    msg = awardExtra(missionId,name,cookie)
                    time.sleep(1)
                elif(status==-1 or status==0):
                    msg = doTask(doLink,missionId,name,cookie)
    return

def awardExtra(missionId,name,cookie):
    channelCode = "1018HYR-2" 
    reqData = getReqData(channelCode,missionId)
    reqData["qdPageId"]="stock_guess" ; reqData["mdClickld"]=int(missionId)
    reqData = quote(json.dumps(reqData).replace(" ",""))
    url = 'https://ms.jr.jd.com/gw/generic/mission/h5/m/awardMission?reqData=' + reqData
    headers=getExtraHeaders(cookie)
    res = requests.request("GET",url = url, headers=headers).json()
    if res['resultData']['success']:
        msg = name + " " + res["resultData"]["msg"] + "\n" 
    else:
        msg = res["resultData"]["msg"] + "\n" 
    
    print("  领取任务 {0} 积分成功".format(name))
    return msg


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
        ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/application=JDJR-App&clientType=ios&iosType=iphone&clientVersion=6.5.90&HiClVersion=6.5.90&isUpdate=0&osVersion=15.6.1&osName=iOS&screen=896*414&src=App Store&netWork=1&netWorkType=1&CpayJS=UnionPay/1.0 JDJR&stockSDK=stocksdk-iphone_4.2.3&sPoint=MTAwMDcjI2RpYW9xaTQwMDI%3D&jdPay=(*#@jdPaySDK*#@jdPayChannel=jdfinance&jdPayChannelVersion=6.5.90&jdPaySdkVersion=4.00.64.00&jdPayClientName=iOS*#@jdPaySDK*#@)'
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        except IndexError:
            pt_pin = f'用户{num}'
        print(f'\n******开始【京东账号{num}】{pt_pin} *********\n')
        print(datetime.now())
        print('每日赚积分任务：')
        finishTaskEveryday(cookie)#每日赚积分
        print('\n')
        time.sleep(2)
        print('猜涨跌任务：')
        finishTaskExtra(cookie)
        print('\n')
        time.sleep(2)
        # print('签到领积分任务：')
        # sign(cookie)
        # time.sleep(2)
