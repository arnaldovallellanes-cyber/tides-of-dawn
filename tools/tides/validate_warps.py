"""Check source warp targets and exclusive static city/interior returns."""
import argparse
from collections import deque
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
DYNAMIC_MAPS = {"MAP_DYNAMIC", "MAP_NONE"}
DYNAMIC_WARPS = {"WARP_ID_DYNAMIC", "-1", "255"}


def validate(maps, contract, require_auralia=False):
    errors = []
    by_id = {m["id"]: m for m in maps}
    by_name = {m["name"]: m for m in maps}
    if len(by_id) != len(maps) or len(by_name) != len(maps):
        errors.append("Duplicate map id or name")
    edges = {m["name"]: [] for m in maps}
    for m in maps:
        for index, w in enumerate(m.get("warp_events", [])):
            label = f"{m['name']} warp {index}"
            dest_id = w["dest_map"]
            if dest_id in DYNAMIC_MAPS:
                continue
            if dest_id not in by_id:
                errors.append(f"{label}: missing destination {dest_id}")
                continue
            dest = by_id[dest_id]
            target = str(w["dest_warp_id"])
            if target in DYNAMIC_WARPS:
                continue
            try:
                target_index = int(target)
            except ValueError:
                errors.append(f"{label}: unrecognized destination warp {target}")
                continue
            if not 0 <= target_index < len(dest.get("warp_events", [])):
                errors.append(f"{label}: {dest['name']} warp {target_index} does not exist")
                continue
            edges[m["name"]].append(dest["name"])

    towns = {m["name"] for m in maps if m.get("map_type") in {"MAP_TYPE_TOWN", "MAP_TYPE_CITY"}}
    towns.update(c for c in contract["cities"] if c in by_name)
    indoor = {m["name"] for m in maps if m.get("map_type") == "MAP_TYPE_INDOOR"}
    for town in sorted(towns):
        for house in set(edges[town]) & indoor:
            queue = deque([house])
            seen = set()
            while queue:
                current = queue.popleft()
                if current in seen:
                    continue
                seen.add(current)
                for dest in edges[current]:
                    if dest in towns and dest != town:
                        errors.append(f"{town} -> {house}: static interior exit leads to {dest}")
                    elif dest in indoor:
                        queue.append(dest)

    expected = set(contract["cities"]) | set(contract["interiors"])
    has_auralia = bool(expected & by_name.keys())
    if require_auralia or has_auralia:
        for name in sorted(expected - by_name.keys()):
            errors.append(f"Required Auralia map missing: {name}")
        for house, city in contract["interiors"].items():
            if house in edges and city in edges:
                exits = set(edges[house]) - indoor
                if city not in exits or exits - {city}:
                    errors.append(f"{house} must return exclusively to {city}; found {sorted(exits)}")
        for city, house in contract["required_round_trips"]:
            if city in edges and house in edges:
                if house not in edges[city] or city not in edges[house]:
                    errors.append(f"Required round trip missing: {city} -> {house} -> {city}")
        for origin, dest in contract["forbidden_edges"]:
            if dest in edges.get(origin, []):
                errors.append(f"Forbidden warp: {origin} -> {dest}")
    return sorted(set(errors)), has_auralia


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maps", type=Path, default=ROOT / "data/maps")
    parser.add_argument("--require-auralia", action="store_true")
    args = parser.parse_args()
    maps = [json.loads(p.read_text()) for p in sorted(args.maps.glob("*/map.json"))]
    if not maps:
        raise SystemExit("No source maps found; warp validation cannot pass.")
    contract = json.loads((ROOT / "docs/tides-of-dawn/warp-contract.json").read_text())
    errors, has_auralia = validate(maps, contract, args.require_auralia)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        raise SystemExit(1)
    print(f"Validated {len(maps)} maps: static destinations, indices and city returns.")
    if not has_auralia:
        print("Auralia migration absent: PuertoBrisa/HarborHouse contract remains PENDING.")


if __name__ == "__main__":
    main()
