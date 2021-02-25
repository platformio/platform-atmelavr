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

import sys
from os.path import join
from time import sleep

from SCons.Script import (
    ARGUMENTS,
    COMMAND_LINE_TARGETS,
    AlwaysBuild,
    Builder,
    Default,
    DefaultEnvironment,
)

from platformio.util import get_serial_ports


def BeforeUpload(target, source, env):  # pylint: disable=W0613,W0621
    upload_options = {}
    if "BOARD" in env:
        upload_options = env.BoardConfig().get("upload", {})

    # Deprecated: compatibility with old projects. Use `program` instead
    if "usb" in env.subst("$UPLOAD_PROTOCOL"):
        upload_options["require_upload_port"] = False
        env.Replace(UPLOAD_SPEED=None)

    if env.subst("$UPLOAD_SPEED"):
        env.Append(UPLOADERFLAGS=["-b", "$UPLOAD_SPEED"])

    # extra upload flags
    if "extra_flags" in upload_options:
        env.Append(UPLOADERFLAGS=upload_options.get("extra_flags"))

    # disable erasing by default
    env.Append(UPLOADERFLAGS=["-D"])

    if upload_options and not upload_options.get("require_upload_port", False):
        return

    env.AutodetectUploadPort()
    env.Append(UPLOADERFLAGS=["-P", '"$UPLOAD_PORT"'])

    if env.subst("$BOARD") in ("raspduino", "emonpi", "sleepypi"):

        def _rpi_sysgpio(path, value):
            with open(path, "w") as f:
                f.write(str(value))

        if env.subst("$BOARD") == "raspduino":
            pin_num = 18
        elif env.subst("$BOARD") == "sleepypi":
            pin_num = 22
        else:
            pin_num = 4

        _rpi_sysgpio("/sys/class/gpio/export", pin_num)
        _rpi_sysgpio("/sys/class/gpio/gpio%d/direction" % pin_num, "out")
        _rpi_sysgpio("/sys/class/gpio/gpio%d/value" % pin_num, 1)
        sleep(0.1)
        _rpi_sysgpio("/sys/class/gpio/gpio%d/value" % pin_num, 0)
        _rpi_sysgpio("/sys/class/gpio/unexport", pin_num)
    else:
        if not upload_options.get("disable_flushing", False) and not env.get(
            "UPLOAD_PORT", ""
        ).startswith("net:"):
            env.FlushSerialBuffer("$UPLOAD_PORT")

        before_ports = get_serial_ports()

        if upload_options.get("use_1200bps_touch", False):
            env.TouchSerialPort("$UPLOAD_PORT", 1200)

        if upload_options.get("wait_for_upload_port", False):
            env.Replace(UPLOAD_PORT=env.WaitForNewSerialPort(before_ports))


env = DefaultEnvironment()
env.SConscript("compat.py", exports="env")

env.Replace(
    AR="avr-gcc-ar",
    AS="avr-as",
    CC="avr-gcc",
    GDB="avr-gdb",
    CXX="avr-g++",
    OBJCOPY="avr-objcopy",
    RANLIB="avr-gcc-ranlib",
    SIZETOOL="avr-size",
    ARFLAGS=["rc"],
    SIZEPROGREGEXP=r"^(?:\.text|\.data|\.bootloader)\s+(\d+).*",
    SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.noinit)\s+(\d+).*",
    SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
    SIZEPRINTCMD="$SIZETOOL --mcu=$BOARD_MCU -C -d $SOURCES",
    PROGSUFFIX=".elf",
)

env.Append(
    BUILDERS=dict(
        ElfToEep=Builder(
            action=env.VerboseAction(
                " ".join(
                    [
                        "$OBJCOPY",
                        "-O",
                        "ihex",
                        "-j",
                        ".eeprom",
                        '--set-section-flags=.eeprom="alloc,load"',
                        "--no-change-warnings",
                        "--change-section-lma",
                        ".eeprom=0",
                        "$SOURCES",
                        "$TARGET",
                    ]
                ),
                "Building $TARGET",
            ),
            suffix=".eep",
        ),
        ElfToHex=Builder(
            action=env.VerboseAction(
                " ".join(
                    ["$OBJCOPY", "-O", "ihex", "-R", ".eeprom", "$SOURCES", "$TARGET"]
                ),
                "Building $TARGET",
            ),
            suffix=".hex",
        ),
    )
)

