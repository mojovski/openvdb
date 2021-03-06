# yue.nicholas@gmail.com
CMAKE_MINIMUM_REQUIRED(VERSION 2.8)
SET(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake_modules")

PROJECT ( OpenVDB )

#for an explanation about the glfw, glew, ... see http://www.cis.gvsu.edu/~dulimarh/Okto/cis367/

FIND_PACKAGE ( GLFW3 REQUIRED )
MESSAGE(STATUS "-------- GLFW FOUND IN ${GLFW_INCLUDE_DIR}, \nlibs: ${GLFW_LIBRARY}")

FIND_PACKAGE ( GLEW REQUIRED )

set(Boost_USE_STATIC_LIBS ON)
FIND_PACKAGE ( Boost REQUIRED COMPONENTS iostreams system thread )
MESSAGE(STATUS "-------- BOOST FOUND IN ${Boost_LIBRARY_DIRS}, \nlibs: ${Boost_LIBRARIES}\nflags: ")
FIND_PACKAGE ( ILMBase REQUIRED )
FIND_PACKAGE ( OpenEXR REQUIRED )
MESSAGE(STATUS "FOund OPENEXR_INCLUDE_DIR: ${OPENEXR_INCLUDE_DIR}\nOPENEXR_LIBRARIES: ${OPENEXR_LIBRARIES}")
FIND_PACKAGE ( TBB REQUIRED )
MESSAGE(STATUS "Found TBB IN ${TBB_INCLUDE_DIRS}\ntbblibs: ${TBB_LIBRARIES}")
FIND_PACKAGE ( ZLIB REQUIRED )
FIND_PACKAGE ( OpenGL REQUIRED )
FIND_PACKAGE ( Blosc)
FIND_PACKAGE ( Doxygen)
IF (APPLE)
  FIND_LIBRARY ( COCOA_LIBRARY Cocoa )
  FIND_LIBRARY ( IOKIT_LIBRARY IOKit )
  FIND_LIBRARY ( COREVIDEO_LIBRARY CoreVideo )
ENDIF ()

IF ( UNIX AND NOT APPLE )
  MESSAGE ( "UNIX" )
  SET ( XI_LIBRARY Xi )
  SET ( XRANDR_LIBRARY Xrandr )
ENDIF ()

#IF ( USE_GLFW3 )
  SET ( OPENVDB_USE_GLFW_FLAG "-DOPENVDB_USE_GLFW_3" )
#ENDIF ()

# MESSAGE ( "ZLIB_INCLUDE_DIR = ${ZLIB_INCLUDE_DIR}")

INCLUDE_DIRECTORIES ( .. ) # So they can simulate referencing installed headers
INCLUDE_DIRECTORIES ( . ) # So they can simulate referencing installed headers

INCLUDE_DIRECTORIES ( ${Boost_INCLUDE_DIR} )
INCLUDE_DIRECTORIES ( ${ILMBASE_INCLUDE_DIRS} )
INCLUDE_DIRECTORIES ( ${TBB_INCLUDE_DIRS} )
INCLUDE_DIRECTORIES ( ${OPENGL_INCLUDE_DIR} )
INCLUDE_DIRECTORIES ( ${ZLIB_INCLUDE_DIR} )
MESSAGE(STATUS "Found GLFW : ${GLFW3_INCLUDE_DIR}")
INCLUDE_DIRECTORIES ( ${GLFW3_INCLUDE_DIR} )

message(STATUS "Found glew include dir: ${GLEW_INCLUDE_DIR}")
INCLUDE_DIRECTORIES ( ${GLEW_INCLUDE_DIR} )
LINK_DIRECTORIES ( ${GLEW_LIBRARY_DIRS} )


#IF (WIN32)
#  # Because of implicit linking!
  LINK_DIRECTORIES ( ${Boost_LIBRARY_DIR} )
#ENDIF ()

IF (WIN32)
  MESSAGE(STATUS "Skipping BLOSC")
ELSE ()
  #MESSAGE(STATUS "Using Blosc lib ${BLOSC_LIBRARY_DIRS}")
  #INCLUDE_DIRECTORIES ( ${BLOSC_INCLUDE_DIR} )
  #SET(OPENVDB_USE_BLOSC "-DOPENVDB_USE_BLOSC")
  #LINK_DIRECTORIES(${BLOSC_LIBRARY_DIRS})
ENDIF ()

IF (WIN32)
  ADD_DEFINITIONS ( -D_WIN32 -DNOMINMAX -DHALF_EXPORTS -DOPENVDB_DLL )
ELSE ()
  ADD_DEFINITIONS ( -pthread -fPIC )
ENDIF ()

# Working around hardcoding of path at DWA
FILE ( GLOB VIEWER_SOURCE_FILES RELATIVE ${CMAKE_SOURCE_DIR} viewer/* )
FILE ( MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/dwa/openvdb_viewer )
FILE ( COPY ${VIEWER_SOURCE_FILES} DESTINATION ${CMAKE_BINARY_DIR}/dwa/openvdb_viewer )
INCLUDE_DIRECTORIES ( ${CMAKE_BINARY_DIR}/dwa )

SET ( OPENVDB_LIBRARY_SOURCE_FILES
  Grid.cc
  io/Archive.cc
  io/Compression.cc
  io/File.cc
  io/GridDescriptor.cc
  io/Queue.cc
  io/Stream.cc
  io/TempFile.cc
  math/Maps.cc
  math/Proximity.cc
  math/QuantizedUnitVec.cc
  math/Transform.cc
  metadata/Metadata.cc
  metadata/MetaMap.cc
  openvdb.cc
  Platform.cc
  util/Formats.cc
  util/Util.cc
  )

 SET_SOURCE_FILES_PROPERTIES ( ${OPENVDB_LIBRARY_SOURCE_FILES}
   PROPERTIES
   COMPILE_FLAGS "-DOPENVDB_PRIVATE ${OPENVDB_USE_BLOSC} ${OPENVDB_USE_GLFW_FLAG}"
 )

ADD_LIBRARY ( openvdb STATIC
  ${OPENVDB_LIBRARY_SOURCE_FILES}
  )

set(ALL_LIBS
  ${Boost_LIBRARIES}
  ${TBB_LIBRARIES}
  ${Ilmbase_HALF_LIBRARY}
  ${ZLIB_LIBRARY}
  ${GLEW_LIBRARIES}
  ${BLOSC_blosc_LIBRARY} 
  ${Openexr_ILMIMF_LIBRARY}
  ${Ilmbase_IEX_LIBRARY}
  ${Ilmbase_ILMTHREAD_LIBRARY}
)

TARGET_LINK_LIBRARIES ( openvdb
  ${ALL_LIBS}
  )




# Doxygen docmentation
FILE ( READ ${CMAKE_SOURCE_DIR}/doxygen-config DOXYGEN_CONFIG_CONTENT )
FILE ( WRITE ${CMAKE_CURRENT_BINARY_DIR}/cmake-doxygen-config ${DOXYGEN_CONFIG_CONTENT} )
FILE ( APPEND ${CMAKE_CURRENT_BINARY_DIR}/cmake-doxygen-config "OUTPUT_DIRECTORY=${CMAKE_BINARY_DIR}/doc\n" )

#uncomment the doxygen generation per default
#ADD_CUSTOM_TARGET ( doc ALL
#  ${DOXYGEN_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/cmake-doxygen-config
#  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
#  COMMENT "Generating API documentation with Doxygen" VERBATIM
#)

INSTALL ( DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/doc/html/ DESTINATION doc)

# Installation
INSTALL ( TARGETS
  #vdb_view
  #vdb_print
  #vdb_render
  DESTINATION
  bin
  )

INSTALL ( TARGETS
  openvdb
  DESTINATION
  lib
  )

INSTALL ( DIRECTORY ${CMAKE_SOURCE_DIR} DESTINATION include
          FILES_MATCHING PATTERN "*.h")
