from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
from jinja2 import Template
import yaml
import sys

junos_hosts = ['vMX-1','vMX-2']
for host in junos_hosts:
	try:
		myFile = host + '.yml'
		with open(myFile,'r') as fh:
			data = yaml.load(fh.read())
		with open('case1.j2','r') as t_fh:
			t_format = t_fh.read()

		template = Template(t_format)
		myConfig = template.render(data)

		dev = Device(host=host, user='lab', password='lab123')
		dev.open()
		config = Config(dev)
		config.clock()
		config.load(myConfig, merge=True, format="text")
		config.pdiff()
		config.commit()
		dev.close()
	except LockError as e:
		print ("The config database was locked!")
	except ConnecTimeoutError as e:
		print ("Connection timed out!")