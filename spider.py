
import time
import requests

# modify 请求头，这是是从chrome直接复制过来的，代码会自动格式化，请求头建议换成自己的
chrome_header = '''
:authority: blog.csdn.net
:method: GET
:path: /phoenix/web/blog/hot-rank?page=0&pageSize=25&type=
:scheme: https
accept: application/json, text/plain, */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5
cookie: uuid_tt_dd=10_18796429750-1658977927448-465913; c_adb=1; UN=qq_34598061; BT=1658978250138; p_uid=U010000; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_18796429750-1658977927448-465913!5744*1*qq_34598061; ssxmod_itna=QqGxBDRQYCqWqGKG=DXGG7AHEuDRho2gGx+80iqGXd53DZDiqAPGhDC+8KRGG4hD+rK7A8nD=zDRSDxF31bl+3hflheiTD4q07Db4GkDAqiOD7wb3Dx1q0rD74irDDxD3fxD5zumx0Rll9wjg0S+VDBolYqQBIq4DCg4Dbrp9DB=dxBQ/IdQUznUDgTRsGG3TlxhWCGpxUBqYY7DoQhh5ApDYGDoeU7DYWRqNBrq3loq4DDfxCxx=eD=; ssxmod_itna2=QqGxBDRQYCqWqGKG=DXGG7AHEuDRho2gGx+80DA6nd4o4D/8XQDFx+7AUZaUKApdMm00yNYqhrA9RdPH/q2U+VnZurRwDrSe9c6O6Z6LF6kl3x78RFg32LajmrF1fHKf6HN86xqWRWsVcmzboeOEo5aEgKCZppi=ODGK/KhmPObH/ntSpOHiomsDzYezDAmWImh96WTQm4DwhitiYubzBGWq00bntG6HYWUM9k=KYxDLxG7eYD==; c_dl_um=-; c_segment=9; dc_sid=7d59a3117eb767df5dbb4a3f335ed0c7; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1658977929,1659538304,1659962559; c_dl_fref=https://blog.csdn.net/m0_46607117/article/details/124209280; c_dl_fpage=/download/weixin_42122988/19111107; c_dl_prid=1660133186668_691745; c_dl_rid=1660133187783_241806; dc_session_id=10_1660315971060.918825; csrfToken=4a5LP-oebPYwwJsk8d4WhtWO; c_first_ref=default; SESSION=eed18c25-b71d-4d27-9190-02f6d1349576; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22qq_34598061%22%2C%22scope%22%3A1%7D%7D; hide_login=1; c_pref=default; firstDie=1; c_first_page=https%3A//blog.csdn.net/qq598535550/article/details/51287630; c_dsid=11_1660317250975.902121; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1660317256; unlogin_scroll_step=1660317259022; log_Id_view=102; log_Id_click=48; c_ref=https%3A//blog.csdn.net/rank/list; c_page_id=default; dc_tos=rgid0y; log_Id_pv=35
referer: https://blog.csdn.net/rank/list
sec-ch-ua: "Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47
'''

# modify 这里修改自己关注的文章关键字
my_favorite_type = '''
卷积
深度学习
机器视觉
opencv
android
java
'''

# modify 这里修改每页获取多少个文章
url = 'https://blog.csdn.net/phoenix/web/blog/hot-rank?page=0&pageSize=50&type='


def chromeHeaderFormat(chrome_header):
    header_param_list = chrome_header.split('\n')
    header_dict = '{'
    for i in header_param_list:
        if i != '':
            param_key = i.split(': ')[0]
            param_value = i.split(': ')[1]
            if ':' in param_key:
                param_key = param_key.replace(':', '')
            t = '"' + param_key + '":'
            one_line = t + '"' + param_value.replace('"', '\\"') + '",'
            header_dict += one_line
    header_dict = header_dict[:-1]
    header_dict += '}'

    header_dict = eval(header_dict)
    return header_dict


headers = chromeHeaderFormat(chrome_header)

response = requests.get(url=url, params='', headers=headers).json()

rank_data = response['data']

class Article:

    def __init__(self, period, avatarUrl, nickName, articleTitle,
                 articleDetailUrl, picList):
        self.period = period
        self.avatarUrl = avatarUrl
        self.nickName = nickName
        self.articleTitle = articleTitle
        self.articleDetailUrl = articleDetailUrl
        self.picList = picList

rank_article_list = []

# 遍历排行榜
for i in rank_data:
    period = i['period']
    nickName = i['nickName']
    avatarUrl = i['avatarUrl']
    articleTitle = i['articleTitle']
    articleDetailUrl = i['articleDetailUrl']
    picList = i['picList']
    article = Article(period, avatarUrl, nickName, articleTitle,
                      articleDetailUrl, picList)
    rank_article_list.append(article)

# 获取自己关注的文章

def getMyFocusArticle(my_favorite_type, article_list):
    count = 0
    for i in article_list:
        if any(type in i.articleTitle.lower() for type in my_favorite_type):
            count += 1
            print("***************************")
            print("文章标题:", i.articleTitle)
            print("作者头像:", i.avatarUrl)
            print("作者昵称:", i.nickName)
            print("文章地址:", i.articleDetailUrl)
            print("封面图片:", i.picList)
            print("***************************")
    print('共', count, '篇我关注的文章')


getMyFocusArticle(my_favorite_type.split('\n')[1:-1], rank_article_list)

