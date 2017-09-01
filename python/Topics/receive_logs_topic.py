#!/usr/bin/env python
#coding:utf-8
import pika
import sys


credentials = pika.PlainCredentials('admin', 'admin')
#链接rabbit服务器（localhost是本机，如果是其他服务器请修改为ip地址）
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='192.168.1.210', port=5672, credentials=credentials, virtual_host='/'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("使用说明: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs',
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] 等待日志输出，结束请按 CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
