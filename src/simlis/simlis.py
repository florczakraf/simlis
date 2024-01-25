import csv
import sys

from argparse import ArgumentParser
from pathlib import Path

import simfile

DIFF_MAP = {
    "Beginner": "B",
    "Easy": "E",
    "Medium": "M",
    "Hard": "H",
    "Challenge": "X",
}


def list_sims(pack):
    sims = []
    for sim in pack.simfiles():
        if isinstance(sim, simfile.SMSimfile):
            print(f"{sim.artist} - {sim.title}: Skipping SM file", file=sys.stderr)
            continue

        sim_data = {
            "Charter": [],
            "Song Title": sim.title,
            "Song Artist": sim.artist,
            "B": "",
            "B Tech": "",
            "E": "",
            "E Tech": "",
            "M": "",
            "M Tech": "",
            "H": "",
            "H Tech": "",
            "X": "",
            "X Tech": "",
        }

        for chart in sim.charts:
            if chart.difficulty == "EDIT":
                print(f"{sim.artist} - {sim.title}: skipping EDIT chart")

            diff = DIFF_MAP[chart.difficulty]
            sim_data["Charter"].append((diff, chart.credit))
            sim_data[diff] = chart.meter
            tech = [chart.chartname, chart.description]
            tech = ", ".join([x for x in tech if x])
            sim_data[f"{diff} Tech"] = tech

        if len(set([x[1] for x in sim_data["Charter"]])) == 1:
            sim_data["Charter"] = sim_data["Charter"][0][1]
        else:
            sim_data["Charter"] = ", ".join([f"{diff}: {charter}" for diff, charter in sim_data["Charter"]])

        sims.append(sim_data)

    return sims

def main():
    parser = ArgumentParser()
    parser.add_argument("path", help="Path to pack", default=Path("."), type=Path)
    parser.add_argument("-o", "--output", help="Path to output csv file", default=None, type=Path)
    args = parser.parse_args()

    pack = simfile.SimfilePack(args.path)

    sim_data = list_sims(pack)

    if args.output is None:
        args.output = Path(f"{pack.name}.csv")
        print(f"Saving output to {args.output}")

    with args.output.open("w", newline="") as csvfile:
        fields = ["Charter", "Song Title", "Song Artist", "B", "B Tech", "E", "E Tech", "M", "M Tech", "H", "H Tech", "X", "X Tech"]
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        for sim in sim_data:
            writer.writerow(sim)


if __name__ == '__main__':
    main()
