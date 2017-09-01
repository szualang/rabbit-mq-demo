#!/usr/bin/env python
#coding:utf-8
import pika,time

credentials = pika.PlainCredentials('admin', 'admin')
#链接rabbit服务器（localhost是本机，如果是其他服务器请修改为ip地址）
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='192.168.1.210', port=5672, credentials=credentials, virtual_host='/'))
channel = connection.channel()


channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(" [x] 发送消息：  当前时间是： %s" % now)
connection.close()
