import hashlib
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
rom = root / "Tides_of_Dawn_Modern_Alpha.gba"
manifest = {
    "project": "Pokemon: Tides of Dawn / Mareas del Alba",
    "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
    "upstream": json.loads((root / "docs/tides-of-dawn/upstream.json").read_text()),
    "rom": rom.name,
    "sha256": hashlib.sha256(rom.read_bytes()).hexdigest(),
    "arm_gcc": subprocess.check_output(["arm-none-eabi-gcc", "--version"], text=True).splitlines()[0],
    "auralia_migration_received": (root / "data/maps/PuertoBrisa/map.json").exists(),
    "emulator_boot_validated": False,
    "save_load_validated": False,
    "all_auralia_house_returns_validated_in_emulator": False,
    "dual_active_abilities_implemented": False,
}
(root / "build-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
