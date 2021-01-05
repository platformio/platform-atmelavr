# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
RIOT

RIOT is a real-time multi-threading operating system that supports
a range of devices that are typically found in the Internet of Things (IoT):
8-bit, 16-bit and 32-bit microcontrollers.

https://www.riot-os.org
"""

from os.path import isdir, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board_config = env.BoardConfig()

FRAMEWORK_DIR = platform.get_package_dir("framework-riot")
assert isdir(FRAMEWORK_DIR)


env.Append(
    ASFLAGS=["-x", "assembler-with-cpp"],

    CFLAGS=[
        "-std=gnu11",
    ],

    CCFLAGS=[
        "-Os",
        "-Wall",
        "-ffunction-sections",
        "-fdata-sections",
        "-flto",
        "-mmcu=$BOARD_MCU"
    ],

    CXXFLAGS=[
        "-fno-exceptions",
        "-fno-threadsafe-statics",
        "-fpermissive",
        "-std=gnu++11"
    ],

    CPPDEFINES=[
        "RIOT"
    ],

    CPPPATH=[
        join(FRAMEWORK_DIR, "core", "include")
    ],

    LINKFLAGS=[
        "-Os",
        "-mmcu=$BOARD_MCU",
        "-Wl,--gc-sections"
    ],

    LIBS=["m"],
)

# copy CCFLAGS to ASFLAGS (-x assembler-with-cpp mode)
env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])

#
# Target: Build Core Library
#

libs = []

# Add sources as a static archive

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "RIOTCore"),
    join(FRAMEWORK_DIR, "core")
))

# Add sources as as object files

# env.BuildSources(
#     join("$BUILD_DIR", "RIOTCore"),
#     join(FRAMEWORK_DIR, "core")
# )

env.Prepend(LIBS=libs)
