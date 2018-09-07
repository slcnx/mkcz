#!/usr/bin/python3
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import time
import json
import os

iot_dict = {
    "iotdevice-ms": ["5001", "6001"],
    "iotuserdevice-ms": ["5002", "6002"],
    "iothouse-ms": ["5003", "6003"],
    "iotai-ms": ["5004", "6004"],
    "iotpublic-ms": ["5005", "6005"],
    "iotdata-ms": ["5006", "6006"],
    "iotauth-ms": ["5007", "6007"],
    "iotuser-ms": ["5008", "6008"],
    "iotdns-ms": ["5009", "6009"],
    "iotautoai-ms": ["5010", "6010"],
   "iotyos-ms": ["5011", "8081", "6011"],
    "iotevent-ms": ["5012", "6012"],
    "iotonline-ms": ["5013", "6013"],
    "iotpush-ms": ["5016", "6016"],
    "iotpay-ms": ["5017", "6017"],
    "iotdefense-ms": ["5018", "6018"],
    "iotacl-ms": ["5032", "6032"],
    "iotauthority-ms": ["5021", "6021"],
    "iotauthority-master": ["5022", "6022"],
    "datasync-master": ["5023", "6023"],
    "apigw-ms": ["443", "1443", "5025", "6025"],
    "iotgw-mq": ["1888", "1889"],
    "mini-mq": ["2888", "2889"],
    "yuemq-router": ["5888", "5889"],
    "yuemq-cnode": ["6888", "6889"],
    "local-mq": ["3888", "3889"],
    "yuemq-global": ["10888", "10889"],
    "iotconnnat-ms": ["2001", "3001"],
    "iotconnp2p-ms": ["5999", "6999"],
    "iotconnrelay-ms": ["5998", "6998"],
    "iotlog-ms": ["5024", "6024"],
    "iotorder-ms": ["5030", "6030"],
    "iotoss-ms": ["5026", "6026"],
    "iotidx-ms": ["5027", "6027"],
    "iotgoods-ms": ["5033", "6033"],
    "iotadmin-ms": ["5031", "8088", "6031"],
    "iotinfrared-ms": ["5034", "6034"],
    "iotmonitor-ms": ["5035", "6035"],
    "iotoauth2-ms": ["5036", "6036"],
    "iotalivoice-ms": ["5037", "6037"],
    "iotdingdauth-ms": ["5038", "6038"],
    "iotdingdvoice-ms": ["5039", "6039"],
    "iotawsvoice-ms": ["5040", "6040"],
    "iotggvoice-ms": ["5042", "6042"]
    }

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
    record['metric'] = 'iot-port'
    record['endpoint'] = os.uname()[1]
    record['tags'] = 'srv=' + metric + ',port=' + port
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
