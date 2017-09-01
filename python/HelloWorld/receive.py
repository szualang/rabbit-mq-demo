#!/usr/bin/env python
#coding:utf-8
import pika,time

credentials = pika.PlainCredentials('admin', 'admin')
#链接rabbit服务器（localhost是本机，如果是其他服务器请修改为ip地址）
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='192.168.1.210', port=5672, credentials=credentials, virtual_host='/'))
channel = connection.channel()


channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(" [x] 接收消息： %r - %s" % (body,now) )

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] 等待消息... 结束请按 CTRL+C')
channel.start_consuming()
