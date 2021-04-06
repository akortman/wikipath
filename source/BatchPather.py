"""
    while true,
    produce a subset of pathing data
    pathfind across it's pairs
    output a file containing performance data
"""

import Pathfinder
import Heuristic
import SubsetBuilder
import WikiReq
import json
from statistics import mean
from random import choice 
import string

valid_chars = "-_.()%s%s" % (string.ascii_letters, string.digits)
cycle = -1

while True:
    cycle += 1
    try:
        # Randomly generate data.
        root = WikiReq.random_page()
        params = {
            #"size":choice([32,48,64]),
            "size":200,
            "branch":choice([1,1,2,4])
        }
        pairs = 8

        graph = SubsetBuilder.build_datasource(root, 20, params)
        #print(json.dumps(graph, indent = 4))

        # Path and get pathing data
        heuristics = {
            "bfs"           : Heuristic.no_heuristic,
            "cats"          : Heuristic.estimate_by_categories,
            "contribs"      : Heuristic.estimate_by_shared_contributors,
            "extract"       : Heuristic.estimate_by_shared_extract_words,
            "coords"        : Heuristic.estimate_by_coord_location,
            "extract_caps"  : Heuristic.estimate_by_capitalised_words
        }

        result = {
            "root":root,
            "pairs":graph["pairs"],
            "means":{}
        }

        for pair in result['pairs']:
            pair["performance"] = {}
            pair["path"] = {}
            pair["path_length"] = {}

        for heur in heuristics:
            perf_list = []
            for pair in result['pairs']:
                path = Pathfinder.pathfind(pair['start'], pair['end'], heuristics[heur], graph)
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
            result['means'][heur] = mean(perf_list)


        # Output to file
        SubsetBuilder.write_to_file(result,
            "./outputs_overnight_01/pathdata_"
            + str(cycle)
            + "_"
            + ''.join(c for c in root.replace(" ", "_") if c in valid_chars) # Formatted root as filename
            + "_s"
            + str(params["size"])
            + "_b"
            + str(params["branch"])
            + ".txt"
        )

        print(" *** ")
        print(" *** CONSTRUCTION OF DATA FOR {cycle} COMPLETE".format(**locals()))
        print(" *** ")

    except ConnectionError:
        continue
    except:
        raise
