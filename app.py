import requests
import re
import base64
import chardet
import urllib

url = 'http://a.nwctfw.com:9998'
search_url = url + '/sou.php?name='
download_url = url + '/find.php?name='

search_keyword = input("请输入关键词:")

headers = {
    "Connection": 'close',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3970.5 Safari/537.36"
}


def search_content(keyword):
    print('查询中...')
    context = requests.get(url=search_url + keyword,
                           headers=headers).content.decode('utf-8')
    return context


def download_content(txt_id):
    print('下载中....')
    context = requests.get(url=download_url + txt_id,
                           headers=headers, stream=True)
    print('下载完成')
    # context = base64.b64decode(requests.get(url=download_url + txt_id, headers=headers).content.decode())
    return context


search_data = search_content(search_keyword if search_keyword != '' else "小姨子")
reg = re.compile("\|wybsf\|.*?\|wybsf\||\|name\|.*?\|name\|")
res = reg.findall(search_data)
find_list = []

res_index = 0
for i in range(int(len(res) / 2)):
    find_list.append(res[res_index:res_index + 2])
    res_index += 2
if len(find_list) == 0:
    print('scx', 'c')
else:
    print(f'查找完毕,共查找到{len(res)}个内容')

for id in find_list:
    txt_name = id[0].replace('|name|', '')
    txt_id = id[1].replace('|wybsf|', '')
    download_data = download_content(txt_id)

    print('开始写入-----------')
    chunk_size = 1024  # 每次最大请求字节
    content_size = int(download_data.headers['content-length'])  # 获得本次请求的字节
    data_count = 0
    with open(txt_name + '.txt', 'wb') as file:
        # 一块一块以下载
        for data in download_data.iter_content(chunk_size=chunk_size):
            file.write(data)
            data_count = data_count + len(data)
            now = (data_count / content_size) * 100  # 计算下载的进度
            print(f"\r {txt_name}.txt 下载进度：%d%%(%d/%d)" %
                  (now, data_count, content_size), end=" ")

    print(f'{txt_name}写入完成---------')
