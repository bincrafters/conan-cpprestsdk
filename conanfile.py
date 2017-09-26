from conans import ConanFile, CMake, tools
from os import path


class CppRestSDKConan(ConanFile):
    name = "cpprestsdk"
    version = "2.9.1"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports_sources = "CMakeLists.txt"
    url = "https://github.com/bincrafters/conan-cpprestsdks"
    author = "Uilian Ries <uilianries@gmail.com>"
    description = "A project for cloud-based client-server communication in native code using a modern asynchronous C++ API design"
    license = "https://github.com/Microsoft/cpprestsdk/blob/master/license.txt"
    requires = "OpenSSL/1.0.2l@conan/stable", \
            "zlib/1.2.8@conan/stable", \
            "websocketpp/0.7.0@bincrafters/testing", \
            "Boost.Random/1.64.0@bincrafters/testing", \
            "Boost.System/1.64.0@bincrafters/testing", \
            "Boost.Thread/1.64.0@bincrafters/testing", \
            "Boost.Filesystem/1.64.0@bincrafters/testing", \
            "Boost.Chrono/1.64.0@bincrafters/testing", \
            "Boost.Atomic/1.64.0@bincrafters/testing", \
            "Boost.Date_Time/1.64.0@bincrafters/testing", \
            "Boost.Regex/1.64.0@bincrafters/testing"
  
    def source(self):
        source_url = "https://github.com/Microsoft/cpprestsdk"
        tools.get("{0}/{1}/archive/v{2}.tar.gz".format(source_url, self.name, self.version))

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
