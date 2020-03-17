# Sen2Tools

Tools to manipulate Sentinel-2 satellite data.

## Module searchInFilesystem

### treeSearch(searchPath, startsWith, contains, endsWith, sort=True)

Search for files under the given searchPath.

Args:
* searchPath (string): From where searching starts.
* startsWith (string): Prefix of wanted filename.
* contains (string): Text contained in wanted filename.
* endsWith (string): Ending or file-format of wanted filename.
* sort (boolean, optional): True by default, sorts itemsFound by date.

Return:
* itemsFound (list of strings): List with fullpaths of itemsFound, sorted be date.


---------------------------------------------------------------------


### metaSearch(searchPath, lessThan)

Select fullpaths of Sentinel-2 scenes, by cloud coverage. \
Reads MTD.xml metadata file. \
Keep images with cloud coverage less than given percentage.

Args:
* searchPath (string): From where searching starts.
* lessThan (float): Cloud coverage value to campare with.

Return:
* itemsFound (list of strings): List with fullpaths of itemsFound, sorted be date.


---------------------------------------------------------------------


### findBand(searchPath, pattern, sort=True)

Search for files under the given searchPath, ending by pattern.

Args:
* searchPath (string): From where searching starts.
* pattern (string): End of path or file looking for. For files, must include format.
* sort (boolean, optional): True by default, sorts itemsFound by date.

Return:
* itemsFound (list of strings): List with fullpaths of itemsFound, sorted be date.


---------------------------------------------------------------------


### findRecord(searchPath, satPath, satRow, year, sort=True)

Search for Sentinel-2 scene folders, by satellite's path, row & year.

Args:
* searchPath (string): From where searching starts.
* satPath, satRow (string): Tile path-row, each as 3 digit number.
* year (string or integer: Year searching for.
* sort (boolean, optional): True by default, sorts itemsFound by date.

Return:
* itemsFound (list of strings): List with fullpaths of itemsFound, sorted be date.