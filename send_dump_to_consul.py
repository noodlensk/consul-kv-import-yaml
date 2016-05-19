#!/usr/bin/env python
import sys, argparse, yaml, consul

parser = argparse.ArgumentParser(description='Params for consul')
parser.add_argument('file', metavar='file', type=str, help='Yaml file name')
parser.add_argument('host', metavar='host', type=str, nargs='?', help='Consul host name', default='consul.service.consul')
parser.add_argument('port', metavar='port', type=int, nargs='?', help='Consul port', default=8500)
args = parser.parse_args()


c = consul.Consul(args.host,args.port)

def parseData(d, key):
  for k, v in d.iteritems():
    if key != "":
      newkey = key + "/" + k
    else:
      newkey = key + k

    if isinstance(v, dict):
      parseData(v, newkey)
    else:
      if isinstance(v, bool):
        val = str(v).lower()
      elif isinstance(v, int):
        val = str(v)
      else:
        val = v
      print "{0} : {1}".format(newkey, val)
      c.kv.put(newkey, val)
with open(args.file, 'r') as stream:
    try:
        data = yaml.load(stream)
        parseData(data, "")
    except yaml.YAMLError as exc:
        print(exc)