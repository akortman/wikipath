import WikiReq
import random
import json
import copy

"""
    Builds a subset of interconnected wikipedia articles.
    Algorithm is in two steps: (1) tree widening and (2) random tree population
            (1) tree widening: for each element in the subset, expand it and add some number of
                links on it to the subset. Continue until we exceed some threshold W (< N).
            (2) random tree population: select a random page in the subset and follow a single link
                recursively some number of times, adding the selected pages to the subset.
    Parameters:
        size            The number of pages to build the subset out of.
        branch          The amount of links to expand on each page in each iteration in (1).
        trees           The number of (potentially unconnected) trees that make up the subset.
                        Also the size of starting_pages.
        widening_thresh The threshold at which we switch to step 2. Less than size.
        pop_depth       The number of times to follow links in step (2).
"""

default_params = {
    "size": 150,
    "branch": 5,
    "widening_thresh": 70,
    "pop_depth": 7
}

def build_graph(root, params = default_params):
    # An object representing the graph space
    gspace = {
        "root":root,
        "came_from":{root:None},
    }
    gspace["subset"] = list(gspace["came_from"].keys())

    # (1) Tree widening
    index = 0
    while len(gspace["subset"]) < params["size"]:
        page = gspace["subset"][index]
        print("Expanding up to {} links on page '{}'.".format(params["branch"], page))

        # Select "branch" links at random from the links on the next page
        all_links = WikiReq.get_links(page)

        links = None

        if len(all_links) < params["branch"]:
            links = all_links
        else:
            links = random.sample(all_links, params["branch"])
        
        # Move from links into the subset if it is unique
        for l in links:
            if l not in gspace["subset"]:
                gspace["subset"].append(l)
                gspace["came_from"][l] = page

        index += 1
        index %= len(gspace["subset"])

    return gspace

def build_datasource(root, pairs, params = default_params):
    graph = build_graph(root, params)
    graph["pairs"] = []

    # Create "pairs" start-end search pairs that are valid in the graph
    longpairs = pairs//2            # Pairs from graph root to any page in graph
    shortpairs = pairs - longpairs  # Pairs between any two known-to-be-interlinked pages
    
    for i in range(longpairs):
        endpt = random.choice(graph["subset"][1:-1])
        graph["pairs"].append({"start":root, "end":endpt})

    for i in range(shortpairs):
        endpt = random.choice(graph["subset"][1:-1])
        path = []
        nextpage = endpt
        while nextpage != root:
            nextpage = graph["came_from"][nextpage]
            path.append(nextpage)
        path.append(root)

        origin = random.choice(path)
        graph["pairs"].append({"start":origin, "end":endpt})

    return graph

def write_to_file(graph, filename):
    output_json = json.dumps(graph, indent=4)

    with open(filename, 'w') as f:
        f.write(output_json)

def load_from_file(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())

def main():
    params = {
        "size":32,
        "branch":2,
        "pairs":12
    }

    roots = [
        "Australia",
        "Porpoise",
        "2007 United States Air Force nuclear weapons incident",
        "Iain Banks",
        "Wikipedia"
    ]

    output_file = "largeset.txt"

    # Build a dataset for each root
    graphs = {"data":[]}
    for root in roots:
        print("Building subset of {} starting at page {}.".format(params["size"], root))
        datasource = build_datasource(root, params["pairs"], params)
        datasource["root"] = root
        graphs["data"].append(datasource)
    print(json.dumps(graphs, indent=4))
    write_to_file(graphs, output_file)
    return

      
if __name__ == '__main__':
    main()
