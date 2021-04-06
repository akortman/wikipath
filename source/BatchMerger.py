import glob
import SubsetBuilder
from statistics import mean

folder = "dataset"
heuristics = [
    "bfs",
    "cats",
    "contribs",
    "extract",
    "coords",
    "extract_caps"
]
paircount = 0
means = {}
samples = {}
for heur in heuristics:
    means[heur] = []
    samples[heur] = []

for f in glob.glob("./" + folder + "/*.txt"):
    data = SubsetBuilder.load_from_file(f)
    paircount += len(data["pairs"])
    for heur in heuristics:
        means[heur].append(data["means"][heur])
        for pair in data["pairs"]:
            samples[heur].append(pair["performance"][heur])
    print("{}".format(f))

result = {
    "mean_performance":{}
}

for heur in heuristics:
    result["mean_performance"][heur] = mean(samples[heur])

result["files"] = len(glob.glob("./" + folder + "/*.txt"))
result["paircount"] = paircount

SubsetBuilder.write_to_file(result, "merged_data.txt")
print(" *** ")
print(" *** Parsing complete: {} files, {} pairs.".format(len(glob.glob("./" + folder + "/*.txt")), paircount))
print(" *** ")
