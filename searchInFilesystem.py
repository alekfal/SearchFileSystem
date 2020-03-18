#!/usr/bin/env python3
# -*- coding: utf-8 -*-



def findMore(searchPath, startsWith, contains, endsWith, mode, sort=True):
    """ Search for directories or files under the given searchPath.

    Args:
    searchPath (string): From where searching starts.
    startsWith (string): Prefix of wanted filename.
    contains (string): Text contained in wanted filename.
    endsWith (string): Ending or file-format of wanted filename.
    mode (int): 1 = search for dirs OR 2 = search for files.
    sort (boolean, optional): True by default, sorts itemsFound by date.

    Return:
    itemsFound (list of strings): List with fullpaths of itemsFound, sorted be date.
    """
    import os
    from os import walk

    itemsFound = []
    for (dirpath, dirnames, filenames) in walk(searchPath):
        # Search for directories.
        if mode == 1:
            for dirname in dirnames:
                if dirname.startswith(startsWith) and dirname.endswith(endsWith) and contains in dirname:
                    itemsFound.append(os.path.join(dirpath, dirname))

        # Search for files.
        elif mode == 2:
            for filename in filenames:
                if filename.startswith(startsWith) and filename.endswith(endsWith) and contains in filename:
                    itemsFound.append(os.path.join(dirpath, filename))
        else:
            print("Select search-mode, dir or file.")

    # Correctly sorted fullpaths, by date. 
    if sort == False:
        pass
    else:
        def get_pattern(oneFullpath):
            """ Returns the date extracted from Sentinel-2 fullpath filenames.
            """
            from datetime import datetime
            return datetime.strptime(oneFullpath.split('.SAFE')[0].split('_')[-1][0:8], '%Y%m%d')

        itemsFound = sorted(itemsFound, key=get_pattern)

    print("For given pattern '{}'*'{}'*'{}', found {} results...".format(
        startsWith, contains, endsWith, len(itemsFound)))

    return (itemsFound)




def metaSearch(searchPath, lessThan, verbose=False):
    """ Select fullpaths of Sentinel-2 scenes, by cloud coverage. Reads
    MTD.xml metadata file. Keep images with cloud coverage less than given percentage.

    Args:
    searchPath (string): From where searching starts.
    lessThan (float): Cloud coverage value to campare with.
    verbose (boolean, optional): True by default, print accepted of rejected dates.

    Return:
    itemsFound (list of strings): List with fullpaths of itemsFound, sorted be date.
    """
    import xml.etree.ElementTree as ET

    # Find all metadata files in given directory.
    possiblePaths = findMore(searchPath, 'MTD', 'L2A', '.xml', 2, sort=True)

    itemsFound = []
    for f in possiblePaths:
        root = ET.parse(f).getroot()
        pref = root[3].tag  # Quality_Indicators_Info
        field = root.find(pref)[0]  # Cloud_Coverage_Assessment
        value = field.text
        if float(value) <= float(lessThan):
            path = f.split('.SAFE')[0] + '.SAFE'
            itemsFound.append(path)

            if verbose == True:
                print("{} --> Image accepted...".format(value))
        else:
            if verbose == True:
                print("{} --> Image rejected...".format(value))
            pass
    
    return itemsFound




def find(searchPath, pattern, mode, sort=True):
    """ Search for directories or files under the given searchPath, ending by pattern.

    Args:
    searchPath (string): From where searching starts.
    pattern (string): End of path or file looking for. For files, must include format.
    mode (int): 1 = search for dirs OR 2 = search for files.
    sort (boolean, optional): True by default, sorts itemsFound by date.

    Return:
    itemsFound (list of strings): List with fullpaths of itemsFound, sorted be date.
    """
    import os
    from os import walk

    itemsFound = []
    for (dirpath, dirnames, filenames) in walk(searchPath):
        # Search for directories.
        if mode == 1:
            for dirname in dirnames:
                if dirname.endswith(str(pattern)):
                    itemsFound.append(os.path.join(dirpath, dirname))

        # Search for files.
        elif mode == 2:
            for filename in filenames:
                if filename.endswith(str(pattern)):
                    itemsFound.append(os.path.join(dirpath, filename))
        else:
            print("Select search-mode, dir or file.")

    # Correctly sorted fullpaths, by date. 
    if sort == False:
        pass
    else:
        def get_pattern(oneFullpath):
            """ Returns the date extracted from Sentinel-2 fullpath filenames.
            """
            from datetime import datetime
            return datetime.strptime(oneFullpath.split('.SAFE')[0].split('_')[-1][0:8], '%Y%m%d')

        itemsFound = sorted(itemsFound, key=get_pattern)

    print("For pattern '{}', found {} results.".format(pattern, len(itemsFound)))

    return (itemsFound)




def findRecord(searchPath, satPath, satRow, year, sort=True):
    """ Search for Sentinel-2 scene folders, by satellite's path, row & year.

    Args:
    searchPath (string): From where searching starts.
    satPath, satRow (string): Tile path-row, each as 3 digit number.
    year (string or integer: Year searching for.
    sort (boolean, optional): True by default, sorts itemsFound by date.

    Return:
    itemsFound (list of strings): List with fullpaths of itemsFound, sorted be date.
    """
    import os
    from os import walk

    # Check requested path and row, as given from user.
    if len(str(satPath)) != 3:
        print('Please supply Path with three digits in total.\ne.g. 081')
    if len(str(satRow)) != 3:
        print('Please supply Row with three digits in total.\ne.g. 036')
    
    itemsFound = []
    # Search every directory under the searchPath.
    for (dirpath, dirnames, filenames) in walk(searchPath):
        # For every folder
        for dirname in dirnames:
            # If folder includes path-row and date.
            if str(satPath)+str(satRow)+'_'+str(year) in dirname:
                # Gather paths to folder.
                itemsFound.append(os.path.join(dirpath, dirname))

    # Correctly sorted fullpaths, by date. 
    if sort == False:
        pass
    else:
        def get_pattern(oneFullpath):
            """ Returns the date extracted from Sentinel-2 fullpath filenames.
            """
            from datetime import datetime
            return datetime.strptime(oneFullpath.split('.SAFE')[0].split('_')[-1][0:8], '%Y%m%d')

        itemsFound = sorted(itemsFound, key=get_pattern)

    print("For given pattern '{}' * '{}' * '{}', found {} results...".format(
        satPath, satRow, year, len(itemsFound)))

    return (itemsFound)