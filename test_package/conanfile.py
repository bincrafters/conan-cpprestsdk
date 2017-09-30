from conans import ConanFile, CMake, RunEnvironment, tools
import os


class TestPackage(ConanFile):
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy(pattern="*.so*", dst="bin", src="lib")
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")

    def test(self):
        with tools.chdir("bin"):
            env_build = RunEnvironment(self)
            with tools.environment_append(env_build.vars):
                if self.settings.os == "Windows":
                    self.run("test_package")
                else:
                    self.run("./test_package")
