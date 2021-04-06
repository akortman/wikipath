import Pathfinder
import Heuristic
import SubsetBuilder
import statistics
import json

def main():
    heuristics = {
        "bfs"       : Heuristic.no_heuristic,
        "cats"      : Heuristic.estimate_by_categories,
        "contribs"  : Heuristic.estimate_by_shared_contributors,
        "extract"   : Heuristic.estimate_by_shared_extract_words,
        "coords"    : Heuristic.estimate_by_coord_location
    }
    heuristic_performances = {}
    for heur in heuristics:
        heuristic_performances[heur] = []

    data_filename = "largeset.txt"
    output_filename = "output.txt"
    intermediate_output_file = "intermediate.txt"
    graphs = SubsetBuilder.load_from_file(data_filename)

    output = {}
    output["outputs"] = []

    for graph in graphs["data"]:
        result = {
            "root":graph["root"],
            "pairs":graph["pairs"],
            "means":{}
        }

        for pair in result['pairs']:
            pair["performance"] = {}
            pair["path_length"] = {}
            pair["path"] = {}

        for heur in heuristics:
            perf_list = []
            for pair in result["pairs"]:
                path = Pathfinder.pathfind(pair["start"], pair["end"], heuristics[heur], graph)
                if path == None:
                    pair["performance"][heur] = None
                    pair["path_length"][heur] = None
                    pair["path"][heur] = None
                    pair["path_not_found"] = ''
                else:
                    performance = path["explored"]
                    pair["performance"][heur] = performance
                    pair["path_length"][heur] = path["length"]
                    pair["path"][heur] = path["path"]
                    perf_list.append(performance)
                    heuristic_performances[heur].append(performance)

            # Calculate mean for this heuristic
            result["means"][heur] = statistics.mean(perf_list)

        output["outputs"].append(result)
        SubsetBuilder.write_to_file(output, intermediate_output_file)

    # Calculate overall mean for each heuristic
    output["overall_mean_performance"] = {}
    for heur in heuristics:
        output["overall_mean_performance"][heur] = statistics.mean(heuristic_performances[heur])

    # Calculate execution time for each heuristic
    """
    output["mean_heuristic_execution_times"] = {}
    for heur in heuristics:
        output["mean_heuristic_execution_time"][heur] = statistics.mean(Heuristic.times[heur])
    """

    # Output to file
    SubsetBuilder.write_to_file(output, output_filename)

if __name__ == '__main__':
    main()
