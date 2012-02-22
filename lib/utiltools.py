#!/usr/bin/python
"""Default python script layout."""

import glob
import os
import subprocess
import matplotlib.pyplot as plt

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2012"
__credits__ =  ""
__license__ = "GPL"
__version__ = "0.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

class UserAccount(object):
	def __init__(self):
		self._Name = ""
		self._infoDict = {}

class DiskObj(object):

	def __init__(self):
		self._Name = ""
		self._infoDict = {}

	def printInfo(self):
		for keys in self._infoDict.keys():
			print "%s: %s" % (keys, self._infoDict[keys])

	def getUsers(self):

		if self._infoDict["Filesystem"] == "none":
			return []
		diskname = self._infoDict["Mounted"]
		users = os.listdir("%s/%s" % (diskname, "home"))
                toRemove = {"G": 1.0, "M":1.0e-3, "%": 1.0, "K": 1.0e-6, "T": 1e3}

		userList = []

		for user in users:
			newUser = UserAccount()
			
			cmd = ["du", "-h", "%s/%s/%s" % (diskname, "home", user)]
			du = subprocess.Popen(cmd, stdout=subprocess.PIPE)
			du_content = du.communicate()[0]
			du_content = [i for i in du_content.replace("\t"," ").replace("\n"," ").split(" ")]
			du_content = du_content[-3]

			for i in du_content:
				try:
					if i in toRemove:
						dd = float(du_content.replace(i, "")) * toRemove[i]
				except:
					x = None

			newUser._infoDict["user"] = user
			newUser._infoDict["size"] = dd

			userList.append(newUser)

		return userList

	def writeLog(self, logfile="user.log"):
		logfile = open(logfile, "a+w")
		users = self.getUsers()
		
		if not users:
			return 0

		for user in users:
			tmpDict = user._infoDict
			# user size
			logfile.write("%s %s\n" % (tmpDict["user"], tmpDict["size"]))
		logfile.write("#\n")
		logfile.close()

	def readLog(self, logfile="user.log"):

		try:
			logfile = open(logfile, "r")
			logline = logfile.readlines()
			logfile.close()
		except:
			return 0

		logList = []
		t = 0
		for log in logline:
			tmpLog = log.replace("\n", "")
			if tmpLog != "#":
				newUser = UserAccount()
				tmpLog = [i for i in tmpLog.split(" ")]
				newUser._infoDict["user"] = tmpLog[0]
				newUser._infoDict["size"] = tmpLog[1]
				newUser._infoDict["Time"] = t
				logList.append(newUser)
			else:
				t += 1

		return logList
	
	def plotHistory(self):

		timeUser = self.readLog()
		if not timeUser:
			print "No user"
			return 0

		# Figure
		fig = plt.figure(0)
		ax1 = fig.add_subplot(311)

		users = self.getUsers()
		for user in users:
			Name = user._infoDict["user"]
			print "Name:", Name
			if Name == "none":
				continue

			size, time = [], []
			
			for tuser in timeUser:
				print "tuser:", tuser._infoDict["user"]

				if tuser._infoDict["user"] == Name:

					tt = tuser._infoDict["Time"]
					aa = tuser._infoDict["size"]

					time.append(float(tt))
					size.append(float(aa))

			ax1.plot(time, size, label=Name)
		
		ax1.set_title(self._infoDict["Mounted"])
		ax1.set_xlabel("time -t0 [days]")
		ax1.set_ylabel("Size [GB]")
		ax1.legend(loc=4)

#	plt.show()
		plt.savefig("user.png", format="png")