import time
import requests

# modify 请求头，这是是从chrome直接复制过来的，代码会自动格式化，请求头建议换成自己的
chrome_header = '''
:authority: blog.csdn.net
:method: GET
:path: /phoenix/web/blog/hot-rank?page=0&pageSize=25&type=
:scheme: https
accept: application/json, text/plain, */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5
cookie: uuid_tt_dd=10_18796429750-1658977927448-465913; c_adb=1; UN=qq_34598061; BT=1658978250138; p_uid=U010000; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_18796429750-1658977927448-465913!5744*1*qq_34598061; ssxmod_itna=QqGxBDRQYCqWqGKG=DXGG7AHEuDRho2gGx+80iqGXd53DZDiqAPGhDC+8KRGG4hD+rK7A8nD=zDRSDxF31bl+3hflheiTD4q07Db4GkDAqiOD7wb3Dx1q0rD74irDDxD3fxD5zumx0Rll9wjg0S+VDBolYqQBIq4DCg4Dbrp9DB=dxBQ/IdQUznUDgTRsGG3TlxhWCGpxUBqYY7DoQhh5ApDYGDoeU7DYWRqNBrq3loq4DDfxCxx=eD=; ssxmod_itna2=QqGxBDRQYCqWqGKG=DXGG7AHEuDRho2gGx+80DA6nd4o4D/8XQDFx+7AUZaUKApdMm00yNYqhrA9RdPH/q2U+VnZurRwDrSe9c6O6Z6LF6kl3x78RFg32LajmrF1fHKf6HN86xqWRWsVcmzboeOEo5aEgKCZppi=ODGK/KhmPObH/ntSpOHiomsDzYezDAmWImh96WTQm4DwhitiYubzBGWq00bntG6HYWUM9k=KYxDLxG7eYD==; c_dl_um=-; c_segment=9; dc_sid=7d59a3117eb767df5dbb4a3f335ed0c7; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1658977929,1659538304,1659962559; c_dl_fref=https://blog.csdn.net/m0_46607117/article/details/124209280; c_dl_fpage=/download/weixin_42122988/19111107; c_dl_prid=1660133186668_691745; c_dl_rid=1660133187783_241806; dc_session_id=10_1660315971060.918825; csrfToken=4a5LP-oebPYwwJsk8d4WhtWO; c_first_ref=default; SESSION=eed18c25-b71d-4d27-9190-02f6d1349576; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22qq_34598061%22%2C%22scope%22%3A1%7D%7D; hide_login=1; c_pref=default; firstDie=1; c_first_page=https%3A//blog.csdn.net/qq598535550/article/details/51287630; c_dsid=11_1660317250975.902121; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1660317256; unlogin_scroll_step=1660317259022; log_Id_view=102; log_Id_click=48; c_ref=https%3A//blog.csdn.net/rank/list; c_page_id=default; dc_tos=rgid0y; log_Id_pv=35
referer: https://blog.csdn.net/rank/list
sec-ch-ua: "Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47
'''

# modify 这里修改自己关注的文章关键字
my_favorite_type = '''
卷积
深度学习
机器视觉
opencv
android
java
'''

# modify 这里修改每页获取多少个文章
url = 'https://blog.csdn.net/phoenix/web/blog/hot-rank?page=0&pageSize=50&type='


def chromeHeaderFormat(chrome_header):
    header_param_list = chrome_header.split('\n')
    header_dict = '{'
    for i in header_param_list:
        if i != '':
            param_key = i.split(': ')[0]
            param_value = i.split(': ')[1]
            if ':' in param_key:
                param_key = param_key.replace(':', '')
            t = '"' + param_key + '":'
            one_line = t + '"' + param_value.replace('"', '\\"') + '",'
            header_dict += one_line
    header_dict = header_dict[:-1]
    header_dict += '}'

    header_dict = eval(header_dict)
    return header_dict


headers = chromeHeaderFormat(chrome_header)

response = requests.get(url=url, params='', headers=headers).json()

rank_data = response['data']

class Article:

    def __init__(self, period, avatarUrl, nickName, articleTitle,
                 articleDetailUrl, picList):
        self.period = period
        self.avatarUrl = avatarUrl
        self.nickName = nickName
        self.articleTitle = articleTitle
        self.articleDetailUrl = articleDetailUrl
        self.picList = picList

rank_article_list = []

# 遍历排行榜
for i in rank_data:
    period = i['period']
    nickName = i['nickName']
    avatarUrl = i['avatarUrl']
    articleTitle = i['articleTitle']
    articleDetailUrl = i['articleDetailUrl']
    picList = i['picList']
    article = Article(period, avatarUrl, nickName, articleTitle,
                      articleDetailUrl, picList)
    rank_article_list.append(article)

# 获取自己关注的文章

def getMyFocusArticle(my_favorite_type, article_list):
    count = 0
    for i in article_list:
        if any(type in i.articleTitle.lower() for type in my_favorite_type):
            count += 1
            print("***************************")
            print("文章标题:", i.articleTitle)
            print("作者头像:", i.avatarUrl)
            print("作者昵称:", i.nickName)
            print("文章地址:", i.articleDetailUrl)
            print("封面图片:", i.picList)
            print("***************************")
    print('共', count, '篇我关注的文章')


getMyFocusArticle(my_favorite_type.split('\n')[1:-1], rank_article_list)
