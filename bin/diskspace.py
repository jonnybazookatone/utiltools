#!/usr/bin/python
"""Default python script layout."""

import glob

from wikibot import wikiLib
from utiltools.lib import utiltools

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2012"
__credits__ =  ""
__license__ = "GPL"
__version__ = "0.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def main():

        Comp = utiltools.DiskDatabase()
        Comp.writeLog()
        Comp.plotHistory()
	for Disk in Comp._Disks:
		Disk.plotHistory()

	imgs = glob.glob("imgs/*.png")
	wikiLib.replaceImage(pagename="MachineStatus",image=imgs)

if __name__ == "__main__":
	main()
# Wed Feb 22 07:23:40 CET 2012
