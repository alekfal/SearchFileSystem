#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 15:02:16 2019

@author: Gounari Olympia
"""

import os
from os import walk

 
def treeSearch(searchPath, startsWith, contains, endsWith):
    """Search for files under the given searchPath.

    Args:
    searchPath (string): From where searching starts.
    startsWith (string): Prefix of wanted filename.
    contains (string): Text contained in wanted filename.
    endsWith (string): Ending of wanted filename.

    Returns:
    itemsFound (list of strings): Found files fullpaths.
    """
    itemsFound = []
    # Search every directory under the searchPath
    for (dirpath, dirnames, filenames) in walk(searchPath):
        for filename in filenames:
            if filename.startswith(startsWith) and filename.endswith(endsWith) and contains in filename:
                print(filename)
                itemsFound.append(dirpath+'/'+filename)

    itemsFound = sorted(itemsFound)
    # Check if searching has been completed successfully
    if not itemsFound:
        print("No items found ...")
    else:
        return itemsFound



def findRecord(searchPath, satPath, satRow, year):
    """
    searchPath = string. Path from where to start searching.
    satPath, satRow = string. Tile path-row, each as 3 digit number.
    year = string or integer. The year searching for.
    recPaths = list of paths of differend records (dates) for the requested
                tile.
    """
    # Check requested path and row, as given from user
    if len(str(satPath)) != 3:
        print('Please supply Path with three digits in total.\ne.g. 081')
    if len(str(satRow)) != 3:
        print('Please supply Row with three digits in total.\ne.g. 036')
    
    recPaths = []
    # Search every directory under the searchPath
    for (dirpath, dirnames, filenames) in walk(searchPath):
        # For every folder
        for dirname in dirnames:
            # If folder includes path-row and date
            if str(satPath)+str(satRow)+'_'+str(year) in dirname:
                # Gather paths to folders.
                recPaths.append(dirpath+'/'+dirname)
    recPaths = sorted(recPaths)
    # Check if searching has been completed successfully
    if not recPaths:
        print("No record-paths found ...")
    else:
        return recPaths
    


def findBand(recPaths, pattern):
    """
    recPaths = list of paths or files.
    pattern = string. End of path or file we are looking for. For files, must
            include format.
    paths = list of paths or files found. Paths should be absolute.
    
    Find folders or files, ending by pattern.
    """
    paths = []
    # Check if recPaths is a directory path
    if os.path.isdir(recPaths[0]):
        # For each record-folder
        for i in range(len(recPaths)):
            # Walk all filesystem-tree branches
            for (dirpath, dirnames, filenames) in walk(recPaths[i]):
                # For every image that ends with requested pattern
                for file in filenames:
                    if file.endswith(str(pattern)):
                        # Add image's path to the list
                        paths.append(dirpath+'/'+file)  
    # Check if recPaths is a file path
    elif os.path.isfile(recPaths[0]):
        # For every image that ends with requested pattern
        for file in recPaths:
            if file.endswith(str(pattern)):
                # Add image's path to the list
                paths.append(os.path.abspath(file))
    else:
        print("function findBand() -> recPaths isn't path or file")
    # Sort images based on date and band-names (ascending)
    paths = sorted(paths)
    print('For pattern "{}", found {} results.'.format(pattern, len(paths)))
    return paths