import sys
from os.path import join

from SCons.Script import COMMAND_LINE_TARGETS, Import, Return

Import("env")


def get_lfuse(target, f_cpu, oscillator, bod, eesave, ckout):
    targets_1 = (
        "atmega2561",
        "atmega2560",
        "atmega1284",
        "atmega1284p",
        "atmega1281",
        "atmega1280",
        "atmega644a",
        "atmega644p",
        "atmega640",
        "atmega328",
        "atmega328p",
        "atmega324a",
        "atmega324p",
        "atmega324pa",
        "atmega168",
        "atmega168p",
        "atmega164a",
        "atmega164p",
        "atmega88",
        "atmega88p",
        "atmega48",
        "atmega48p",
    )
    targets_2 = (
        "atmega328pb",
        "atmega324pb",
        "atmega168pb",
        "atmega162",
        "atmega88pb",
        "atmega48pb",
        "at90can128",
        "at90can64",
        "at90can32",
    )
    targets_3 = (
        "atmega8535",
        "atmega8515",
        "atmega128",
        "atmega64",
        "atmega32",
        "atmega16",
        "atmega8",
    )
    targets_4 = ("attiny13", "attiny13a")

    ckout_bit = 1 if ckout == "yes" else 0
    ckout_offset = ckout_bit << 6

    if target in targets_1:
        if oscillator == "external":
            return 0xF7 & ~ckout_offset
        elif oscillator == "external_clock":
            return 0xE0 & ~ckout_offset
        else:
            if f_cpu == "8000000L":
                return 0xE2 & ~ckout_offset
            else:
                return 0x62 & ~ckout_offset

    elif target in targets_2:
        if oscillator == "external":
            return 0xFF & ~ckout_offset
        elif oscillator == "external_clock":
            return 0xE0 & ~ckout_offset
        else:
            if f_cpu == "8000000L":
                return 0xE2 & ~ckout_offset
            else:
                return 0x62 & ~ckout_offset

    elif target in targets_3:
        if bod == "4.0v":
            bod_bits = 0b11
        elif bod == "2.7v":
            bod_bits = 0b01
        else:
            bod_bits = 0b00

        bod_offset = bod_bits << 6
        if oscillator == "external":
            return 0xFF & ~bod_offset
        elif oscillator == "external_clock":
            return 0xE0 & ~bod_offset
        else:
            if f_cpu == "8000000L":
                return 0xE4 & ~bod_offset
            else:
                return 0xE1 & ~bod_offset

    elif target in targets_4:
        eesave_bit = 1 if eesave == "yes" else 0
        eesave_offset = eesave_bit << 6
        if oscillator == "external" or oscillator == "external_clock":
            return 0x78 & ~eesave_offset
        else:
            if f_cpu == "9600000L":
                return 0x7A & ~eesave_offset
            elif f_cpu == "4800000L":
                return 0x79 & ~eesave_offset
            elif f_cpu == "1200000L":
                return 0x6A & ~eesave_offset
            elif f_cpu == "600000L":
                return 0x69 & ~eesave_offset
            elif f_cpu == "128000L":
                return 0x7B & ~eesave_offset
            elif f_cpu == "16000L":
                return 0x6B & ~eesave_offset

    else:
        sys.stderr.write("Error: Couldn't calculate lfuse for %s\n" % target)
        env.Exit(1)


def get_hfuse(target, uart, oscillator, bod, eesave, jtagen):
    targets_1 = (
        "atmega2561",
        "atmega2560",
        "atmega1284",
        "atmega1284p",
        "atmega1281",
        "atmega1280",
        "atmega644a",
        "atmega644p",
        "atmega640",
        "atmega324a",
        "atmega324p",
        "atmega324pa",
        "atmega324pb",
        "at90can128",
        "at90can64",
        "at90can32",
    )
    targets_2 = ("atmega328", "atmega328p", "atmega328pb")
    targets_3 = ("atmega164a", "atmega164p", "atmega162")
    targets_4 = (
        "atmega168",
        "atmega168p",
        "atmega168pb",
        "atmega88",
        "atmega88p",
        "atmega88pb",
        "atmega48",
        "atmega48p",
        "atmega48pb",
    )
    targets_5 = ("atmega128", "atmega64", "atmega32")
    targets_6 = ("atmega8535", "atmega8515", "atmega16", "atmega8")
    targets_7 = ("attiny13", "attiny13a")

    eesave_bit = 1 if eesave == "yes" else 0
    eesave_offset = eesave_bit << 3
    ckopt_bit = 1 if oscillator == "external" else 0
    ckopt_offset = ckopt_bit << 4
    jtagen_bit = 1 if jtagen == "yes" else 0
    jtagen_offset = jtagen_bit << 6

    if target in targets_1:
        if uart == "no_bootloader":
            return 0xDF & ~jtagen_offset & ~eesave_offset
        else:
            return 0xDE & ~jtagen_offset & ~eesave_offset

    elif target in targets_2:
        if uart == "no_bootloader":
            return 0xDF & ~eesave_offset
        else:
            return 0xDE & ~eesave_offset

    elif target in targets_3:
        if uart == "no_bootloader":
            return 0xDD & ~jtagen_offset & ~eesave_offset
        else:
            return 0xDC & ~jtagen_offset & ~eesave_offset

    elif target in targets_4:
        if bod == "4.3v":
            return 0xDC & ~eesave_offset
        elif bod == "2.7v":
            return 0xDD & ~eesave_offset
        elif bod == "1.8v":
            return 0xDE & ~eesave_offset
        else:
            return 0xDF & ~eesave_offset

    elif target in targets_5:
        if uart == "no_bootloader":
            return 0xDF & ~jtagen_offset & ~ckopt_offset & ~eesave_offset
        else:
            return 0xDE & ~jtagen_offset & ~ckopt_offset & ~eesave_offset

    elif target in targets_6:
        if uart == "no_bootloader":
            return 0xDD & ~ckopt_offset & ~eesave_offset
        else:
            return 0xDC & ~ckopt_offset & ~eesave_offset

    elif target in targets_7:
        if bod == "4.3v":
            return 0x9
        elif bod == "2.7v":
            return 0xFB
        elif bod == "1.8v":
            return 0xFD
        else:
            return 0xFF

    else:
        sys.stderr.write("Error: Couldn't calculate hfuse for %s\n" % target)
        env.Exit(1)


