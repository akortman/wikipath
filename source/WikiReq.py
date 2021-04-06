"""
The WikiReq module contains code to request data through the MediaWiki API.
"""

import requests
import json

link_cache = {}
category_cache = {}
contributor_cache = {}
extract_cache = {}
coord_cache = {}
session = requests.Session()

# Contains common code for generic retrieval of data
#   additional_params is extra parametes required
#   requested_item is the item in pages returned, i.e. "links" or "categories"
#   data_in_requested is the subitem that should be returned from the item
#   i.e. from each LINK you want a TITLE, should be "title"
def get_generic(pagename, additional_params, requested_item, data_in_requested, continue_flag, cache, url='https://en.wikipedia.org/w/api.php'):
    # Check if returned value is cached
    if pagename in cache:
        return cache[pagename]

    # Setup request parameters
    reqparams = {
        'action':'query',
        'prop':'',
        'titles':pagename,
        'format':'json',
        'redirects':''
    }
    reqparams.update(additional_params)

    result = []
    more = True

    while more:
        # Request the link data from the server
        while True:
            try:
                data_json = session.get(url, params=reqparams, timeout=1)
                break

            except:
                continue

        if data_json == None:
            break

        # Convert JSON data to py obj
        data = json.loads(data_json.text)

        # Check if there are more items after this
        if 'continue' in data:
            reqparams[continue_flag] = data['continue'][continue_flag]
        else:
            more = False

        # Return the extracted data
        if 'query' not in data:
            print("Error: query not in response:\n", data)
            return []

        pages = data['query']['pages']
        page = pages[list(pages.keys())[0]]

        # Check that the page exists
        if 'missing' in page or requested_item not in page:
            # Page is missing, return an empty list
            return []
        
        result_raw = page[requested_item]

        # result_raw is an array of dicts each with a desired element inside
        # Append each item to the list of items
        for res in result_raw:
            result.append(res[data_in_requested])

    cache[pagename] = result
    return result

def get_links(pagename):
    params = {
        'prop':'links',
        'pllimit':'max',
        'plnamespace':'0'
    }

    return get_generic(
        pagename            = pagename,
        additional_params   = params,
        requested_item      = "links",
        data_in_requested   = "title",
        continue_flag       = "plcontinue",
        cache               = link_cache
    )

# Get a random set of pages from Wikipedia
def random_page():
    # Setup request parameters
    reqparams = {
        'action':'query',
        'list':'random',
        'format':'json',
        'rnlimit':'1',
        'rnnamespace':'0'
    }

    # Get random page
    while True:
        try:
            data_json = session.get('https://en.wikipedia.org/w/api.php', params=reqparams, timeout=1)
            break
            
        except:
            continue

    # Extact page from json data
    data = json.loads(data_json.text)
    page = data['query']['random'][0]['title']

    return page

def get_cats(pagename):
    params = {
        'prop':'categories',
        'cllimit':'max',
    }

    return get_generic(
        pagename            = pagename,
        additional_params   = params,
        requested_item      = "categories",
        data_in_requested   = "title",
        continue_flag       = "clcontinue",
        cache               = category_cache
    )

def get_contribs(pagename):
    params = {
        'prop':'contributors',
        'pclimit':'max',
    }

    return get_generic(
        pagename            = pagename,
        additional_params   = params,
        requested_item      = "contributors",
        data_in_requested   = "userid",
        continue_flag       = "pccontinue",
        cache               = contributor_cache
    )

def get_images(pagename):
    pass

def get_coords(pagename):
    cache = coord_cache

    # Check if returned value is cached
    if pagename in cache:
        return cache[pagename]

    # Setup request parameters
    reqparams = {
        'action':'query',
        'prop':'coordinates',
        'titles':pagename,
        'colimit':'max',
        'format':'json',
        'coprop':'',
        'redirects':''
    }

    result = []

    # Request the link data from the server
    while True:
        try:
            data_json = session.get('https://en.wikipedia.org/w/api.php', params=reqparams, timeout=1)
            break
            
        except:
            continue

    if data_json == None:
        return []

    # Convert JSON data to py obj
    data = json.loads(data_json.text)

    # Return the extracted data
    if 'query' not in data:
        print("Error: query not in response:\n", data)
        return []

    pages = data['query']['pages']
    page = pages[list(pages.keys())[0]]

    # Check that the page exists
    if 'missing' in page or "coordinates" not in page or len(page["coordinates"]) == 0:
        # Page is missing, return an empty list
        return []

    result = page["coordinates"][0]
    del result["primary"]
    
    cache[pagename] = result
    return result

def get_extract(pagename):
    cache = extract_cache

    # Check if returned value is cached
    if pagename in cache:
        return cache[pagename]

    # Setup request parameters
    reqparams = {
        'action':'query',
        'titles':pagename,
        'format':'json',
        'prop':'extracts',
        'exsentences':'10',
        'exintro':'1',
        'explaintext':'1',
        'redirects':''
    }

    # Request the link data from the server
    while True:
            try:
                data_json = session.get('https://en.wikipedia.org/w/api.php', params=reqparams, timeout=1)
                break
                
            except:
                continue
            
    if data_json == None:
        return []

    # Convert JSON data to py obj
    data = json.loads(data_json.text)

    # Return the extracted data
    if 'query' not in data:
        print("Error: query not in response:\n", data)
        return []

    pages = data['query']['pages']
    page = pages[list(pages.keys())[0]]

    # Check that the page exists
    if 'missing' in page or "extract" not in page:
        # Page is missing, return an empty list
        return []

    result = page["extract"]
    print("Extract is: ", result)
    
    cache[pagename] = result

    return result

def main():
    print(get_coords("Australia"))

if __name__ == "__main__":
    main()