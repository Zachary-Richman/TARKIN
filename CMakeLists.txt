cmake_minimum_required(VERSION 3.20)

project(TARKIN LANGUAGES C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

# External dependencies
set(EXTERNAL_DIR "${CMAKE_CURRENT_SOURCE_DIR}/worker/external")

# REBOUND
set(REBOUND_DIR "${EXTERNAL_DIR}/rebound")
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

# cJSON
set(CJSON_DIR "${EXTERNAL_DIR}/cJSON")

if(NOT EXISTS "${CJSON_DIR}/cJSON.c")
    message(FATAL_ERROR "cJSON source files not found: ${CJSON_DIR}")
endif()

add_library(cjson STATIC
        "${CJSON_DIR}/cJSON.c"
)

target_include_directories(cjson PUBLIC
        "${CJSON_DIR}"
)

# TARKIN executable
add_executable(orbit_test
        worker/src/main.c
        worker/src/json_in.c
        worker/src/stability.c
        worker/src/creator.c
        worker/src/simulation.c
        worker/src/dynamic_fgets.c
)

# Project headers
target_include_directories(orbit_test PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/worker/include"
)

# Dependencies
target_link_libraries(orbit_test PRIVATE
        rebound
        cjson
)

if(NOT MSVC)
    target_link_libraries(orbit_test PRIVATE m)
endif()