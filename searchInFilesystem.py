#!/usr/bin/env python3
# -*- coding: utf-8 -*-



def treeSearch(searchPath, startsWith, contains, endsWith, sort=True):
    """ Search for files under the given searchPath.

    Args:
    searchPath (string): From where searching starts.
    startsWith (string): Prefix of wanted filename.
    contains (string): Text contained in wanted filename.
    endsWith (string): Ending or file-format of wanted filename.
    sort (boolean, optional): True by default, sorts itemsFound by date.

    Return:
    itemsFound (list of strings): List with fullpaths of itemsFound, sorted be date.
    """
    from os import walk

    itemsFound = []
    # Search every directory under the searchPath.
    for (dirpath, dirnames, filenames) in walk(searchPath):
        for filename in filenames:
            if filename.startswith(startsWith) and filename.endswith(endsWith) and contains in filename:
                itemsFound.append(dirpath+'/'+filename)
    
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

    # Check if searching has been completed successfully.
    if not itemsFound:
        print("No items found ...")
    else:
        return (itemsFound)



def metaSearch(searchPath, lessThan):
    """ Select fullpaths of Sentinel-2 scenes, by cloud coverage. Reads
    MTD.xml metadata file. Keep images with cloud coverage less than given percentage.

    Args:
    searchPath (string): From where searching starts.
    lessThan (float): Cloud coverage value to campare with.

    Return:
    itemsFound (list of strings): List with fullpaths of itemsFound, sorted be date.
    """
    import xml.etree.ElementTree as ET

    # Find all metadata files in given directory.
    possiblePaths = treeSearch(searchPath, 'MTD', 'L2A', '.xml', sort=True)

    itemsFound = []
    for f in possiblePaths:
        root = ET.parse(f).getroot()
        pref = root[3].tag  # Quality_Indicators_Info
        field = root.find(pref)[0]  # Cloud_Coverage_Assessment
        value = field.text
        if float(value) <= float(lessThan):
            path = f.split('.SAFE')[0] + '.SAFE'
            itemsFound.append(path)

            #print("{} --> Image accepted...".format(value))
        else:
            #print("{} --> Image not accepted...".format(value))
            pass
    
    return itemsFound



def findBand(searchPath, pattern, sort=True):
    """ Search for files under the given searchPath, ending by pattern.

    Args:
    searchPath (string): From where searching starts.
    pattern (string): End of path or file looking for. For files, must include format.
    sort (boolean, optional): True by default, sorts itemsFound by date.

    Return:
    itemsFound (list of strings): List with fullpaths of itemsFound, sorted be date.
    """
    import os
    from os import walk

    itemsFound = []
    # Check if searchPath is a directory path.
    if os.path.isdir(searchPath[0]):
        # Walk all filesystem-tree branches.
        for (dirpath, dirnames, filenames) in walk(searchPath):
            # For every image that ends with requested pattern.
            for file in filenames:
                if file.endswith(str(pattern)):
                    # Add image's path to the list.
                    itemsFound.append(dirpath+'/'+file)  
    # Check if searchPath is a file path
    elif os.path.isfile(searchPath[0]):
        # For every image that ends with requested pattern.
        for file in searchPath:
            if file.endswith(str(pattern)):
                # Add image's path to the list.
                itemsFound.append(os.path.abspath(file))
    else:
        print("function findBand() -> searchPath isn't path or file")

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

    # Check if searching has been completed successfully.
    if not itemsFound:
        print("No items found ...")
    else:
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
                itemsFound.append(dirpath+'/'+dirname)

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
        satPath, satRow, endsWith, len(itemsFound)))

    # Check if searching has been completed successfully.
    if not itemsFound:
        print("No items found ...")
    else:
        return (itemsFound)