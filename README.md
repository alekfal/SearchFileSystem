# SearchFileSystem

Searching filesystem for Satellite data files

### Functions

#### treeSearch(searchPath, startsWith, contains, endsWith)

Search for files under the given searchPath.
Args:

* searchPath (string): From where searching starts.
* startsWith (string): Prefix of wanted filename.
* contains (string): Text contained in wanted filename.
* endsWith (string): Ending of wanted filename.

Returns:

* itemsFound (list of strings): Found files fullpaths.

---------------------------------------------------------------------