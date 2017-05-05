from kafka import KafkaConsumer
import hdfs

hdfs_client = hdfs.Config().get_client()
kafka_client = KafkaConsumer("test1", bootstrap_servers="sandbox.hortonworks.com:6667")

i = 0
file = 0
queue = []

for msg in kafka_client:
	i = i + 1

	queue.append(msg.value)
	
	if i % 1000 == 0:
		with hdfs_client.write("/labdata/kafka/test_" + str(file) + ".hl7") as writer:
			for cur in queue:
				hl7 = {}
				hl7_list = []

				for seg in hl7_msg.split('\n'):
					fields = seg.split('|')
					if fields[0] == 'MSH':
						hl7['msh_ts'] = fields[6]
					if fields[0] == 'OBX':
						hl7['component'] = fields[3]
						hl7['value'] = fields[5]
						hl7['unit'] = fields[6]
						hl7['result_ts'] = fields[14]
						hl7['method'] = fields[18]

						hl7_list.append(hl7.copy())
					if fields[0] == 'OBR':
						hl7['req_ts'] = fields[6]
						hl7['obr_ts'] = fields[8]
				
				for cur_hl7 in hl7_list:
					cur_line = [cur_hl7['msh_ts'], cur_hl7['req_ts'], cur_hl7['obr_ts'], cur_hl7['component'], cur_hl7['value'], cur_hl7['unit'], cur_hl7['result_ts'], cur_hl7['method']]
					writer.write(','.join(cur_line) + '\n')

		file = file + 1
		queue = []