import kafka

demo1_config = {
    'kafka_host': '9.134.75.180:9092',
    'kafka_topic': 'test'
}


def produce():
    producer = kafka.KafkaProducer(bootstrap_servers=[demo1_config['kafka_host']], api_version=(3, 8, 1))
    print('link kafka ok.')

    messages = [
        {'kkkk': 'vvvv'},
        ]

    for each_msg in messages:
        this_key = list(each_msg.keys())[0]
        this_val = each_msg[this_key]
        future = producer.send(demo1_config['kafka_topic'], key=this_key.encode('utf-8'),value=this_val.encode('utf-8'))
        print('produce: key={}, val={}'.format(this_key, this_val))
    producer.close()
    print('produce over.')

if __name__ == '__main__':
    produce()