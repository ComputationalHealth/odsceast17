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

	if i % 100 == 0:
		with hdfs_client.write("/tmp/test_" + str(file) + ".hl7") as writer:
			for cur in queue:
				writer.write(cur)

		file = file + 1
		queue = []