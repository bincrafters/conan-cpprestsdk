PROJECT(conan-cpprestsdk)

MESSAGE(WARNING "Conan CppRestSDK Wrapped CMake")
cmake_minimum_required(VERSION 2.8.12)
include(conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

# Find Boost and zlib 
if (WIN32)
    set(BOOST_ROOT ${CONAN_BOOST_ROOT})
    set(BOOST_LIBRARYDIR ${CONAN_LIB_DIRS_BOOST})
    find_package(Boost 1.62 COMPONENTS system date_time regex REQUIRED)

    set(ZLIB_ROOT ${CONAN_ZLIB_ROOT})
    set(ZLIB_LIBRARYDIR ${CONAN_LIB_DIRS_ZLIB})
    find_package(ZLIB REQUIRED)
endif(WIN32)

add_subdirectory("cpprestsdk-2.9.1/Release")
