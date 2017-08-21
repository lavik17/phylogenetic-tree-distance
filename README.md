# phylogenetic-tree-distance

Version 2.0
This script takes a Newick formatted tree and a list of taxa of interest.
The user can supply a distance threshold (default is 0.05)
The script will search for all taxa within a distance smaller than the threshold
Three files will be created:
1. List of all matches
2. List of matches without taxa that are found in the user provided list
3. List of taxa that were missing from the tree

Syntax:

  tree-distance.py -t <tree.nwk> -l <list.txt> -v [threshold]

-t Newick tree file  

-l List of taxa of interest, each taxon in a new line
