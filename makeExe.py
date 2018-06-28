import sys
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Tools\Scripts')
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7')
import clr

clr.AddReference('IronPython')
clr.AddReference('IronPython.Modules')
clr.AddReference('Microsoft.Scripting.Metadata')
clr.AddReference('Microsoft.Scripting')
clr.AddReference('Microsoft.Dynamic')
clr.AddReference('mscorlib')
clr.AddReference('System')
clr.AddReference('System.Data')

# add your added modules
clr.AddReference("Xceed.Wpf.Toolkit")
#
# adapted from os-path-walk-example-3.py

import os, glob
import fnmatch
import pyc

gVersion = "0.1"
BinFolder = "3DSVideoConverter" + gVersion

def doscopy(filename1):
	global BinFolder
	print filename1
	if not os.path.exists(BinFolder) :
		os.makedirs(BinFolder)
	os.system ("copy %s %s\%s" % (filename1, BinFolder, filename1))

def dosxcopy(filename1):
	global BinFolder
	print filename1
	if not os.path.exists(BinFolder) :
		os.makedirs(BinFolder)
	os.system ("xcopy /Y /S %s %s\%s" % (filename1, BinFolder, filename1))

def manualcopy() :
	global manualFile
	global BinFolder
	sourceFile = (".\Doc\%s" % manualFile)
	if not os.path.exists(BinFolder) :
		os.makedirs(BinFolder)
	print sourceFile
	os.system ("copy %s %s\%s" % (sourceFile, BinFolder, manualFile))
	
class GlobDirectoryWalker:
    # a forward iterator that traverses a directory tree
    def __init__(self, directory, pattern="*") :
        self.stack = [directory]
        self.pattern = pattern
        self.files = []
        self.index = 0
    def __getitem__(self, index):
        while 1:
            try:
                file = self.files[self.index]
                self.index = self.index + 1
            except IndexError:
                # pop next directory from stack
                self.directory = self.stack.pop()
                self.files = os.listdir(self.directory)
                self.index = 0
            else:
                # got a filename
                fullname = os.path.join(self.directory, file)
                if os.path.isdir(fullname) and not os.path.islink(fullname) and fullname[-4:]<>'.svn':
                    self.stack.append(fullname)
                if fnmatch.fnmatch(file, self.pattern):
                    return fullname

#"""
#Build StdLib.DLL
gb = glob.glob(r".\Lib\*.py")
gb += glob.glob(r".\Lib\ctypes\*.py")
gb += glob.glob(r".\Lib\json\*.py")
gb += glob.glob(r".\Lib\encodings\*.py")
gb.append("/out:StdLib")    
print ["/target:dll",]+gb
pyc.Main(["/embed","/platform:x86","/target:dll"]+gb)
print "Done Lib"
#"""
#Build EXE
# for DEBUG
#gb=["/main:QATracking.py","AddQACase.py","DBManager.py","JIRAParser.py","/embed","/standalone","/target:winexe"]
# the "/standalone" option does not works properly, so use separated dlls
#gb=["/main:3DSVideoConverter.py", "/embed","/platform:x86","/target:exe"]
gb=["/main:3DSVideoConverter.py",  "/embed","/platform:x86","/target:winexe"]
pyc.Main(gb)

#CopyFiles to Release Directory
#doscopy("PrivacyKeeper.ico")
doscopy("WizardDialog.xaml")
doscopy("3DSVideoConverter.xaml")
doscopy("Progress3D.xaml")
doscopy("OpenSourceLicenseTerms.txt")
dosxcopy("FFMPEG")
doscopy("3DSVideoConverter.exe")
doscopy("StdLib.dll")
# the "/standalon" option does not works properly, so use separated dlls
doscopy("Microsoft.Dynamic.dll")
doscopy("Microsoft.Scripting.dll")
doscopy("IronPython.dll")
doscopy("IronPython.Modules.dll")
#doscopy("IronPython.SQLite.dll")
doscopy("IronPython.Wpf.dll")
doscopy("FontAwesome.WPF.dll")
doscopy("Xceed.Wpf.Toolkit.dll")
#manualcopy()

