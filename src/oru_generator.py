#!/usr/bin/env python
import os
import time

import observation

from kafka import KafkaProducer


NEW_LINE = '\n'
SLEEP = 5
NUMBER_MESSAGES = 2

KAFKA_BROKERS = "192.168.99.100:6667"
KAFKA_TOPIC = "default-test"
# KAFKA_BROKERS = os.getenv("KAFKA_BROKERS", "localhost:6667")
# KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "default-test")

KafkaProducer = KafkaProducer(bootstrap_servers=KAFKA_BROKERS)

while 1:
    for _ in range(NUMBER_MESSAGES):
        obs = observation.Observation()

        msh = 'MSH|^~\&|||||{0}||ORU^R01|||||||'.format(
                    obs.msh_time)
        
        HL7_MESSAGE = msh

        obr = 'OBR||||{0}||{1}||{2}||||||||||{3}|||||||{4}||||'.format(
            obs.universal_service_id,
            obs.req_time,
            obs.obs_end_time,
            obs.method,
            obs.result_status)
        
        for k in obs.oru['components'].keys():
            obx_i = 'OBX|||{0}||{1}|{2}||||||||{3}||||{4}|'.format(
                        k,
                        obs.oru['components'][k]['value'],
                        obs.oru['components'][k]['unit'],
                        obs.obx_time,
                        obs.oru['method']
                        )
            obr = NEW_LINE.join([obr, obx_i])
            
        HL7_MESSAGE = NEW_LINE.join([HL7_MESSAGE, obr])

        # send HL7_MESSAGE to Kafka
        print (HL7_MESSAGE)
        KafkaProducer.send(KAFKA_TOPIC, HL7_MESSAGE)

    KafkaProducer.flush()
    time.sleep(SLEEP)
