"""Validate GBA image structure; this does not certify boot or save/load."""
from pathlib import Path
import sys


def validate(data):
    errors = []
    if not 0xC0 <= len(data) <= 32 * 1024 * 1024:
        return ["ROM size is outside GBA bounds"]
    if data[0xB2] != 0x96:
        errors.append("Invalid fixed GBA header byte")
    if data[0xBD] != (-(sum(data[0xA0:0xBD]) + 0x19) & 0xFF):
        errors.append("Invalid GBA header complement checksum")
    if not data[0xA0:0xAC].startswith(b"TIDES DAWN"):
        errors.append("Unexpected ROM title")
    if data[0xAC:0xB0] != b"BPEE":
        errors.append("Unexpected game code")
    if data[:4] in {b"\0" * 4, b"\xff" * 4}:
        errors.append("Missing reset vector")
    if not any(marker in data for marker in (b"FLASH1M_V", b"FLASH_V", b"SRAM_V", b"EEPROM_V")):
        errors.append("No recognized save-library signature")
    return errors


if __name__ == "__main__":
    errors = validate(Path(sys.argv[1]).read_bytes())
    if errors:
        raise SystemExit("; ".join(errors))
    print("GBA image header, size and save signature valid. Emulator acceptance remains pending.")
