cmake_minimum_required(VERSION 2.8.12)
project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()

if(CMAKE_COMPILER_IS_GNUCC)
	add_definitions(-Wno-conversion)
endif()

set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR};${CMAKE_MODULE_PATH}")

# Find Boost and zlib
if (WIN32)
    if (NOT CPPREST_EXCLUDE_WEBSOCKETS)
        find_package(Boost 1.66 COMPONENTS system date_time regex REQUIRED)
    endif()

    if (NOT CPPREST_EXCLUDE_COMPRESSION)
      set(ZLIB_ROOT ${CONAN_ZLIB_ROOT})
      set(ZLIB_LIBRARYDIR ${CONAN_LIB_DIRS_ZLIB})
      find_package(ZLIB REQUIRED)
    endif()
endif(WIN32)

add_subdirectory("cpprestsdk-${CPPREST_VERSION}/Release")