class DiskDatabase(object):

	def __init__(self):
		self._Name = None
		self._Disks = self.collectDisks()

	def collectDisks(self):
		# Obtain df -h
		cmd = ["df", "-h"]
		df = subprocess.Popen(cmd, stdout=subprocess.PIPE)
		df_content = df.communicate()[0]
		df_content = [i for i in df_content.split("\n") if i]

		# Parse
		# Filesystem            Size  Used Avail Use% Mounted on
		header = [i for i in df_content[0].split(" ") if i]
		diskList = []
		headerlen = len(header)-1

		for disk in df_content[1:]:

			newDisk = DiskObj()
			diskcontent = [i for i in disk.split(" ") if i]
			
			for i in range(headerlen):
				head = header[i]
				content = diskcontent[i]
				newDisk._Name = "TEST"
				newDisk._infoDict[head] = content

			diskList.append(newDisk)

		return diskList

	def printInfo(self):
		for disk in self._Disks:
			disk.printInfo()
			print ""

	def writeLog(self, logfile="disk.log"):
		logfile = open(logfile, "a+w")
		for disk in self._Disks:
			tmpDict = disk._infoDict
			# Filesystem            Size  Used Avail Use% Mounted on
			logfile.write("%s %s %s %s %s %s\n" % (tmpDict["Filesystem"], tmpDict["Size"], tmpDict["Used"], tmpDict["Avail"], tmpDict["Use%"], tmpDict["Mounted"]))
		logfile.write("#\n")
		logfile.close()

	def readLog(self, logfile="disk.log"):
		logfile = open(logfile, "r")
		logline = logfile.readlines()
		logfile.close()


		logList = []
		t = 0
		for log in logline:
			tmpLog = log.replace("\n", "")
			if tmpLog != "#":
				newDisk = DiskObj()
				tmpLog = [i for i in tmpLog.split(" ")]
				newDisk._infoDict["Filesystem"] = tmpLog[0]
				newDisk._infoDict["Size"] = tmpLog[1]
				newDisk._infoDict["Used"] = tmpLog[2]
				newDisk._infoDict["Avail"] = tmpLog[3]
				newDisk._infoDict["Use%"] = tmpLog[4]
				newDisk._infoDict["Mounted"] = tmpLog[5]
				newDisk._infoDict["Time"] = t
				logList.append(newDisk)
			else:
				t += 1

		return logList

	def plotHistory(self):

		timeDisk = self.readLog()

		# Figure
		fig = plt.figure(0)
		ax1 = fig.add_subplot(311)
		ax2 = fig.add_subplot(312)
		ax3 = fig.add_subplot(313)

		for disk in self._Disks:
			Name = disk._infoDict["Filesystem"]
			print "Name:", Name
			if Name == "none":
				continue

			used, avail, usage, time = [], [], [], []
			
			for tdisk in timeDisk:
				print "tdisk:", tdisk._infoDict["Filesystem"]

				if tdisk._infoDict["Filesystem"] == Name:

					toRemove = {"G": 1.0, "M":1.0e-3, "%": 1.0, "K": 1.0e-6, "T": 1e3}
					tt = tdisk._infoDict["Time"]
					aa = tdisk._infoDict["Avail"]
					uu = tdisk._infoDict["Used"]
					usus = tdisk._infoDict["Use%"]

					for i in toRemove:
						try:
							if i in aa:
								aa = float(aa.replace(i,"")) * toRemove[i]
						except:
							x = None

						try:
							if i in uu:
								uu = float(uu.replace(i,"")) * toRemove[i]
						except:
							x = None

						try:
							if i in usus:
								usus = float(usus.replace(i,"")) * toRemove[i]
						except:
							x = None

					time.append(float(tt))
					avail.append(float(aa))
					used.append(float(uu))
					usage.append(float(usus))

			ax1.plot(time, usage, label=Name)
			ax2.plot(time, used, label=Name)
			ax3.plot(time, avail, label=Name)
		
		ax1.set_title("Usage")
		ax1.set_xlabel("time -t0 [days]")
		ax1.set_ylabel("%")
	
		ax2.set_title("Used")
		ax2.set_xlabel("time - t0 [days]")
		ax2.set_ylabel("Size [GB]")

                ax3.set_title("Available")
                ax3.set_xlabel("time -t0 [days]")
                ax3.set_ylabel("Size [GB]")

		ax1.legend(loc=4)
		ax2.legend(loc=4)
		ax3.legend(loc=4)
		plt.savefig("disk.png", format="png")



def main():

	MyComp = DiskDatabase()
	MyComp.collectDisks()
	for Disk in MyComp._Disks:
		Disk.writeLog()
		Disk.plotHistory()

if __name__ == "__main__":
	main()
# Tue Feb 21 23:20:18 CLST 2012
