from __future__ import print_function
from conans import ConanFile, CMake, tools
from os import path, getcwd, environ
import subprocess


def call(command):
    return subprocess.check_output(command, shell=False).strip()


def find_sysroot(sdk):
    return call(["xcrun", "--show-sdk-path", "-sdk", sdk])


class CppRestSDKConan(ConanFile):
    name = "cpprestsdk"
    version = "2.10.2"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "exclude_websockets": [True, False],
               "exclude_compression": [True, False],
               "fPIC": [True, False]}
    default_options = "shared=False", "exclude_websockets=False", "fPIC=True", "exclude_compression=False"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = ['cmake']
    url = "https://github.com/bincrafters/conan-cpprestsdk"
    homepage = "https://github.com/Microsoft/cpprestsdk"
    author = "Bincrafters <bincrafters@gmail.com>"
    description = "A project for cloud-based client-server communication in native code using a modern asynchronous " \
                  "C++ API design"
    license = "https://github.com/Microsoft/cpprestsdk/blob/master/license.txt"
    root = "%s-%s" % (name, version)
    short_paths = True

    def configure(self):
        if self.settings.compiler == 'Visual Studio':
            del self.options.fPIC

    def requirements(self):
        self.requires.add("OpenSSL/1.0.2o@conan/stable")
        if not self.options.exclude_compression:
            self.requires.add("zlib/1.2.11@conan/stable")
        if not self.options.exclude_websockets:
            self.requires.add("websocketpp/0.7.0@bincrafters/stable")
        self.requires.add("boost_random/1.66.0@bincrafters/stable")
        self.requires.add("boost_system/1.66.0@bincrafters/stable")
        self.requires.add("boost_thread/1.66.0@bincrafters/stable")
        self.requires.add("boost_filesystem/1.66.0@bincrafters/stable")
        self.requires.add("boost_chrono/1.66.0@bincrafters/stable")
        self.requires.add("boost_atomic/1.66.0@bincrafters/stable")
        self.requires.add("boost_asio/1.66.0@bincrafters/stable")
        self.requires.add("boost_date_time/1.66.0@bincrafters/stable")
        self.requires.add("boost_regex/1.66.0@bincrafters/stable")
        self.requires.add("cmake_findboost_modular/1.66.0@bincrafters/stable")

    def source(self):
        source_url = "https://github.com/Microsoft/cpprestsdk"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))

        if self.settings.compiler == 'clang' and str(self.settings.compiler.libcxx) in ['libstdc++', 'libstdc++11']:
            tools.replace_in_file(path.join('cpprestsdk-%s' % self.version, 'Release', 'CMakeLists.txt'),
                                  'libc++', 'libstdc++')
        if self.settings.os == 'Android':
            tools.replace_in_file(path.join('cpprestsdk-%s' % self.version, 'Release', 'cmake', 'cpprest_find_boost.cmake'), 'find_host_package', 'find_package')
            tools.replace_in_file(path.join('cpprestsdk-%s' % self.version, 'Release', 'src', 'pch', 'stdafx.h'), '#include "boost/config/stdlib/libstdcpp3.hpp"', '//#include "boost/config/stdlib/libstdcpp3.hpp"')
            tools.replace_in_file(path.join('cpprestsdk-%s' % self.version, 'Release', 'src', 'http', 'client', 'http_client_asio.cpp'),
                                  'm_timer.expires_from_now(m_duration)',
                                  'm_timer.expires_from_now(std::chrono::microseconds(m_duration.count()))')

    def build(self):
        if self.settings.compiler == 'Visual Studio':
            with tools.vcvars(self.settings, force=True, filter_known_paths=False):
                self.build_cmake()
        else:
            self.build_cmake()

    def build_cmake(self):
        if self.settings.os == "iOS":
            with open('toolchain.cmake', 'w') as toolchain_cmake:
                if self.settings.arch == "armv8":
                    arch = "arm64"
                    sdk = "iphoneos"
                elif self.settings.arch == "x86_64":
                    arch = "x86_64"
                    sdk = "iphonesimulator"
                sysroot = find_sysroot(sdk)
                toolchain_cmake.write('set(CMAKE_C_COMPILER /usr/bin/clang CACHE STRING "" FORCE)\n')
                toolchain_cmake.write('set(CMAKE_CXX_COMPILER /usr/bin/clang++ CACHE STRING "" FORCE)\n')
                toolchain_cmake.write('set(CMAKE_C_COMPILER_WORKS YES)\n')
                toolchain_cmake.write('set(CMAKE_CXX_COMPILER_WORKS YES)\n')
                toolchain_cmake.write('set(CMAKE_XCODE_EFFECTIVE_PLATFORMS "-%s" CACHE STRING "" FORCE)\n' % sdk)
                toolchain_cmake.write('set(CMAKE_OSX_ARCHITECTURES "%s" CACHE STRING "" FORCE)\n' % arch)
                toolchain_cmake.write('set(CMAKE_OSX_SYSROOT "%s" CACHE STRING "" FORCE)\n' % sysroot)
            environ['CONAN_CMAKE_TOOLCHAIN_FILE'] = path.join(getcwd(), 'toolchain.cmake')

        cmake = CMake(self)
        if self.settings.compiler != 'Visual Studio':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.definitions["BUILD_TESTS"] = False
        cmake.definitions["BUILD_SAMPLES"] = False
        cmake.definitions["WERROR"] = False
        cmake.definitions["CPPREST_EXCLUDE_WEBSOCKETS"] = self.options.exclude_websockets
        cmake.definitions["CPPREST_EXCLUDE_COMPRESSION"] = self.options.exclude_compression
        cmake.definitions["CPPREST_VERSION"] = self.version
        if self.settings.os == "iOS":
            cmake.definitions["IOS"] = True
        elif self.settings.os == "Android":
            cmake.definitions["ANDROID"] = True
            cmake.definitions["CONAN_LIBCXX"] = ''
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("license.txt", dst="license", src=self.root)
        self.copy(pattern="*", dst="include", src=path.join(self.root, "Release", "include"))
        self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        if self.settings.compiler == "Visual Studio":
            debug_suffix = 'd' if self.settings.build_type == 'Debug' else ''
            version_tokens = self.version.split(".")
            vs_version = str(self.settings.compiler.version) + '0'
            versioned_name = "cpprest%s_%s_%s%s" % (vs_version, version_tokens[0], version_tokens[1], debug_suffix)
            # CppRestSDK uses different library name depends on CMAKE_VS_PLATFORM_TOOLSET
            if not path.isfile(path.join(self.package_folder, 'lib', '%s.lib' % versioned_name)):
                versioned_name = "cpprest_%s_%s%s" % (version_tokens[0], version_tokens[1], debug_suffix)
            lib_name = versioned_name
        else:
            lib_name = 'cpprest'
        self.cpp_info.libs.append(lib_name)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
        elif self.settings.os == "Windows":
            self.cpp_info.libs.append("winhttp")
        if not self.options.shared:
            self.cpp_info.defines.append("_NO_ASYNCRTIMP")
