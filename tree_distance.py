#!/usr/bin/env python3

# Version 2.0
# This script takes a Newick formatted tree and a list of taxa of interest.
# The user can supply a distance threshold (default is 0.05)
# The script will search for all taxa within a distance smaller than the threshold
# Three files will be created:
# 1. List of all matches
# 2. List of matches without taxa that are found in the user provided list
# 3. List of taxa that were missing from the tree

# Needs the following files:
# tree.nwk - Newick formatted tree file
# taxa-list.txt - List of taxa to check


import sys
import csv
import argparse
from ete3 import Tree
from collections import defaultdict

#get the arguments from the user
def main(**kwargs):
	
	tree_file=kwargs["tree"]
	listfile=kwargs["list"]
	threshold=kwargs["value"]
	
	print('\n\nStarting search for taxa with distance of up to %f' % threshold)
	# read in newick tree
	t = Tree(tree_file)

	# read in list of taxa into a dictionary
	# first create a dictionary
	nearby_leaves = defaultdict(list)
	nearby_leaves_nr = {}
	notfound_leaves = defaultdict(list)
	
				
	with open(listfile) as file:
		for line in file:
			indicator = line.strip()
			#set the distance counter to zero
			distance = float(0)
			#jump to that taxon in the tree
			try:
				# 'target = t&indicator' This is a shortcut that can replace the following line:
				target = t.search_nodes(name=indicator)[0]
				print('Looking at taxon : %s' % target) 
				#see who is the parent of the taxon in question
				for leaf in t:
					distance = target.get_distance(leaf)
					if distance <= threshold:
						nearby_leaves [indicator].append(leaf.name)
			except:
				notfound_leaves [indicator].append('Not found in tree') 
				print('Not found : %s' % indicator)			
				
	# remove taxa hits that are present in the taxa list file 
	nearby_leaves_nr = nearby_leaves
	with open(listfile) as file:
		for line in file:
			for key,value in nearby_leaves_nr.items():
				for v in value:
					if v == line.strip():
						value.remove(v)
						
	print('\n\nDone searching\n')					
	
	#write the output file
	print('Writing taxa-output.csv')
	with open('taxa-output.csv', 'wb') as csv_file:
		w = csv.writer(open('taxa-output.csv', "w"))
		for key, val in nearby_leaves.items():
			w.writerow([key, val])     
	csv_file.close()

	print('writing taxa-output-nr.csv')
	#write the output-nr file
	with open('taxa-output-nr.csv', 'wb') as csv_file:
		w = csv.writer(open('taxa-output-nr.csv', "w"))
		for key, val in nearby_leaves_nr.items():
			w.writerow([key, val])     
	csv_file.close()
	
	print('Writing taxa-notfound.csv')
	#write the output-nr file
	with open('taxa-notfound.csv', 'wb') as csv_file:
		w = csv.writer(open('taxa-notfound.csv', "w"))
		for key, val in notfound_leaves.items():
			w.writerow([key, val])     
	csv_file.close()
	
	print('\nAll done!')
#start the main body of the script
#get the arguments
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Picks all taxa that are at X distance from list of other taxa")
	parser.add_argument("-t", "--tree", type=str, required=True, help="Newick tree file")
	parser.add_argument("-l", "--list", type=str, required=True, help="List of taxa to search")
	parser.add_argument("-v", "--value", nargs="?", const="0.05", type=float, required=False, help="Distance threshold as fraction. Default is 0.05")
	args = parser.parse_args() 
	main(tree=args.tree, list=args.list, value=args.value)
