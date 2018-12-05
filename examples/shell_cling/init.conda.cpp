// Load this file into cling, like so:
//
// > cling --std=c++14
// [cling]$ .L init.cpp          <=== Type this to load this file

#pragma cling add_library_path("/root/miniconda3/lib/")
#pragma cling add_include_path("/root/miniconda3/include")

#pragma cling load("libopencv_core.so")
#pragma cling load("libopencv_calib3d.so")
#pragma cling load("libopencv_highgui.so")
#pragma cling load("libopencv_imgcodecs.so")
#pragma cling load("libopencv_imgproc.so")

//#pragma cling add_include_path("fplus_include/")
#pragma cling add_include_path(".")

#include <string>
#include <vector>
#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <fplus/fplus.hpp>