def get_efuse(target, uart, bod, cfd):

    targets_without_efuse = (
        "atmega8535",
        "atmega8515",
        "atmega8",
        "atmega16",
        "atmega32",
        "attiny13a",
        "attiny13",
    )
    targets_1 = (
        "atmega2561",
        "atmega2560",
        "atmega1284",
        "atmega1284p",
        "atmega1281",
        "atmega1280",
        "atmega644a",
        "atmega644p",
        "atmega640",
        "atmega328",
        "atmega328p",
        "atmega324a",
        "atmega324p",
        "atmega324pa",
        "atmega164a",
        "atmega164p",
    )
    targets_2 = ("atmega328pb", "atmega324pb")
    targets_3 = (
        "atmega168",
        "atmega168p",
        "atmega168pb",
        "atmega88",
        "atmega88p",
        "atmega88pb",
    )
    targets_4 = ("atmega128", "atmega64", "atmega48", "atmega48p")
    targets_5 = ("at90can128", "at90can64", "at90can32")
    targets_6 = ("atmega162",)

    cfd_bit = 1 if cfd == "yes" else 0
    cfd_offset = cfd_bit << 3

    if target in targets_without_efuse:
        return None

    if target in targets_1:
        if bod == "4.3v":
            return 0xFC
        elif bod == "2.7v":
            return 0xFD
        elif bod == "1.8v":
            return 0xFE
        else:
            return 0xFF

    elif target in targets_2:
        if bod == "4.3v":
            return 0xF4 | cfd_offset
        elif bod == "2.7v":
            return 0xF5 | cfd_offset
        elif bod == "1.8v":
            return 0xF6 | cfd_offset
        else:
            return 0xF7

    elif target in targets_3:
        return 0xFD if uart == "no_bootloader" else 0xFC

    elif target in targets_4:
        return 0xFF

    elif target in targets_5:
        if bod == "4.1v":
            return 0xFD
        elif bod == "4.0v":
            return 0xFB
        elif bod == "3.9v":
            return 0xF9
        elif bod == "3.8v":
            return 0xF7
        elif bod == "2.7v":
            return 0xF5
        elif bod == "2.6v":
            return 0xF3
        elif bod == "2.5v":
            return 0xF1
        else:
            return 0xFF

    elif target in targets_6:
        if bod == "4.3v":
            return 0xF9
        elif bod == "2.7v":
            return 0xFB
        elif bod == "1.8v":
            return 0xFD
        else:
            return 0xFF

    else:
        sys.stderr.write("Error: Couldn't calculate efuse for %s\n" % target)
        env.Exit(1)


def is_target_without_bootloader(target):
    targets_without_bootloader = (
        "atmega48",
        "atmega48p",
        "attiny4313",
        "attiny2313",
        "attiny1634",
        "attiny861",
        "attiny841",
        "attiny461",
        "attiny441",
        "attiny261",
        "attiny167",
        "attiny88",
        "attiny87",
        "attiny85",
        "attiny84",
        "attiny48",
        "attiny45",
        "attiny44",
        "attiny43",
        "attiny40",
        "attiny26",
        "attiny25",
        "attiny24",
        "attiny13",
        "attiny13a",
    )

    return target in targets_without_bootloader


def get_lock_bits(target):
    if is_target_without_bootloader(target):
        return "0xff"
    else:
        return "0x0f"


board = env.BoardConfig()
platform = env.PioPlatform()
core = board.get("build.core", "")

target = (
    board.get("build.mcu").lower()
    if board.get("build.mcu", "")
    else env.subst("$BOARD").lower()
)

