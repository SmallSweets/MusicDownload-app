import requests
import re
import json
import os
import urllib.request,urllib.error,urllib.parse

headers = {"cookie": "kg_mid=4b42424f9fa4d173c4601c6b476003f2; kg_dfid=2AHvg428HZSx0oRNWX0prTMo; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1587913892,1588084386; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; kg_mid_temp=4b42424f9fa4d173c4601c6b476003f2; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1588093697",
           "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}

list_num = -1
show_music_info_list = []
search_music_url_all = []


def music_get_url(name,page):
    content_url_list = []
    code_name = urllib.parse.quote(name)  #字符串转化为编码格式
    music_list = "https://songsearch.kugou.com/song_search_v2?callback=jQuery112405886208845288214_1588464073802&keyword={}&page={}&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1588464073804".format(code_name,page) #获取歌名产生的歌曲列表 下载列表全部
    music_list_response = requests.get(music_list,headers=headers,).text
    music_list_html = re.findall(r'\((.*)\)',music_list_response)[0]
    music_list_html_dict = json.loads(music_list_html)
    # print(music_list_html_dict["data"]["lists"])
    for i in range(len(music_list_html_dict["data"]["lists"])):
        music_hash = music_list_html_dict["data"]["lists"][i]["FileHash"]  #关键字 hash
        music_albumid = music_list_html_dict["data"]["lists"][i]["AlbumID"]  #关键字album_id
        information_url = "https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery19101144344902676131_1588093696865&hash={}&album_id={}&dfid=2AHvg428HZSx0oRNWX0prTMo&mid=4b42424f9fa4d173c4601c6b476003f2&platid=4&_=1588093696867".format(music_hash,music_albumid)
        content_url_list.append(information_url)  #包含歌曲详细信息
        search_music_url_all.append(information_url)
    return content_url_list


def out_music_list(sid,list_num):
    url = sid
    response = requests.get(url, headers=headers).text
    cut_json = re.findall(r'\((.*)\)', response)[0]  # 格式为json格式
    cut_dict = json.loads(cut_json)  # 转换为字典格式 才能根据键获取值
    music_name = cut_dict["data"]["song_name"]  # 歌曲名
    singer = cut_dict["data"]["author_name"]  # 歌手名
    show_music_info = str(list_num)+ "  "+music_name+"---"+singer
    show_music_info_list.append(show_music_info)

def Preservation(sid,download_context):
    url = sid
    response = requests.get(url,headers=headers).text
    cut_json = re.findall(r'\((.*)\)',response)[0]  #格式为json格式
    cut_dict = json.loads(cut_json)  #转换为字典格式 才能根据键获取值
    music_url = cut_dict["data"]["play_url"]  #歌曲播放地址
    music_name = cut_dict["data"]["song_name"]  #歌曲名
    singer = cut_dict["data"]["author_name"]  #歌手名
    data_url = download_context
    data_name = data_url + music_name + "---" + singer + ".mp3"
    content_url = requests.get(music_url,headers=headers).content
    try:
        if not os.path.exists(data_url):  #判断有误文件夹
            os.mkdir(data_url)
        if not os.path.exists(data_name):  #判断有无文件
            with open(data_name,"wb") as f:
                f.write(content_url)
            return "%s 下载成功" % (music_name + "---" + singer)
        else:
            return "文件已存在"
    except:
        return "下载失败"

def out(list,start):
    list_num = start
    for sid in list:  # 当没有版权时是没有play_url的 这部分要修改
        list_num += 1
        out_music_list(sid,list_num)


def main(user_input):
    global infor_music_list
    next = "0"
    while next != "1":
        download_name = user_input
        page = "1"
        while page != "0":
            infor_music_list = music_get_url(download_name,page)
            page = input("默认为第一页,翻页请输入页数,继续请输入0:")
        context = input("请输入下载目录(默认为D:/)不输入则设定为默认:")
        if context:
            download_context = context
        else:
            download_context = "D:/"
        download_num = []
        decide_num = input("请输入歌曲的序号(多个序号请用空格分隔):")
        download_num.append(decide_num)
        if len(download_num[0]) > 1:
            download_num = download_num[0].split(" ")
        else:
            download_num = download_num

        for sid in download_num:
            sid = int(sid)
            sid = infor_music_list[sid]
            Preservation(sid,download_context)
        next = input("继续下载请输入0,退出请输入1:")

if __name__ == '__main__':
    kk = []
    for i in range(1,3):
        kk = music_get_url("有点甜",i)
        print(len(kk))
    out(kk)
    print(show_music_info_list)