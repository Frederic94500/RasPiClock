from xmlrpc.server import SimpleXMLRPCServer

import os, sys

def rpc():
	with SimpleXMLRPCServer(('0.0.0.0', 8000)) as server:
		import psutil
		server.register_introspection_functions()

		class ComputerUsage:
			def cpu_usage(self):
				return psutil.cpu_percent()
			def ram_usage(self):
				return psutil.virtual_memory().percent

		server.register_instance(ComputerUsage())

		def computer_temp():
			if sys.platform == "win32": #Windows via OpenHardwareMonitor
				import wmi
				w = wmi.WMI(namespace="root\OpenHardwareMonitor")
				temperature_infos = w.Sensor()
				temp = []
				for sensor in temperature_infos:
					if sensor.SensorType==u'Temperature':
						if sensor.Name == "GPU Core" or sensor.Name == "CPU Package":
							temp.append(sensor.Value)
				return temp

			elif "armv7l" in os.uname(): #RPI
				temp = list(os.popen("vcgencmd measure_temp").readline())
				del temp[-3:-1]
				del temp[-1]
				del temp[0:5]
				temp = "".join(temp)
				return temp

			elif "x86_64" in os.uname():
				print("NA")

		server.register_function(computer_temp, "temperature")

		server.serve_forever()

if sys.platform == "linux":
	import daemon
	with daemon.DaemonContext():
		rpc()

elif sys.platform == "win32":
	rpc()

else:
	print("Je ne vous connais pas")
	sys.exit()