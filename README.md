# Atmel AVR: development platform for [PlatformIO](https://platformio.org)

[![Build Status](https://github.com/platformio/platform-atmelavr/workflows/Examples/badge.svg)](https://github.com/platformio/platform-atmelavr/actions)

Atmel AVR 8- and 32-bit MCUs deliver a unique combination of performance, power efficiency and design flexibility. Optimized to speed time to market-and easily adapt to new ones-they are based on the industrys most code-efficient architecture for C and assembly programming.

* [Home](https://registry.platformio.org/platforms/platformio/atmelavr) (home page in the PlatformIO Registry)
* [Documentation](https://docs.platformio.org/page/platforms/atmelavr.html) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](https://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](https://docs.platformio.org/page/projectconf.html) file:

## Stable version

```ini
[env:stable]
platform = atmelavr
board = ...
...
```

## Development version

```ini
[env:development]
platform = https://github.com/platformio/platform-atmelavr.git
board = ...
...
```

# Configuration

Please navigate to [documentation](https://docs.platformio.org/page/platforms/atmelavr.html).
