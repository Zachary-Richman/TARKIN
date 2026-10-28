cmake_minimum_required(VERSION 3.20)

project(TARKIN LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(orbit_test
        worker/main.cpp
        worker/orbit_worker.h
)