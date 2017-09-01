#!/usr/bin/env python
#coding:utf-8
import pika, sys, time

credentials = pika.PlainCredentials('admin', 'admin')
#链接rabbit服务器（localhost是本机，如果是其他服务器请修改为ip地址）
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='192.168.1.210', port=5672, credentials=credentials, virtual_host='/') )
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
message = message + '  ' + time.strftime( "%H:%M:%S", time.localtime() )

channel.basic_publish( exchange='logs',
                      routing_key='',
                      body=message )
print( " [x] 发送消息： %r" % message )
connection.close()
