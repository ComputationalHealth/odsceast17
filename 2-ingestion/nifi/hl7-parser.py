from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback
import json

class PyStreamCallback(StreamCallback):
	def __init__(self):
		pass
	def process(self, inputStream, outputStream):
		hl7_msg = IOUtils.toString(inputStream, StandardCharsets.UTF_8)

		hl7_list = []

		hl7 = {}
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

		for msg in hl7_list:
			outputStream.write(bytearray(json.dumps(hl7_list, indent=4).encode('utf-8'))) 

flowFile = session.get()
if (flowFile != None):
	flowFile = session.write(flowFile,PyStreamCallback())
	session.transfer(flowFile, REL_SUCCESS)