# Allow user to override via pre:script
if env.get("PROGNAME", "program") == "program":
    env.Replace(PROGNAME="firmware")

if not env.get("PIOFRAMEWORK"):
    env.SConscript("frameworks/_bare.py", exports="env")

#
# Target: Build executable and linkable firmware
#

target_elf = None
if "nobuild" in COMMAND_LINE_TARGETS:
    target_elf = join("$BUILD_DIR", "${PROGNAME}.elf")
    target_firm = join("$BUILD_DIR", "${PROGNAME}.hex")
else:
    target_elf = env.BuildProgram()
    target_firm = env.ElfToHex(join("$BUILD_DIR", "${PROGNAME}"), target_elf)

AlwaysBuild(env.Alias("nobuild", target_firm))
target_buildprog = env.Alias("buildprog", target_firm, target_firm)

#
# Target: Print binary size
#

target_size = env.AddPlatformTarget(
    "size",
    target_elf,
    env.VerboseAction("$SIZEPRINTCMD", "Calculating size $SOURCE"),
    "Program Size",
    "Calculate program size",
)

#
# Target: Upload by default .hex file
#

upload_protocol = env.subst("$UPLOAD_PROTOCOL")

if upload_protocol == "micronucleus":
    env.Replace(
        UPLOADER="micronucleus",
        UPLOADERFLAGS=[
            "--no-ansi",
            "--run",
            "--timeout",
            "60"
        ],
        UPLOADCMD="$UPLOADER $UPLOADERFLAGS $SOURCES",
    )
    upload_actions = [env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")]

elif upload_protocol == "custom":
    upload_actions = [env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")]

else:
    env.Replace(
        UPLOADER="avrdude",
        UPLOADERFLAGS=[
            "-p",
            "$BOARD_MCU",
            "-C",
            join(
                env.PioPlatform().get_package_dir("tool-avrdude") or "", "avrdude.conf"
            ),
            "-c",
            "$UPLOAD_PROTOCOL",
        ],
        UPLOADCMD="$UPLOADER $UPLOADERFLAGS -U flash:w:$SOURCES:i",
        UPLOADEEPCMD="$UPLOADER $UPLOADERFLAGS -U eeprom:w:$SOURCES:i",
    )

    if int(ARGUMENTS.get("PIOVERBOSE", 0)):
        env.Prepend(UPLOADERFLAGS=["-v"])

    upload_actions = [
        env.VerboseAction(BeforeUpload, "Looking for upload port..."),
        env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE"),
    ]


env.AddPlatformTarget("upload", target_firm, upload_actions, "Upload")

#
# Target: Upload EEPROM data (from EEMEM directive)
#

env.AddPlatformTarget(
    "uploadeep",
    join("$BUILD_DIR", "${PROGNAME}.eep")
    if "nobuild" in COMMAND_LINE_TARGETS
    else env.ElfToEep(target_elf),
    [
        env.VerboseAction(BeforeUpload, "Looking for upload port..."),
        env.VerboseAction("$UPLOADEEPCMD", "Uploading $SOURCE"),
    ],
    "Upload EEPROM",
)

#
# Deprecated target: Upload firmware using external programmer
#

if "program" in COMMAND_LINE_TARGETS:
    sys.stderr.write(
        "Error: The `program` target is deprecated. To use a programmer for uploading "
        "firmware specify custom `upload_command`.\n"
        "More information: https://docs.platformio.org/en/latest/platforms/"
        "atmelavr.html#upload-using-programmer\n")
    env.Exit(1)

#
# Target: Setup fuses
#

fuses_action = None
if "fuses" in COMMAND_LINE_TARGETS:
    fuses_action = env.SConscript("fuses.py", exports="env")
env.AddPlatformTarget("fuses", None, fuses_action, "Set Fuses")

#
# Target: Upload bootloader
#

bootloader_actions = None
if "bootloader" in COMMAND_LINE_TARGETS:
    bootloader_actions = env.SConscript("bootloader.py", exports="env")
env.AddPlatformTarget("bootloader", None, bootloader_actions, "Burn Bootloader")

#
# Setup default targets
#

Default([target_buildprog, target_size])
