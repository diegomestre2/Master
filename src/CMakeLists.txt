cmake_minimum_required(VERSION 3.5)
project(TPCH_Query6_CS)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES tpchQuery06.c)
add_executable(TPCH_Query6_CS ${SOURCE_FILES})