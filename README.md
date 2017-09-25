[![Download](https://api.bintray.com/packages/uilianries/conan/cpprestsdk%3Auilianries/images/download.svg) ](https://bintray.com/uilianries/conan/cpprestsdk%3Auilianries/_latestVersion)
[![Travis Build Status](https://travis-ci.org/uilianries/conan-cpprestsdk.svg?branch=release%2F2.9.1)](https://travis-ci.org/uilianries/conan-cpprestsdk)
[![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/goisbnt12o3ueq3o/branch/release/2.9.1?svg=true)](https://ci.appveyor.com/project/uilianries/conan-cpprestsdk/branch/release/2.9.1)
[![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)

The **C++ REST SDK** is a Microsoft project for cloud-based client-server communication in native code using a modern asynchronous C++ API design. This project aims to help C++ developers connect to and interact with services.

![conan-cpprestsdk](conan-cpprestsdk.png)

[Conan.io](https://conan.io) package for [cpprestsdk](https://github.com/Microsoft/cpprestsdk) project

The packages generated with this **conanfile** can be found in [Bintray](https://bintray.com/uilianries/conan/cpprestsdk%3Auilianries).

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py

If your are in Windows you should run it from a VisualStudio console in order to get "mc.exe" in path.

## Upload packages to server

    $ conan upload cpprestsdk/2.9.1@uilianries/stable --all

## Reuse the packages

### Basic setup

    $ conan install cpprestsdk/2.9.1@uilianries/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    cpprestsdk/2.9.1@uilianries/stable

    [options]
    cpprestsdk:shared=True # False

    [generators]
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install .

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.

### License
[MIT](LICENSE)
