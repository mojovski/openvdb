# This file adds the include directories and library dirs to your project.
# You should include this file from your project by:
# include(/pathto/Config.cmake)

#BUG: ${CMAKE_CURRENT_LIST_DIR} doenst work. Workaround:
string(REGEX REPLACE "/Config.cmake" "" path ${CMAKE_CURRENT_LIST_FILE})
#message(STATUS "File Dir of OsLibConfig: ${path}")

set(OPENVDB_INCLUDE_DIRS ${path})
set(OPENVDB_LIBRARY_DIRS "${path}/openvdb/")
if(MSVC)
	MESSAGE(STATUS "SKIPPING OPENVDB FILES")
else()
	set(OPENVDB_LIBRARIES openvdb Half tbb)
endif(MSVC)