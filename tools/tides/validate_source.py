"""Reject incomplete checkouts or builds outside the pinned modern source history."""
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_COMMIT = "bb1093a7c72d3961d9a37d8e02ad2abc2c866682"
REQUIRED = (
    "Makefile", "config.mk", "ld_script_modern.ld", "data/event_scripts.s",
    "include/constants/species.h", "include/constants/items.h",
    "src/pokemon.c", "src/battle_main.c", "src/starter_choose.c",
)


def validate(root):
    errors = [f"Missing source: {name}" for name in REQUIRED if not (root / name).is_file()]
    lock = json.loads((root / "docs/tides-of-dawn/upstream.json").read_text())
    if lock["commit"] != EXPECTED_COMMIT or lock["tag"] != "expansion/1.17.1":
        errors.append("Source lock does not match the required Expansion 1.17.1 commit")
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", EXPECTED_COMMIT, "HEAD"],
        cwd=root, capture_output=True,
    )
    if result.returncode != 0:
        errors.append("Pinned Expansion commit is not an ancestor of this checkout")
    return errors


if __name__ == "__main__":
    errors = validate(ROOT)
    if errors:
        raise SystemExit("\n".join(errors))
    print("Complete modern source present; Expansion 1.17.1 ancestry verified.")
