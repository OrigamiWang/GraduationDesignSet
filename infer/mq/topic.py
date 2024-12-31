import kafka

def list_all_topics():
    consumer = kafka.KafkaConsumer(bootstrap_servers=['9.134.75.180:9092'])
    return consumer.topics()


print(list_all_topics())