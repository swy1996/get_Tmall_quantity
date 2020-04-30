import json
import requests
from datetime import datetime
import time

config_file_name = "data.json"
load_config = {}
all_forwait_time = 8
one_wait_time = 0.3

def get_data(data,index):
    try:
        response = requests.get(
            url="https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/",
            params = {
                "type": "jsonp",
                "data": data, #商品id
            },
            headers={
                "Host": "h5api.m.taobao.com",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Mobile Safari/537.36",
                "Sec-Fetch-Dest": "script",
                "Accept": "*/*",
                "Sec-Fetch-Site": "cross-site",
                "Sec-Fetch-Mode": "no-cors",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Accept-Encoding": "gzip",
            },
        )
        # print(response.content)
        if response.status_code!=200:
            print("错误处理")
            # 错误处理
        elif response.status_code == 200 and response.content:
            try:
                if json.loads(response.content.decode())['ret'][0]=="SUCCESS::调用成功":
                    global load_config
                    #判断库存增加的数量超过500通知
                    if load_config['id_list'][index]['shangci_kucun'] and float(json.loads(json.loads(response.content.decode())['data']['apiStack'][0]['value'])['skuCore']['sku2info']['0']['quantity'])-float(load_config['id_list'][index]['shangci_kucun']) > load_config['kucun_add_count_msg']:
                        is_buy = "库存增加了" + str(float(json.loads(json.loads(response.content.decode())['data']['apiStack'][0]['value'])['skuCore']['sku2info']['0']['quantity'])-float(load_config['id_list'][index]['shangci_kucun']))
                        title = json.loads(response.content.decode())['data']['item']['title']
                        img_url = "http:" + json.loads(response.content.decode())['data']['item']['images'][0]
                        print(title + "    " + is_buy)
                        # tongzhi(title + is_buy, data, img_url)
                    # 判断库存的数量超过500通知
                    if float(json.loads(json.loads(response.content.decode())['data']['apiStack'][0]['value'])['skuCore']['sku2info']['0']['quantity']) > load_config['kucun_all_count_msg'] and load_config['id_list'][index]['msg_kucun']=="true":
                        is_buy = "库存="+str(json.loads(json.loads(response.content.decode())['data']['apiStack'][0]['value'])['skuCore']['sku2info']['0']['quantity'])
                        title = json.loads(response.content.decode())['data']['item']['title']
                        img_url = "http:" + json.loads(response.content.decode())['data']['item']['images'][0]
                        print(title + "    " + is_buy)
                        # tongzhi(title + is_buy, data, img_url)
                    # 商品上架通知
                    if json.loads(json.loads(response.content.decode())['data']['apiStack'][0]['value'])['trade']['buyEnable']=='true':
                        is_buy = "已上架"
                        title = json.loads(response.content.decode())['data']['item']['title']
                        img_url = "http:" + json.loads(response.content.decode())['data']['item']['images'][0]
                        print(title + "    " +is_buy+ "    " +'库存' + json.loads(json.loads(response.content.decode())['data']['apiStack'][0]['value'])['skuCore']['sku2info']['0']['quantity'])
                        # tongzhi(title + is_buy, data, img_url)
                    # 商品未上架
                    elif json.loads(json.loads(response.content.decode())['data']['apiStack'][0]['value'])['trade']['buyEnable']=='false':
                        is_buy = "未上架"
                        title = json.loads(response.content.decode())['data']['item']['title']
                        print(title + "    " +is_buy+ "    " +'库存' + json.loads(json.loads(response.content.decode())['data']['apiStack'][0]['value'])['skuCore']['sku2info']['0']['quantity'])
                    else:
                        print("调用成功但未状态")

                    if json.loads(response.content.decode())['data']['apiStack'] and json.loads(json.loads(response.content.decode())['data']['apiStack'][0]['value'])['skuCore']['sku2info']['0']['quantity']:
                        load_config['id_list'][index]['shangci_kucun'] = json.loads(json.loads(response.content.decode())['data']['apiStack'][0]['value'])['skuCore']['sku2info']['0']['quantity']
            except:
                print('调用失败')
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def read_config():
    try:
        with open(config_file_name, 'rb') as f:
            global load_config
            load_config = json.load(f)
            global one_wait_time
            one_wait_time = load_config["one_wait_time"]
            load_config["get_count"] = load_config["get_count"]+1
            load_config["last_time"] = '刷新时间：' + datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    except:
        print("第二阶段读取配置错误,请检查配置文件！")
    for index,i in enumerate(load_config["id_list"]):
        if load_config["id_list"][index]["status"] == "true":
            get_data("{\"itemNumId\":\"" + i["id"] + "\"}",index)
            time.sleep(one_wait_time)
    write_config()

def write_config():
    try:
        with open(config_file_name, 'w',encoding='utf-8') as f:
            json.dump(load_config, f, indent=1,ensure_ascii=False)
            print("更新文件完成...")
    except:
        print("更新文件错误,请检查！")

def tongzhi(info,data,img_url):
    for i in load_config["dd_send_msg_url_list"]:
        dd_data = {
            "msgtype": "link",
            "link": {
                "text": info,
                "title": info,
                "picUrl": img_url,
                "messageUrl": "https://detail.m.tmall.com/item.htm?id=" + json.loads(data)['itemNumId']
            }
        }
        res_data = requests.post(i, json=dd_data)
        print(res_data.text)

def timer(n):
    while True:
        print('\n'+'刷新时间：'+datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
        read_config()
        time.sleep(n)

if __name__ == '__main__':
    try:
        with open(config_file_name, 'r',encoding='utf-8') as f:
            load_config = json.load(f)
            all_forwait_time = load_config["all_forwait_time"]
            timer(all_forwait_time)
    except:
        print("第一阶段读取配置错误,请检查配置文件！")






