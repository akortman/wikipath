import WikiReq
from math import radians, cos, sin, asin, sqrt
from random import random
import time

time_start = None

def start_timer():
    time_start = time.process_time()

def end_timer():
    if time_start == None:
        return None
    return time.process_time() - time_start()


times = {
    "bfs"       : [],
    "cats"      : [],
    "contribs"  : [],
    "extract"   : [],
    "coords"    : []
}

"""
    Contains heuristic methods for estimating the distance between two Wikipedia articles (returns
    a floating point value between 0.0 and 1.0.)
"""

"""
    Takes a list of shared values and returns a float between 0 and 1 representing a distance
    measure.
"""
def convert_shared_values_to_dist(shared):
    return 1 / (1 + len(shared))

def heuristic_generic_shared(start, end, heurfunc):
    print("Estimating distance between {} and {}".format(start, end))
    startvals = heurfunc(start)
    endvals = heurfunc(end)
    shared = [elem for elem in startvals if elem in endvals]
    return shared

"""
    Shared categories
    Assumption: A page that shares a category with the goal page is likely close to it.
    Definition:
        Let Shared = the number of categories that Current shares with Goal. 
        Estimate = 1/(1+Shared).
"""
def estimate_by_categories(start, end):
    heur = WikiReq.get_cats
    shared = heuristic_generic_shared(start, end, heur)
    estimate = convert_shared_values_to_dist(shared)
    print("\t{start} and {end} share {0} (dist {estimate}) categories: {shared}".format(len(shared), **locals()))

    return estimate

"""
    Shared contibutors
    Assumption: If a contributor has edited both the Current and Goal pages, they are likely to link to each other.
    Definition:
        Let SharedContribs = the number of contributors that have edited both Current and Goal.
        Estimate = 1/(1+SharedContribs).
"""
def estimate_by_shared_contributors(start, end):

    heur = WikiReq.get_contribs
    shared = heuristic_generic_shared(start, end, heur)
    estimate = convert_shared_values_to_dist(shared)
    print("\t{start} and {end} share {0} (dist {estimate}) contibutors: {shared}".format(len(shared), **locals()))

    return estimate

"""
    Shared extract words
    Assumption: If a contributor has edited both the Current and Goal pages, they are likely to link to each other.
    Definition:
        Let SharedContribs = the number of contributors that have edited both Current and Goal.
        Estimate = 1/(1+SharedContribs).
"""
def estimate_by_shared_extract_words(start, end):
    # Get extracts and split them into lists of words
    ext_start_words = str(WikiReq.get_extract(start)).split()
    ext_end_words   = str(WikiReq.get_extract(end)).split()
    #print("Words in start '{}': {}".format(start, ext_start_words))
    #print("Words in end '{}': {}".format(end, ext_end_words))

    # Reduce two lists into a list of shared words
    shared = [word for word in ext_start_words if word in ext_end_words]
    #print("Shared words: {}".format(shared))

    estimate = 1 / (1 + len(shared))
    #print("Estimate is {estimate}".format(**locals()))

    return estimate

def estimate_by_capitalised_words(start, end):
    # Get extracts and split them into lists of words
    ext_start_words = str(WikiReq.get_extract(start)).split()
    ext_end_words   = str(WikiReq.get_extract(end)).split()

    # Filter into 
    ext_start_words = [word for word in ext_start_words if len(word) > 0 and word[0].isupper()]
    ext_end_words   = [word for word in ext_end_words if len(word) > 0 and word[0].isupper()]
    print("Capital words in start '{}': {}".format(start, ext_start_words))
    print("Capital words in end '{}': {}".format(end, ext_end_words))

    # Reduce two lists into a list of shared words
    shared = [word for word in ext_start_words if word in ext_end_words]
    print("Shared words: {}".format(shared))

    estimate = 1 / (1 + len(shared))
    #print("Estimate is {estimate}".format(**locals()))

    return estimate


# haversine() taken directly from http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km
# End of code sourced from http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points

def estimate_by_coord_location(start, end):
    start_coords = WikiReq.get_coords(start)
    end_coords = WikiReq.get_coords(end)

    if len(start_coords) == 0 or len(end_coords) == 0:
        print("No coordinate data on one of the pages, returning a max estimate of 1.0.")
        times["coords"].append(end_timer())
        return 1.0 # Maximum

    lon1 = float(start_coords["lon"])
    lat1 = float(start_coords["lat"])
    lon2 = float(end_coords["lon"])
    lat2 = float(end_coords["lat"])

    dist = haversine(lon1, lat1, lon2, lat2)
    earth_circumference = 40075 # km
    estimate = dist / earth_circumference

    print("Distance between {start} and {end} is {dist}, producing an estimate of {estimate}".format(**locals()))
   
    return estimate

def no_heuristic(start, end):
    estimate = 0

    return estimate

def main():
    estimate_by_capitalised_words("Australia", "Dog")
    pass

if __name__ == "__main__":
    main()
