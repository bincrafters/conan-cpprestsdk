################################################################################
# CMake receipt for cpprestsdk test
#
# Copyright (c) Microsoft Corporation
################################################################################
project(conan-cpprestsdk-test)
cmake_minimum_required(VERSION 3.1.3)

# Import Conan package #########################################################
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# Build test ###################################################################
file(GLOB SOURCE_FILES ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp)
add_executable(${CMAKE_PROJECT_NAME} ${SOURCE_FILES})
target_link_libraries(${CMAKE_PROJECT_NAME} ${CONAN_LIBS})
set_property(TARGET ${CMAKE_PROJECT_NAME} PROPERTY CXX_STANDARD 11)

# Execute test #################################################################
enable_testing()
add_test(NAME test-all
         COMMAND ${CMAKE_PROJECT_NAME}
         WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
