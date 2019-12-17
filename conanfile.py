from __future__ import print_function
from conans import ConanFile, CMake, tools
import os


class CppRestSDKConan(ConanFile):
    name = "cpprestsdk"
    version = "2.10.14"
    description = "A project for cloud-based client-server communication in native code using a modern asynchronous " \
                  "C++ API design"
    topics = ("conan", "cpprestsdk", "rest", "client", "http")
    url = "https://github.com/bincrafters/conan-cpprestsdk"
    homepage = "https://github.com/Microsoft/cpprestsdk"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "exclude_websockets": [True, False],
        "exclude_compression": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": False,
        "exclude_websockets": False,
        "fPIC": True,
        "exclude_compression": False
    }

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    root = "%s-%s" % (name, version)
    short_paths = True

    def configure(self):
        if self.settings.compiler == 'Visual Studio':
            del self.options.fPIC

    def requirements(self):
        self.requires.add("openssl/1.1.1d")
        if not self.options.exclude_compression:
            self.requires.add("zlib/1.2.11")
        if not self.options.exclude_websockets:
            self.requires.add("websocketpp/0.8.1@bincrafters/stable")
        self.requires.add("boost/1.71.0")

    def source(self):
        sha256 = "f2628b248f714d7bbd6a536553bc3782602c68ca1b129017985dd70cc3515278"
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version

        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        if self.settings.os == "iOS":
            with open('toolchain.cmake', 'w') as toolchain_cmake:
                if self.settings.arch == "armv8":
                    arch = "arm64"
                    sdk = "iphoneos"
                elif self.settings.arch == "x86_64":
                    arch = "x86_64"
                    sdk = "iphonesimulator"
                sysroot = tools.XCRun(self.settings).sdk_path
                toolchain_cmake.write('set(CMAKE_C_COMPILER /usr/bin/clang CACHE STRING "" FORCE)\n')
                toolchain_cmake.write('set(CMAKE_CXX_COMPILER /usr/bin/clang++ CACHE STRING "" FORCE)\n')
                toolchain_cmake.write('set(CMAKE_C_COMPILER_WORKS YES)\n')
                toolchain_cmake.write('set(CMAKE_CXX_COMPILER_WORKS YES)\n')
                toolchain_cmake.write('set(CMAKE_XCODE_EFFECTIVE_PLATFORMS "-%s" CACHE STRING "" FORCE)\n' % sdk)
                toolchain_cmake.write('set(CMAKE_OSX_ARCHITECTURES "%s" CACHE STRING "" FORCE)\n' % arch)
                toolchain_cmake.write('set(CMAKE_OSX_SYSROOT "%s" CACHE STRING "" FORCE)\n' % sysroot)
            os.environ['CONAN_CMAKE_TOOLCHAIN_FILE'] = os.path.join(os.getcwd(), 'toolchain.cmake')

        cmake = CMake(self, set_cmake_flags=True)
        cmake.definitions["BUILD_TESTS"] = False
        cmake.definitions["BUILD_SAMPLES"] = False
        cmake.definitions["WERROR"] = False
        cmake.definitions["CPPREST_EXCLUDE_WEBSOCKETS"] = self.options.exclude_websockets
        cmake.definitions["CPPREST_EXCLUDE_COMPRESSION"] = self.options.exclude_compression
        cmake.definitions["CPPREST_VERSION"] = self.version
        cmake.definitions["OPENSSL_ROOT_DIR"] = self.deps_cpp_info['openssl'].rootpath
        cmake.definitions["OPENSSL_USE_STATIC_LIBS"] = not self.options['openssl'].shared
        cmake.definitions["BOOST_ROOT"] = self.deps_cpp_info["boost"].rootpath
        cmake.definitions["BOOST_INCLUDEDIR"] = self.deps_cpp_info["boost"].include_paths[0]
        cmake.definitions["BOOST_LIBRARYDIR"] = self.deps_cpp_info["boost"].lib_paths[0]
        cmake.definitions["Boost_NO_SYSTEM_PATHS"] = True
        cmake.definitions["Boost_ADDITIONAL_VERSIONS"] = "1.69.0"
        cmake.definitions["Boost_USE_DEBUG_LIBS"] = self.settings.build_type == "Debug"
        cmake.definitions["Boost_USE_RELEASE_LIBS"] = self.settings.build_type != "Debug"
        cmake.definitions["Boost_USE_STATIC_LIBS"] = not self.options["boost"].shared
        if self.settings.get_safe("compiler.runtime"):
            cmake.definitions["OPENSSL_MSVC_STATIC_RT"] = 'MT' in str(self.settings.compiler.runtime)
            cmake.definitions["Boost_USE_STATIC_RUNTIME"] = 'MT' in str(self.settings.compiler.runtime)
            cmake.definitions["Boost_USE_DEBUG_RUNTIME"] = 'd' in str(self.settings.compiler.runtime)
        if self.settings.os == "iOS":
            cmake.definitions["IOS"] = True
        elif self.settings.os == "Android":
            cmake.definitions["ANDROID"] = True
            cmake.definitions["CONAN_LIBCXX"] = ''
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def _patch(self):
        cpprest_find_websocketpp = """
function(cpprest_find_websocketpp)
if(NOT TARGET cpprestsdk_websocketpp_internal)
add_library(cpprestsdk_websocketpp_internal INTERFACE)
target_include_directories(cpprestsdk_websocketpp_internal INTERFACE "${CONAN_INCLUDE_DIRS_WEBSOCKETPP}")
target_link_libraries(cpprestsdk_websocketpp_internal INTERFACE "${CONAN_LIBS_WEBSOCKETPP}")
endif()
endfunction()
"""
        cpprest_find_openssl = """
function(cpprest_find_openssl)
if(NOT TARGET cpprestsdk_openssl_internal)
add_library(cpprestsdk_openssl_internal INTERFACE)
target_include_directories(cpprestsdk_openssl_internal INTERFACE "${CONAN_INCLUDE_DIRS_OPENSSL}")
target_link_libraries(cpprestsdk_openssl_internal INTERFACE "${CONAN_LIBS_OPENSSL}")
endif()
endfunction()
"""
        tools.save(os.path.join(self._source_subfolder, "Release", "cmake", "cpprest_find_websocketpp.cmake"),
                   cpprest_find_websocketpp)
        tools.save(os.path.join(self._source_subfolder, "Release", "cmake", "cpprest_find_openssl.cmake"),
                   cpprest_find_openssl)

        tools.replace_in_file(os.path.join(self._source_subfolder, 'Release', 'CMakeLists.txt'), "-Wconversion", "")
        if self.settings.compiler == 'clang' and str(self.settings.compiler.libcxx) in ['libstdc++', 'libstdc++11']:
            tools.replace_in_file(os.path.join(self._source_subfolder, 'Release', 'CMakeLists.txt'),
                                  'libc++', 'libstdc++')
        if self.settings.os == 'Android':
            tools.replace_in_file(os.path.join(self._source_subfolder, 'Release', 'src', 'pch', 'stdafx.h'),
                                  '#include "boost/config/stdlib/libstdcpp3.hpp"',
                                  '//#include "boost/config/stdlib/libstdcpp3.hpp"')
            # https://github.com/Microsoft/cpprestsdk/issues/372#issuecomment-386798723
            tools.replace_in_file(os.path.join(self._source_subfolder, 'Release', 'src', 'http', 'client',
                                            'http_client_asio.cpp'),
                                  'm_timer.expires_from_now(m_duration)',
                                  'm_timer.expires_from_now(std::chrono::microseconds(m_duration.count()))')

    def build(self):
        self._patch()
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

        self.copy("license.txt", dst="license", src=self._source_subfolder)
        self.copy(pattern="*", dst="include", src=os.path.join(self._source_subfolder, "Release", "include"))
        self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        if self.settings.compiler == "Visual Studio":
            debug_suffix = 'd' if self.settings.build_type == 'Debug' else ''
            toolset = {'12': '120',
                       '14': '140',
                       '15': '141',
                       '16': '142'}.get(str(self.settings.compiler.version))
            version_tokens = self.version.split(".")
            versioned_name = "cpprest%s_%s_%s%s" % (toolset, version_tokens[0], version_tokens[1], debug_suffix)
            # CppRestSDK uses different library name depends on CMAKE_VS_PLATFORM_TOOLSET
            if not os.path.isfile(os.path.join(self.package_folder, 'lib', '%s.lib' % versioned_name)):
                versioned_name = "cpprest_%s_%s%s" % (version_tokens[0], version_tokens[1], debug_suffix)
            lib_name = versioned_name
        else:
            lib_name = 'cpprest'
        self.cpp_info.libs.append(lib_name)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
        elif self.settings.os == "Windows":
            self.cpp_info.libs.extend(["winhttp", "httpapi", "bcrypt"])
        elif self.settings.os == "Macos":
            self.cpp_info.exelinkflags.append("-framework CoreFoundation")
            self.cpp_info.exelinkflags.append("-framework Security")
            self.cpp_info.sharedlinkflags.append("-framework CoreFoundation")
            self.cpp_info.sharedlinkflags.append("-framework Security")
        if not self.options.shared:
            self.cpp_info.defines.append("_NO_ASYNCRTIMP")
