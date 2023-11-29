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

from platformio.public import PlatformBase


class AtmelavrPlatform(PlatformBase):

    def configure_default_packages(self, variables, targets):
        if not variables.get("board"):
            return super().configure_default_packages(variables, targets)

        build_core = variables.get(
            "board_build.core", self.board_config(variables.get("board")).get(
                "build.core", "arduino"))

        if "arduino" in variables.get(
                "pioframework", []) and build_core != "arduino":

            framework_package = "framework-arduino-avr-%s" % build_core.lower()
            if build_core in ("dtiny", "pro"):
                framework_package = "framework-arduino-avr-digistump"
            elif build_core in ("tiny", "tinymodern"):
                framework_package = "framework-arduino-avr-attiny"

            if build_core in (
                "MiniCore",
                "MegaCore",
                "MightyCore",
                "MajorCore",
                "MicroCore",
            ):
                self.packages["tool-avrdude"]["version"] = "~1.70200.0"

            self.frameworks["arduino"]["package"] = framework_package
            self.packages[framework_package]["optional"] = False
            self.packages["framework-arduino-avr"]["optional"] = True

        upload_protocol = variables.get(
            "upload_protocol",
            self.board_config(variables.get("board")).get(
                "upload.protocol", ""))
        disabled_tool = "tool-micronucleus"
        required_tool = ""

        if upload_protocol == "micronucleus":
            disabled_tool = "tool-avrdude"

        if "fuses" in targets or "bootloader" in targets:
            required_tool = "tool-avrdude"

        if required_tool in self.packages:
            self.packages[required_tool]["optional"] = False

        if disabled_tool in self.packages and disabled_tool != required_tool:
            del self.packages[disabled_tool]

        return super().configure_default_packages(variables, targets)

    def on_run_err(self, line):  # pylint: disable=R0201
        # fix STDERR "flash written" for avrdude
        if "avrdude" in line:
            self.on_run_out(line)
        else:
            super().on_run_err(line)

    def get_boards(self, id_=None):
        result = super().get_boards(id_)
        if not result:
            return result
        if id_:
            return self._add_default_debug_tools(result)
        else:
            for key, value in result.items():
                result[key] = self._add_default_debug_tools(result[key])
        return result

    def _add_default_debug_tools(self, board):
        debug = board.manifest.get("debug", {})
        build = board.manifest.get("build", {})
        if "tools" not in debug:
            debug["tools"] = {}

        if debug.get("simavr_target", ""):
            debug["tools"]["simavr"] = {
                "init_cmds": [
                    "define pio_reset_halt_target",
                    "   monitor reset halt",
                    "end",
                    "define pio_reset_run_target",
                    "   monitor reset",
                    "end",
                    "target remote $DEBUG_PORT",
                    "$INIT_BREAK",
                    "$LOAD_CMDS"
                ],
                "port": ":1234",
                "server": {
                    "package": "tool-simavr",
                    "arguments": [
                        "-g",
                        "-m", debug["simavr_target"],
                        "-f", build.get("f_cpu", "")
                    ],
                    "executable": "bin/simavr"
                }
            }
        if debug.get("avr-stub", ""):
            speed = debug["avr-stub"]["speed"]
            debug["tools"]["avr-stub"] = {
                "init_cmds": [
                    "define pio_reset_halt_target",
                    "   monitor reset",
                    "end",
                    "define pio_reset_run_target",
                    "end",
                    "set remotetimeout 1",
                    "set serial baud {0}".format(speed),
                    "set remote hardware-breakpoint-limit 8",
                    "set remote hardware-watchpoint-limit 0",
                    "target remote $DEBUG_PORT"
                ],
                "init_break": "",
                "load_cmd": "preload",
                "require_debug_port": True,
                "default": False
            }

        board.manifest["debug"] = debug
        return board
