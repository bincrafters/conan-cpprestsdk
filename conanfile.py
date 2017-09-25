"""Conan.io recipe for CppRestSDK library
"""
from conans import ConanFile, CMake
from os import path


class CppRestSDKConan(ConanFile):
    """Checkout CppRestSDK, build and create package
    """
    name = "cpprestsdk"
    version = "2.9.1"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    exports_sources = "CMakeLists.txt"
    url = "https://github.com/Microsoft/cpprestsdk"
    author = "Uilian Ries <uilianries@gmail.com>"
    description = "A project for cloud-based client-server communication in native code using a modern asynchronous C++ API design"
    license = "https://github.com/Microsoft/cpprestsdk/blob/master/license.txt"
    requires = "Boost/1.62.0@lasote/stable", "OpenSSL/1.0.2l@conan/stable"
    cpprestsdk_dir = "%s-%s" % (name, version)
    default_options = "shared=True"

    def source(self):
        self.run("git clone --depth=50 --branch=v%s %s.git %s" % (self.version, self.url, self.cpprestsdk_dir))

    def config_options(self):
        if self.settings.os == "Linux":
            self.options["Boost"].fPIC = True

    def configure(self):
        if self.settings.os == "Macos" or self.settings.os == "Windows":
            self.options.shared = True

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False
        cmake.definitions["BUILD_SAMPLES"] = False
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("license.txt",  dst=".", src=self.cpprestsdk_dir)
        self.copy(pattern="*", dst="include", src=path.join("cpprestsdk-2.9.1", "Release", "include"))
        self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=path.join("cpprestsdk-2.9.1", "Release", "Binaries"), keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src=path.join("cpprestsdk-2.9.1", "Release", "Binaries"), keep_path=False)

    def package_info(self):
        lib_name = "cpprest_2_9" if self.settings.compiler == "Visual Studio" else "cpprest"
        self.cpp_info.libs.append(lib_name)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
