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

from platformio.managers.platform import PlatformBase


class AtmelavrPlatform(PlatformBase):

    def configure_default_packages(self, variables, targets):
        if variables.get("board"):
            board_config = self.board_config(variables.get("board"))
            disabled_tool = "tool-micronucleus"
            required_tool = ""

            if "digispark" in board_config.get("build.core", ""):
                disabled_tool = "tool-avrdude"

            if "fuses" in targets:
                required_tool = "tool-avrdude"

            if required_tool in self.packages:
                self.packages[required_tool]['optional'] = False

            if disabled_tool in self.packages and \
                    disabled_tool != required_tool:
                del self.packages[disabled_tool]

        return PlatformBase.configure_default_packages(self, variables,
                                                       targets)

    def on_run_err(self, line):  # pylint: disable=R0201
        # fix STDERR "flash written" for avrdude
        if "avrdude" in line:
            self.on_run_out(line)
        else:
            PlatformBase.on_run_err(self, line)
