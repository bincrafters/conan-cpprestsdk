"""Validation for CppRestSDK library package

"""
from os import getenv
from conans import CMake
from conans import ConanFile


class TestCppRestSDKConan(ConanFile):
    """Build test with cpprestsdk package
    """
    author = "Uilian Ries <uilianries@gmail.com>"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    channel = getenv("CONAN_CHANNEL", "testing")
    username = getenv("CONAN_USERNAME", "uilianries")
    requires = "cpprestsdk/2.9.1@%s/%s" % (username, channel), "Catch/1.9.6@uilianries/stable"

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_dir="./")
        cmake.build()

    def imports(self):
        self.copy(pattern="*.so*", dst="bin", src="lib")
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")

    def test(self):
        cmake = CMake(self)
        cmake.configure(build_dir="./")
        cmake.test()
