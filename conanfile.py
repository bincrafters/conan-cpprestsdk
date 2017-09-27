from __future__ import print_function
from conans import ConanFile, CMake, tools
from os import path, getcwd
import fnmatch


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

    def requirements(self):
        self.requires.add("OpenSSL/1.0.2l@conan/stable")
        self.requires.add("zlib/1.2.8@conan/stable")
        self.requires.add("websocketpp/0.7.0@%s/%s" % (self.user, self.channel))
        self.requires.add("Boost.Random/1.64.0@%s/%s" % (self.user, self.channel))
        self.requires.add("Boost.System/1.64.0@%s/%s" % (self.user, self.channel))
        self.requires.add("Boost.Thread/1.64.0@%s/%s" % (self.user, self.channel))
        self.requires.add("Boost.Filesystem/1.64.0@%s/%s" % (self.user, self.channel))
        self.requires.add("Boost.Chrono/1.64.0@%s/%s" % (self.user, self.channel))
        self.requires.add("Boost.Atomic/1.64.0@%s/%s" % (self.user, self.channel))
        self.requires.add("Boost.Date_Time/1.64.0@%s/%s" % (self.user, self.channel))
        self.requires.add("Boost.Regex/1.64.0@%s/%s" % (self.user, self.channel))

    def source(self):
        source_url = "https://github.com/Microsoft/cpprestsdk"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))

    def build(self):
        boost_include_dirs = []
        boost_library_dirs = []
        boost_libraries = []
        for (pkg_name, cpp_info) in self.deps_cpp_info.dependencies:
            if fnmatch.fnmatch(pkg_name, "Boost.*"):
                boost_include_dirs.extend([path.join(cpp_info.rootpath, d) for d in cpp_info.includedirs])
                if cpp_info.libs:
                    boost_library_dirs.extend([path.join(cpp_info.rootpath, d) for d in cpp_info.libdirs])
                    boost_libraries.extend(cpp_info.libs)

        boost_include_dirs = ";".join(boost_include_dirs)
        boost_library_dirs = ";".join(boost_library_dirs)
        boost_libraries = ";".join(boost_libraries)

        # we have to use our own FindBoost.cmake, as CMake's one does not support modular boost
        with open("FindBoost.cmake", "w") as boost_config:
            boost_config.write('message(STATUS "using boost config")\n')
            boost_config.write('set(Boost_INCLUDE_DIRS "%s")\n' % boost_include_dirs)
            boost_config.write('set(Boost_LIBRARY_DIRR "%s")\n' % boost_library_dirs)
            boost_config.write('set(Boost_LIBRARIES "%s")\n' % boost_libraries)
            boost_config.write('set(Boost_FOUND ON)\n')
            for (pkg_name, cpp_info) in self.deps_cpp_info.dependencies:
                if fnmatch.fnmatch(pkg_name, "Boost.*") and cpp_info.libs:
                    for library in cpp_info.libs:
                        library_name = library.split('_')[1].upper()
                        boost_config.write('set(Boost_%s_LIBRARY "%s")\n' % (library_name, library))

        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False
        cmake.definitions["BUILD_SAMPLES"] = False
        cmake.definitions["BUILD_SAMPLES"] = False
        cmake.definitions["CMAKE_MODULE_PATH"] = getcwd()
        cmake.definitions["CMAKE_VERBOSE_MAKEFILE"] = True
        cmake.configure()
        cmake.build()

    def package(self):
        root = "%s-%s" % (self.name, self.version)
        self.copy("license.txt",  dst=".", src=root)
        self.copy(pattern="*", dst="include", src=path.join(root, "Release", "include"))
        self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=path.join(root, "Release", "Binaries"), keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src=path.join(root, "Release", "Binaries"), keep_path=False)

    def package_info(self):
        version_tokens = self.version.split(".")
        versioned_name = "cpprest_%s_%s" % (version_tokens[0], version_tokens[1])
        lib_name = versioned_name if self.settings.compiler == "Visual Studio" else "cpprest"
        self.cpp_info.libs.append(lib_name)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
