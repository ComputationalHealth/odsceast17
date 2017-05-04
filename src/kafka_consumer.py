import csv

from kafka import KafkaConsumer

KAFKA_BROKERS = "192.168.99.100:6667"
KAFKA_TOPIC = "default-test"

# hdfs_client = hdfs.Config().get_client()
kafka_client  = KafkaConsumer(KAFKA_TOPIC,
						 bootstrap_servers=KAFKA_BROKERS,
                         auto_offset_reset='earliest')

data = {}
data['messages'] = []

hl7 = {
	'msg_ts':str(),
	'coll_ts':str(),
	'order_ts':str(),
	'result_ts':str(),
	'component':str(),
	'value':str(),
	'unit':str(),
	'method':str()
}

i = 0
file = 0
queue = []

for msg in kafka_client :
    
    i = i + 1
    queue.append(msg.value)

    hl7 = {}
    segments = msg.value.split('\n')

    for seg in segments:
        fields = seg.split('|')
        if fields[0] == 'MSH':
            hl7['msg_ts'] = fields[6]
        if fields[0] == 'OBX':
            hl7['component'] = fields[3]
            hl7['value'] = fields[5]
            hl7['unit'] = fields[6]
            hl7['result_ts'] = fields[14]
            hl7['method'] = fields[18]
        if fields[0] == 'OBR':
            hl7['order_ts'] = fields[6]
            hl7['coll_ts'] = fields[8]


    data['messages'].append(hl7)
    keys = hl7.keys()
    with open('test.csv', 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data['messages'])

    if i % 100 == 0:
		with hdfs_client.write("/tmp/test_" + str(file) + ".hl7") as writer:
			for cur in queue:
				writer.write(cur)

		file = file + 1
		queue = []