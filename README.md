# Atmel AVR: development platform for [PlatformIO](http://platformio.org)
[![Build Status](https://travis-ci.org/platformio/platform-atmelavr.svg?branch=develop)](https://travis-ci.org/platformio/platform-atmelavr)
[![Build status](https://ci.appveyor.com/api/projects/status/ympddo5w1osqx6qr/branch/develop?svg=true)](https://ci.appveyor.com/project/ivankravets/platform-atmelavr/branch/develop)

Atmel AVR 8- and 32-bit MCUs deliver a unique combination of performance, power efficiency and design flexibility. Optimized to speed time to market-and easily adapt to new ones-they are based on the industrys most code-efficient architecture for C and assembly programming.

* [Home](http://platformio.org/platforms/atmelavr) (home page in PlatformIO Platform Registry)
* [Documentation](http://docs.platformio.org/page/platforms/atmelavr.html) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](http://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](http://docs.platformio.org/page/projectconf.html) file:

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

Please navigate to [documentation](http://docs.platformio.org/page/platforms/atmelavr.html).
