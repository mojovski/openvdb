#sets up all the environment variables required by openvdb
import pkgconfig
print pkgconfig.exists('glib-2.0')
print pkgconfig.cflags('boost')
import os
import subprocess as sub

def callcmd(cmd):
	p = sub.Popen(cmd,stdout=sub.PIPE,stderr=sub.PIPE, shell=True)
	output, errors = p.communicate()
	#print errors
	return output

def locatePathToFile(filename, guesses=[]):
	#check hypothesises first
	for guess in guesses:
		dirname=os.path.dirname(guess)
		if os.path.isdir(dirname):
			print "found "+filename+" in "+dirname
			return dirname
	#use the OS locate feature
	hypothesis=callcmd("locate "+filename)
	hlist=hypothesis.split("\n")
	dirname=os.path.dirname(hlist[0])
	if (not os.path.isdir(dirname)):
		raise Exception(filename+" not found!")
	print "found "+filename+" in "+dirname
	return dirname

def locateIncludeDir(dirname, file_inside, guesses=[]):
	"""
	dirname: The direcory to find. e.g. /tbb
	file_inside: The file, which must be located in that directory. e.g. tbb.h
	guesses: Initial hypotheses eg /usr/include/tbb
	"""

	#check hypothesises first
	for guess in guesses:
		abs_file=guess+"/"+file_inside
		if os.path.isfile(abs_file):
			parent_dir=guess.split(dirname)[0]
			print "found "+file_inside+" in "+guess+", parent dir: "+parent_dir
			return parent_dir #return /usr/include instead of /usr/include/tbb
	#use the OS locate feature
	hypothesis=callcmd("locate "+dirname)
	hlist=hypothesis.split("\n")
	for hi in hlist:
		abs_file=hi+"/"+file_inside
		if os.path.isfile(abs_file):
			parent_dir=hi.split(dirname)[0]
			print "found "+file_inside+" in "+hi+", parent dir: "+parent_dir
			return parent_dir #return /usr/include instead of /usr/include/tbb

	raise Exception(filename+" not found!")

os.environ["INSTALL_DIR"]="/tmp/openvdb"
#-----------
# find boost
#----------
boost_include_dir="/usr/include"
if (not (os.path.isdir(boost_include_dir+"/boost"))):
	raise Exception("Boost Include dir not found")
print "found boost BOOST_INCL_DIR in "+boost_include_dir
os.environ["BOOST_INCL_DIR"]=boost_include_dir

#set BOOST_LIB_DIR
hypothesis=callcmd("locate libboost_iostreams.a")
#finds something like /usr/lib/x86_64-linux-gnu/libboost_iostreams.a
boost_lib_dir=os.path.dirname(hypothesis.split("\n")[0])
print "found BOOST_LIB_DIR in "+boost_lib_dir
os.environ["BOOST_LIB_DIR"]=boost_lib_dir

os.environ["BOOST_THREAD_LIB"]="-lpthread"

#------------
#	find openext
#-----------
openexr_dir=locateIncludeDir("/OpenEXR", file_inside="half.h", guesses=["/usr/include/OpenEXR"])
os.environ["ILMBASE_INCL_DIR"]="/usr/include/OpenEXR/" #special case. :(#openexr_dir


#----------
# locate #ILMBASE_LIB_DIR
#-----------
openexr_lib_dir=locatePathToFile("/libHalf.so")
os.environ["ILMBASE_LIB_DIR"]=openexr_lib_dir

ilmbase_lib=locatePathToFile("/libIlmThread.a")
os.environ["ILMBASE_LIB"]=openexr_lib_dir

linker_flag_half="-lHalf"
os.environ["HALF_LIB"]=linker_flag_half

#----------
#locate exr_incl_dir
#--------
exr_incl_dir=locatePathToFile("/ImfName.h", guesses=["/usr/include/OpenEXR/ImfName.h"])
os.environ["EXR_INCL_DIR"]= exr_incl_dir

os.environ["EXR_LIB_DIR"]=locatePathToFile("/libIlmImf.so", guesses=["/usr/lib/x86_64-linux-gnu/libIlmImf.a"])
#linker flag
os.environ["EXR_LIB"]="-lIlmImf"

############
#	locate TBB
#-----------
#TBB_INCL_DIR
os.environ["TBB_INCL_DIR"]=locateIncludeDir("/tbb", file_inside="tbb.h", guesses=["/usr/include/tbb/"])
os.environ["TBB_LIB_DIR"]=locatePathToFile("/libtbb.so", guesses=["/usr/lib/libtbb.so"])
os.environ["TBB_LIB"]="-ltbb"

############
#	locate Blosc
#------------
os.environ["BLOSC_INCL_DIR"]=locateIncludeDir("/blosc", file_inside="blosc.h")
os.environ["BLOSC_LIB_DIR"]=locatePathToFile("/libblosc.a")
os.environ["BLOSC_LIB"]="-lblosc"

############
#	locate concurrent malloc lib
#-------------
os.environ["CONCURRENT_MALLOC_LIB_DIR"]=locatePathToFile("/libjemalloc.a", guesses=["/usr/lib/x86_64-linux-gnu/libjemalloc.a"])
#locateIncludeDir("/jemalloc", file_inside="jemalloc.h", guesses=["/usr/include/jemalloc/"])
os.environ["CONCURRENT_MALLOC_LIB"]="-ljemalloc"


#############
#	locate GLFW
#------------
os.environ["GLFW_INCL_DIR"]=locateIncludeDir("/GLFW", file_inside="glfw3.h", guesses=[os.path.dirname(os.path.realpath(__file__))+"/../../glfw/include/GLFW/"])
os.environ["GLFW_LIB_DIR"]=locatePathToFile("/libglfw3.a", guesses=[os.path.dirname(os.path.realpath(__file__))+"/../../glfw/src/libglfw3.a"])
os.environ["GLFW_MAJOR_VERSION"]="3"

##############
#	locate LOG4CPLUS
#-------------
os.environ["LOG4CPLUS_INCL_DIR"]=locateIncludeDir("/log4cplus", file_inside="loglevel.h", guesses=["/usr/include/log4cplus/"])
os.environ["LOG4CPLUS_LIB_DIR"]=locatePathToFile("liblog4cplus.so", guesses=["/usr/lib/liblog4cplus.so"])
os.environ["LOG4CPLUS_LIB"]="-lllog4cplus"

os.environ["PYTHON_VERSION"]="" #deactivate

#####################################################################
#			build

#os.system("make")
print "Now, call 'make'"