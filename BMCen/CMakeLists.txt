cmake_minimum_required(VERSION 2.8)
project( Motion )
find_package( OpenCV REQUIRED )
add_library( motionlib SHARED
	motion-estimation.cpp )

target_link_libraries( motionlib ${OpenCV_LIBS} )
