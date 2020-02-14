# 查看天猫商品库存脚本

## [data.json](data.json) 配置文件
```json
{
 "#": "外层循环等待时间",
 "all_forwait_time": 2,
 "##": "循环内请求等待时间",
 "one_wait_time": 0.3,
 "###": "设定商品库存超过多少提醒",
 "kucun_all_count_msg": 499,
 "####": "设定商品库存比上次增加超过多少提醒",
 "kucun_add_count_msg": 499,
 "#####": "程序运行总次数",
 "get_count": 0,
 "######": "程序最后一次运行时间",
 "last_time": "刷新时间：2020-02-14  14:08:21",
 "#######": "遍历的商品列表",
 "id_list": [
  {
   "########": "商品id",
   "id": "550189462849",
   "#########": "是否通知库存提醒(true为提醒，不提醒false即可)",
   "msg_kucun": "true",
   "##########": "上次库存记录",
   "shangci_kucun": "26",
   "###########": "是否监控(true为监控，不监控false即可)",
   "status": "true"
  }
 ],
 "########": "通知地址，我这里使用的是钉钉机器人",
 "dd_send_msg_url_list": [
  "钉钉机器人webhook"
 ]
}
```

## [main.py](main.py)（程序运行）
```
python3 main.py
如果print打印不及时：
python3 -u main.py
```
 