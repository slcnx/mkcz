# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import time
import json
import os

iot_dict = {
	"io.device-ms": ['5001', '6001'],
 	"iot.userdevice-ms": ['5002', '6002']
	} 

ports_list = ['5001', '6001']
def fetch_ss_state(k, port_list):
	count = 0
	# value: 0，端口不存在。1，端口存在。
	raw_data = Popen(["ss", "-tunl"], stdout=PIPE, stderr=PIPE).communicate()[0]
	for line in raw_data.splitlines():
	 	line = str(line)
		sub_item = ':' + port_list + ' '
		if sub_item in line:
			value = 1
			break
	else:
		value = 0

	create_record(k, port_list, value)	


def create_record(metric, port, value):
	record = {}
	record['metric'] = metric
	record['endpoint'] = os.uname()[1]
	record['tags'] = 'srv=iotdevice-ms,port=' + port
	record['value'] = value
	record['timestamp'] = int(time.time()) 
	record['counterType'] = 'GAUGE'
	record['step'] = 60
	data.append(record)

if __name__ == "__main__":
	data = []
	for k, v in iot_dict.items():
		for port_list in v:
			fetch_ss_state(k, port_list)

	print(json.dumps(data))
