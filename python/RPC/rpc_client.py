#!/usr/bin/env python
#coding:utf-8
import pika
import uuid

class FibonacciRpcClient(object):
    def __init__(self):

        credentials = pika.PlainCredentials('admin', 'admin')
        # 链接rabbit服务器（localhost是本机，如果是其他服务器请修改为ip地址）

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='192.168.1.210', port=5672, credentials=credentials, virtual_host='/'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

print(" [x] 请求计算： fib(30)")
response = fibonacci_rpc.call(30)
print(" [.] 服务端返回： %r" % response)
