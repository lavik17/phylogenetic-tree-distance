# phylogenetic-tree-distance
returns all leaves that are at an X distance from a list of other leaves

The script takes a newick tree, list of taxa, and a uses a hardcoded distance of 0.5
The output is taxa-output.csv

Syntax: 
  tree-distance.py -t <tree.nwk> -l <list.txt>

-t Newick tree file')
-l List of taxa of interest, each taxon in a new line


Needed upgrades:
Ask the user for distance
Ask the user for the name of output file
