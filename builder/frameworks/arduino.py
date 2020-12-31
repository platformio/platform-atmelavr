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
Arduino

Arduino Wiring-based Framework allows writing cross-platform software to
control devices attached to a wide range of Arduino boards to create all
kinds of creative coding, interactive objects, spaces or physical experiences.

http://arduino.cc/en/Reference/HomePage
"""

from os.path import isdir, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()
build_core = board.get("build.core", "")

FRAMEWORK_DIR = platform.get_package_dir("framework-arduino-avr")
if build_core in ("dtiny", "pro"):
    FRAMEWORK_DIR = platform.get_package_dir("framework-arduino-avr-digistump")
elif build_core in ("tiny", "tinymodern"):
    FRAMEWORK_DIR = platform.get_package_dir("framework-arduino-avr-attiny")
elif build_core != "arduino":
    FRAMEWORK_DIR = platform.get_package_dir(
        "framework-arduino-avr-%s" % build_core.lower())

assert isdir(FRAMEWORK_DIR)


def get_bootloader_size():
    max_size = board.get("upload.maximum_size")
    if max_size > 4096 and max_size <= 32768:
        return 512
    elif max_size >= 65536 or board.get("build.mcu").startswith("at90can32"):
        return 1024
    return 0


CPPDEFINES = [
    ("F_CPU", "$BOARD_F_CPU"),
    "ARDUINO_ARCH_AVR",
    ("ARDUINO", 10808)
]

if "build.usb_product" in board:
    CPPDEFINES += [
        ("USB_VID", board.get("build.hwids")[0][0]),
        ("USB_PID", board.get("build.hwids")[0][1]),
        ("USB_PRODUCT", '\\"%s\\"' %
         board.get("build.usb_product", "").replace('"', "")),
        ("USB_MANUFACTURER", '\\"%s\\"' %
         board.get("vendor", "").replace('"', ""))
    ]

env.Append(
    ASFLAGS=["-x", "assembler-with-cpp"],

    CFLAGS=[
        "-std=gnu11",
        "-fno-fat-lto-objects"
    ],

    CCFLAGS=[
        "-Os",  # optimize for size
        "-Wall",  # show warnings
        "-ffunction-sections",  # place each function in its own section
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

    LINKFLAGS=[
        "-Os",
        "-mmcu=$BOARD_MCU",
        "-Wl,--gc-sections",
        "-flto",
        "-fuse-linker-plugin"
    ],

    CPPDEFINES=CPPDEFINES,

    LIBS=["m"],

    LIBSOURCE_DIRS=[
        join(FRAMEWORK_DIR, "libraries")
    ],

    CPPPATH=[
        join(FRAMEWORK_DIR, "cores", build_core)
    ]
)

#
# Take into account bootloader size
#

if (
    build_core in ("MiniCore", "MegaCore", "MightyCore", "MajorCore")
    and board.get("hardware.uart", "uart0") != "no_bootloader"
):
    upload_section = board.get("upload")
    upload_section["maximum_size"] -= board.get(
        "bootloader.size", get_bootloader_size()
    )
# copy CCFLAGS to ASFLAGS (-x assembler-with-cpp mode)
env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])

#
# Target: Build Core Library
#

libs = []

if "build.variant" in board:
    variants_dir = join(
        "$PROJECT_DIR", board.get("build.variants_dir")) if board.get(
            "build.variants_dir", "") else join(FRAMEWORK_DIR, "variants")

    env.Append(
        CPPPATH=[
            join(variants_dir, board.get("build.variant"))
        ]
    )
    libs.append(env.BuildLibrary(
        join("$BUILD_DIR", "FrameworkArduinoVariant"),
        join(variants_dir, board.get("build.variant"))
    ))

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkArduino"),
    join(FRAMEWORK_DIR, "cores", build_core)
))

env.Prepend(LIBS=libs)
