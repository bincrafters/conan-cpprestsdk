[ ![Download](https://api.bintray.com/packages/bincrafters/public-conan/cpprestsdk%3Abincrafters/images/download.svg?version=2.9.1%3Astable) ](https://bintray.com/bincrafters/public-conan/cpprestsdk%3Abincrafters/2.9.1%3Astable/link)
[![Build Status](https://travis-ci.org/bincrafters/conan-cpprestsdk.svg?branch=stable%2F2.9.1)](https://travis-ci.org/bincrafters/conan-cpprestsdk)
[![Build status](https://ci.appveyor.com/api/projects/status/a5snyovachh6e8nh?svg=true)](https://ci.appveyor.com/project/BinCrafters/conan-cpprestsdk)

The **C++ REST SDK** is a Microsoft project for cloud-based client-server communication in native code using a modern asynchronous C++ API design. This project aims to help C++ developers connect to and interact with services.

![conan-cpprestsdk](conan-cpprestsdk.png)

[Conan.io](https://conan.io) package for [cpprestsdk](https://github.com/Microsoft/cpprestsdk) project

The packages generated with this **conanfile** can be found in [Bintray](https://bintray.com/bincrafters/public-conan/cpprestsdk%3Abincrafters).

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py

If your are in Windows you should run it from a VisualStudio console in order to get "mc.exe" in path.

## Upload packages to server

    $ conan upload cpprestsdk/2.9.1@bincrafters/stable --all

## Reuse the packages

### Basic setup

    $ conan install cpprestsdk/2.9.1@bincrafters/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    cpprestsdk/2.9.1@bincrafters/stable

    [options]
    cpprestsdk:shared=True # False

    [generators]
    cmake

Complete the installation of requirements for your project running:

    conan install .

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.

### License
[MIT](LICENSE)
