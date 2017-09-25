"""This script build Conan.io package to multiple platforms."""
from conan.packager import ConanMultiPackager
import platform


if __name__ == "__main__":
    builder = ConanMultiPackager(args="--build missing")
    builder.add_common_builds(shared_option_name="cpprestsdk:shared", pure_c=False)
    filtered_builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        # XXX (uilian.ries): MTd could not link
        if settings["compiler"] == "Visual Studio" and settings["compiler.runtime"] == "MTd":
            continue
        # XXX (uilian.ries): libstdc++ could not link on Linux
        if settings["compiler"] == "clang" and platform.system() == "Linux":
            settings["compiler.libcxx"] = "libc++"
        filtered_builds.append([settings, options, env_vars, build_requires])
    builder.builds = filtered_builds
    builder.run()
