"""Compile actual starter lookup functions on the host, without claiming a GBA build."""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


@unittest.skipUnless(shutil.which("gcc"), "Host gcc is required")
class StarterResolutionTests(unittest.TestCase):
    def test_actual_c_lookup_handles_all_starters_forms_and_invalid_choices(self):
        source = (ROOT / "src/starter_choose.c").read_text()
        defines = "\n".join(re.findall(r"^#define STARTER_(?:MON_COUNT|ZORUA_HISUI)\s+\d+", source, re.M))
        table = re.search(r"static const u16 sStarterMon\[.*?\n\};", source, re.S).group()
        lookup = re.search(r"u16 GetStarterPokemon\(.*?\n\}", source, re.S).group()
        item = re.search(r"u16 GetTidesStarterHeldItem\(.*?\n\}", source, re.S).group()
        # Symbolic host enums deliberately differ from the engine's species IDs.
        # The test compiles the implementation above instead of recreating its lookup logic.
        harness = r'''
#include <assert.h>
#include <stdint.h>
typedef uint16_t u16;
enum { HOST_SENTINEL, SPECIES_TREECKO, SPECIES_CHIMCHAR, SPECIES_FROAKIE,
       SPECIES_RIOLU, SPECIES_ZORUA, SPECIES_CHARCADET, SPECIES_ZORUA_HISUI };
enum { ITEM_NONE, ITEM_AUSPICIOUS_ARMOR, ITEM_MALICIOUS_ARMOR };
static u16 sStarterHeldItem;
'''
        harness += defines + "\n" + table + "\n" + lookup + "\n" + item
        harness += r'''
int main(void)
{
    assert(GetStarterPokemon(0) == SPECIES_TREECKO);
    assert(GetStarterPokemon(1) == SPECIES_CHIMCHAR);
    assert(GetStarterPokemon(2) == SPECIES_FROAKIE);
    assert(GetStarterPokemon(3) == SPECIES_RIOLU);
    assert(GetStarterPokemon(4) == SPECIES_ZORUA);
    assert(GetStarterPokemon(5) == SPECIES_CHARCADET);
    assert(GetStarterPokemon(6) == SPECIES_ZORUA_HISUI);
    assert(GetStarterPokemon(7) == SPECIES_TREECKO);
    assert(GetStarterPokemon(UINT16_MAX) == SPECIES_TREECKO);
    assert(GetTidesStarterHeldItem() == ITEM_NONE);
    sStarterHeldItem = ITEM_AUSPICIOUS_ARMOR;
    assert(GetTidesStarterHeldItem() == ITEM_AUSPICIOUS_ARMOR);
    sStarterHeldItem = ITEM_MALICIOUS_ARMOR;
    assert(GetTidesStarterHeldItem() == ITEM_MALICIOUS_ARMOR);
    return 0;
}
'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            (path / "starter_lookup.c").write_text(harness)
            subprocess.run(["gcc", "-std=c17", "-Wall", "-Wextra", "-Werror",
                            "-fsanitize=undefined", "-fno-sanitize-recover=all",
                            str(path / "starter_lookup.c"), "-o", str(path / "lookup")],
                           check=True, capture_output=True)
            subprocess.run([str(path / "lookup")], check=True, capture_output=True)


if __name__ == "__main__":
    unittest.main()
