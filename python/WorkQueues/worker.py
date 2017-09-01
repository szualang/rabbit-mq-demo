#!/usr/bin/env python
#coding:utf-8
import pika
import time

credentials = pika.PlainCredentials('admin', 'admin')
#链接rabbit服务器（localhost是本机，如果是其他服务器请修改为ip地址）
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='192.168.1.210', port=5672, credentials=credentials, virtual_host='/'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

print(' [*] 等待消息... 结束请按 CTRL+C')

def callback(ch, method, properties, body):
    print('')
    print(" [x] 接收消息： %r" % body )
    print(" [x] 开始执行任务，当前时间：%s " % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
    # 模拟长时间工作进程，进程停顿，根据传过来的.点号，停顿秒数
    time.sleep(body.count(b'.'))
    print( " [x] 任务执行完成！当前时间：%s " % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
    print('')
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()
