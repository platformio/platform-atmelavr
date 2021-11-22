How to build PlatformIO based project
=====================================

1. [Install PlatformIO Core](http://docs.platformio.org/page/core.html)
2. Download [development platform with examples](https://github.com/platformio/platform-atmelavr/archive/develop.zip)
3. Extract ZIP archive
4. Run these commands:

```shell
# Change directory to example
$ cd platform-atmelavr/examples/simba-blink

# Process example project
$ pio run

# Upload firmware to Arduino Uno
$ pio run --environment arduino_uno --target upload
```
