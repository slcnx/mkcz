#!/usr/bin/python3
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import json
import  time,os

def get_names():
  # get all processes name
  p1 = Popen(["ss","-tanp"], stdout=PIPE)
  p2 = Popen(["grep", "-Po", "(?<=users:\(\(\")[\w-]+"], stdin=p1.stdout, stdout=PIPE)
  raw_data = Popen(["sort","-u"], stdin=p2.stdout, stdout=PIPE)
  allProcesses = raw_data.communicate()[0].decode().split()
  return allProcesses


def create_record(process,type_,value):
  record = {}
  record['metric'] = 'custom'
  record['endpoint'] = os.uname()[1]
  record['tags'] = "process=%s,tag=%s" % (process,type_)
  record['value'] = value.strip()
  record['timestamp'] = int(time.time())
  record['counterType'] = 'GAUGE'
  record['step'] = 60
  data.append(record)

# nginx
def fetch_process_info(process):
  p1 = Popen(["ps", "axu"], stdout=PIPE)
  p2 = Popen(["grep", process], stdin=p1.stdout, stdout=PIPE)
  p3 = Popen(["grep","-v", "grep"], stdin=p2.stdout, stdout=PIPE)
  cpu = Popen(["awk","{sum+=$3}END{print sum}"], stdin=p3.stdout, stdout=PIPE)
  p1 = Popen(["ps", "axu"], stdout=PIPE)
  p2 = Popen(["grep", process], stdin=p1.stdout, stdout=PIPE)
  p3 = Popen(["grep","-v", "grep"], stdin=p2.stdout, stdout=PIPE)
  mem = Popen(["awk","{sum+=$4}END{print sum}"], stdin=p3.stdout, stdout=PIPE)
  cpupercent = cpu.communicate()[0].decode()
  mempercent = mem.communicate()[0].decode()
  create_record(process,'cpupercent',cpupercent)
  create_record(process,'mempercent',mempercent)

if __name__ == "__main__":
  data = []
  for process in get_names():
    fetch_process_info(process) 
  print(json.dumps(data))
