# :robot: 微信订阅机器人

## :fish: 微信订阅机器人之闲鱼二手商品监控
### :hammer:技术栈及库:
* python3
* itchat & wxpy
* flask
* flask-mail
* Mysql + MongoDB + Redis
* sqlachemy + mongoengine
* Celery
* Requests

#### 细节
##### 四个部分: 爬虫 | 交互式微信机器人 | 微信机器人web接口 | 推送
- 爬虫
    > 实时爬取闲鱼商品存入Mysql数据库
- 交互式微信机器人
    > 自动通过好友，好友订阅爬虫，将好友和需求存入MongoDB
- 微信机器人web接口
    > 微信机器人服务接口，主要为推送提供API
- 推送
    > 轮询Mysql商品数据库, 根据MongoDB中的数据做分类后请求API将信息推送至微信好友(订阅者)
##### 流程
- 启动web服务 -> 启动Celery队列任务 

- Celery 启动发出信号将下面四个任务跑起来
    * 爬虫运行
    * 交互式微信机器人运行
    * 更新MongoDB中的微信好友数据
    * 推送服务运行

##### 微信机器人登录
方法一: 
> 服务运行起则会请求登录, 使用 itchat 的回调，调用celery被动任务中的邮件服务，将二维码发送至自己的邮箱然后扫码登录。

方法二:
> 请求/login这个登录接口获取二维码扫码登录

📌 TODO:
- 爬虫:
    * 商品去重
- 推送:
    * 商品推送至对应的订阅者
- 交互式微信机器人:
    * 丰富的交互
- 登录:
    控制邮件频率间隔 | 实现方法二

### LICENSE
>MIT License
>Copyright (c) 2019 

> 仅作为学习与交流的项目.