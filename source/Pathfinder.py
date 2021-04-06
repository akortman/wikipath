import WikiReq
import Heuristic
import SubsetBuilder

def pathfind(start, end, heuristic, graph):
    print("Finding path between {start} and {end} with heuristic {heuristic}.".format(**locals()))

    # Set up A* search variables
    #start = start.replace(' ', '_')
    fringe = [start]        # The fringe contains articles we can explore
    page_costs = {start:0}  # page_costs maps explored articles to their costs (to get from start to the article)
    f_values = {}           # f_values contains f = g + h (known + estimate) costs for each article explorable
    came_from = {}          # came_from maps explored articles to where we got to the article from

    # Pathfinder control loop
    path_found = False
    while not path_found:
        if not fringe:
            print("Path not found.")
            return None

        # Get the article to visit next: The node in fringe with the lowest f_value
        min_estimate = float('inf')

        current = None

        for page in fringe:
            # If the f-value for page is not yet calculated, calculate it and add it to f_values
            if page not in f_values:
                f_values[page] = page_costs[page] + heuristic(page, end)
            if f_values[page] < min_estimate:
                current = page
                min_estimate = f_values[page]

        # Expand current article
        links = WikiReq.get_links(current)

        # Remove the expanded article from the fringe
        fringe.remove(current)

        print("Expanding '", current, "' with ", len(links), ' links, ', len(fringe), ' in fringe beforehand', sep='')
       
        for link in links:
            if link in fringe or link in came_from:
                continue

            if link not in graph["subset"]:
                continue
            print(" !!! Adding {}, in the graph, to fringe".format(link))

            # Replace spaces in link with underscore

            # Update path and cost data
            page_costs[link] = page_costs[current] + 1
            came_from[link] = current
            fringe.append(link)

            if link == end:
                path_found = True
                break

    # Rebuilt path
    path = [end]
    while path[0] != start:
        path.insert(0, came_from[path[0]])

    print('Path found: ', path, sep='')

    path_data = {
        "path":path,
        "length":len(path),
        "explored":len(list(came_from.keys()))
    }

    return path_data

def main():
    # Do a single pathfind
    start = "Australia"
    end = "Animal worship"
    heur = Heuristic.estimate_by_shared_extract_words
    print("Pathfinding between {start} and {end} using heuristic {heur}.".format(**locals()))
    graph_filename = "source.txt"
    graph = SubsetBuilder.load_from_file(graph_filename)
    path = pathfind(start, end, heur, graph)
    print(path)

if __name__ == '__main__':
    main()