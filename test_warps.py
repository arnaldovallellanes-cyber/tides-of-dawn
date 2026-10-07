import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("warps", ROOT / "tools/tides/validate_warps.py")
warps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(warps)
CONTRACT = json.loads((ROOT / "docs/tides-of-dawn/warp-contract.json").read_text())


def map_data(name, targets=(), indoor=False):
    return {"name": name, "id": "MAP_" + name.upper(),
            "map_type": "MAP_TYPE_INDOOR" if indoor else "MAP_TYPE_TOWN",
            "warp_events": [{"dest_map": "MAP_" + dest.upper(), "dest_warp_id": "0"} for dest in targets]}


class WarpTests(unittest.TestCase):
    def fixture(self):
        return [map_data("PuebloAlmendro", ["AlmendroHome"]),
                map_data("AlmendroHome", ["PuebloAlmendro"], True),
                map_data("PuertoBrisa", ["HarborHouse"]),
                map_data("HarborHouse", ["PuertoBrisa"], True),
                map_data("VillaMangle")]

    def test_correct_city_round_trips(self):
        self.assertEqual(warps.validate(self.fixture(), CONTRACT), ([], True))

    def test_original_puerto_brisa_wrong_house_regression(self):
        maps = self.fixture()
        maps[2]["warp_events"][0]["dest_map"] = "MAP_ALMENDROHOME"
        errors, _ = warps.validate(maps, CONTRACT)
        self.assertTrue(any("Forbidden warp" in e for e in errors))
        self.assertTrue(any("static interior exit leads to PuebloAlmendro" in e for e in errors))

    def test_harbor_house_wrong_exit(self):
        maps = self.fixture()
        maps[3]["warp_events"][0]["dest_map"] = "MAP_PUEBLOALMENDRO"
        errors, _ = warps.validate(maps, CONTRACT)
        self.assertTrue(any("HarborHouse must return exclusively" in e for e in errors))

    def test_invalid_destination_index(self):
        maps = self.fixture()
        maps[2]["warp_events"][0]["dest_warp_id"] = "3"
        self.assertTrue(any("warp 3 does not exist" in e for e in warps.validate(maps, CONTRACT)[0]))

    def test_missing_destination(self):
        maps = self.fixture()
        maps[2]["warp_events"][0]["dest_map"] = "MAP_MISSING"
        self.assertTrue(any("missing destination" in e for e in warps.validate(maps, CONTRACT)[0]))

    def test_second_floor_wrong_city(self):
        maps = self.fixture()
        maps[3]["warp_events"].append({"dest_map": "MAP_HARBORUPSTAIRS", "dest_warp_id": "0"})
        maps.append(map_data("HarborUpstairs", ["PuebloAlmendro"], True))
        self.assertTrue(any("static interior exit leads to PuebloAlmendro" in e for e in warps.validate(maps, CONTRACT)[0]))

    def test_missing_migration_is_not_a_pass(self):
        maps = [map_data("OldTown", ["OldHome"]), map_data("OldHome", ["OldTown"], True)]
        self.assertEqual(warps.validate(maps, CONTRACT), ([], False))
        self.assertTrue(warps.validate(maps, CONTRACT, True)[0])

    def test_dynamic_returns_are_not_static_city_ownership(self):
        maps = [map_data("OldTown", ["OldHome"]), map_data("OldHome", ["OldTown"], True)]
        maps[1]["warp_events"][0]["dest_warp_id"] = "WARP_ID_DYNAMIC"
        self.assertEqual(warps.validate(maps, CONTRACT), ([], False))


if __name__ == "__main__":
    unittest.main()
