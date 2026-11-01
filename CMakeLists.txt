cmake_minimum_required(VERSION 3.20)

project(TARKIN LANGUAGES C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

# REBOUND
set(REBOUND_DIR "${CMAKE_CURRENT_SOURCE_DIR}/worker/external/rebound")
set(REBOUND_SRC "${REBOUND_DIR}/src")

if(NOT EXISTS "${REBOUND_SRC}/rebound.c")
    message(FATAL_ERROR "REBOUND source files not found: ${REBOUND_SRC}")
endif()

file(GLOB REBOUND_SOURCES CONFIGURE_DEPENDS
        "${REBOUND_SRC}/*.c"
)

add_library(rebound STATIC ${REBOUND_SOURCES})
target_compile_definitions(rebound PUBLIC BUILDINGLIBREBOUND)

target_include_directories(rebound PUBLIC
        "${REBOUND_SRC}"
)

# Test executable
add_executable(orbit_test
        worker/src/main.c
        worker/include/creator.h
        worker/include/stability.h
)

target_link_libraries(orbit_test PRIVATE rebound)

if(NOT MSVC)
    target_link_libraries(orbit_test PRIVATE m)
endif()