import kafka

demo1_config = {
    'kafka_host': '9.134.75.180:9092',
    'kafka_topic': 'test'  # topic的名字由k8s的statefulset的id来决定
}

def consume():
    consumer = kafka.KafkaConsumer(demo1_config['kafka_topic'],
                                   bootstrap_servers=[demo1_config['kafka_host']],
                                   api_version=(3, 8, 1),
                                   group_id='my_consumer_group',  # 指定消费者组
                                   auto_offset_reset='earliest',)
    print('link kafka ok.')
    for message in consumer:
        print("topic = %s , partition = %d ,  offset = %d , value=%s" % (message.topic, message.partition, message.offset,message.value))
        consumer.commit()

if __name__ == '__main__':
    consume()