fuses_section = "fuses"
if "bootloader" in COMMAND_LINE_TARGETS:
    fuses_section = "bootloader"

lfuse = board.get("%s.lfuse" % fuses_section, "")
hfuse = board.get("%s.hfuse" % fuses_section, "")
efuse = board.get("%s.efuse" % fuses_section, "")
lock = board.get("%s.lock_bits" % fuses_section, get_lock_bits(target))
if "bootloader" in COMMAND_LINE_TARGETS:
    # A special case for unlocking chip to burn a new bootloader
    lock = board.get("%s.unlock_bits" % fuses_section, "0x3F")

if (not lfuse or not hfuse) and core not in (
    "MiniCore",
    "MegaCore",
    "MightyCore",
    "MajorCore",
    "MicroCore",
):
    sys.stderr.write(
        "Error: Dynamic fuses generation for %s is not supported."
        " Please specify fuses in platformio.ini\n" % target
    )
    env.Exit(1)

if core in ("MiniCore", "MegaCore", "MightyCore", "MajorCore", "MicroCore"):
    f_cpu = board.get("build.f_cpu", "16000000L").upper()
    oscillator = board.get("hardware.oscillator", "external").lower()
    bod = board.get("hardware.bod", "2.7v").lower()
    uart = board.get("hardware.uart", "uart0").lower()
    eesave = board.get("hardware.eesave", "yes").lower()
    jtagen = board.get("hardware.jtagen", "no").lower()
    ckout = board.get("hardware.ckout", "no").lower()
    cfd = board.get("hardware.cfd", "no").lower()

    print("\nTARGET CONFIGURATION:")
    print("---------------------")
    print("Target = %s" % target)
    print("Clock speed = %s" % f_cpu)
    print("Oscillator = %s" % oscillator)
    print("BOD level = %s" % bod)
    print("Save EEPROM = %s" % eesave)

    if target not in ("attiny13", "attiny13a"):
        print("UART port = %s" % uart)

    if target not in (
        "atmega8535",
        "atmega8515",
        "atmega128",
        "atmega64",
        "atmega32",
        "atmega16",
        "atmega8",
        "attiny13",
        "attiny13a",
    ):
        print("Clock output = %s" % ckout)

    if target in (
        "atmega2561",
        "atmega2560",
        "atmega1284",
        "atmega1284p",
        "atmega1281",
        "atmega1280",
        "atmega644a",
        "atmega644p",
        "atmega640",
        "atmega324a",
        "atmega324p",
        "atmega324pa",
        "atmega324pb",
        "at90can128",
        "at90can64",
        "at90can32",
        "atmega164a",
        "atmega164p",
        "atmega162",
        "atmega128",
        "atmega64",
        "atmega32",
    ):
        print("JTAG enable = %s" % jtagen)

    if target in ("atmega324pb", "atmega328pb"):
        print("CFD enable = %s" % cfd)

    print("---------------------")

    lfuse = lfuse or hex(get_lfuse(target, f_cpu, oscillator, bod, eesave, ckout))
    hfuse = hfuse or hex(get_hfuse(target, uart, oscillator, bod, eesave, jtagen))
    efuse = efuse or get_efuse(target, uart, bod, cfd)

env.Replace(
    FUSESUPLOADER="avrdude",
    FUSESUPLOADERFLAGS=[
        "-p",
        "$BOARD_MCU",
        "-C",
        '"%s"'
        % join(env.PioPlatform().get_package_dir("tool-avrdude") or "", "avrdude.conf"),
    ],
    FUSESFLAGS=[
        "-Ulock:w:%s:m" % lock,
        "-Uhfuse:w:%s:m" % hfuse,
        "-Ulfuse:w:%s:m" % lfuse,
    ],
    SETFUSESCMD="$FUSESUPLOADER $FUSESUPLOADERFLAGS $UPLOAD_FLAGS $FUSESFLAGS",
)

if not is_target_without_bootloader(target):
    env.Append(FUSESUPLOADERFLAGS=["-e"])

if env.subst("$UPLOAD_PROTOCOL") != "custom":
    env.Append(FUSESUPLOADERFLAGS=["-c", "$UPLOAD_PROTOCOL"])
else:
    print(
        "Warning: The `custom` upload protocol is used! The upload and fuse flags may "
        "conflict!\nMore information: "
        "https://docs.platformio.org/en/latest/platforms/atmelavr.html"
        "#overriding-default-fuses-command\n"
    )

if efuse:
    efuse = efuse if isinstance(efuse, str) else hex(efuse)
    env.Append(FUSESFLAGS=["-Uefuse:w:%s:m" % efuse])

print(
    "\nSelected fuses: [lfuse = %s, hfuse = %s%s]"
    % (lfuse, hfuse, ", efuse = %s" % efuse if efuse else "")
)

fuses_action = env.VerboseAction("$SETFUSESCMD", "Setting fuses")

Return("fuses_action")
