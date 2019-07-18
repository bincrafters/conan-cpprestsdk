cmake_minimum_required(VERSION 2.8.12)
project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()

set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR};${CMAKE_MODULE_PATH}")

add_library(cpprestsdk_websocketpp_internal INTERFACE)
target_include_directories(cpprestsdk_websocketpp_internal INTERFACE "${CONAN_INCLUDE_DIRS_WEBSOCKETPP}")
target_link_libraries(cpprestsdk_websocketpp_internal INTERFACE "${CONAN_LIBS_WEBSOCKETPP}")

add_subdirectory("source_subfolder")
