#!/usr/bin/python


# Needs the following files:
# tree.nwk - Newick formatted tree file
# taxa-list.txt - List of taxa to check


import sys, getopt, csv, subprocess
from ete3 import Tree
from collections import defaultdict

#get the arguments from the user
def userhelp():
	print('\n\n\nThe script takes a newick tree, list of taxa, and a uses a set distance of 0.5')
	print('The output is taxa-output.csv')
	print('\nSyntax: tree-distance.py -t <tree.nwk> -l <list.txt>')
	print('\n-t Newick tree file')
	print('-l List of taxa of interest, each taxon in a new line')
	
#get the arguments from the user
def main(argv):
	tree_file = ''
	list_file = ''
	try:
		opts, args = getopt.getopt(argv,'ht:l:s',['help','tree','list'])
	except getopt.GetoptError:
		userhelp()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			userhelp()
			sys.exit()
		elif opt in ('-t', '--tree'):
			tree_file = arg
		elif opt in ('-l', '--list'):
			list_file = arg
		else:
			userhelp()
			sys.exit(2)

	#Set a distance threshold value
	threshold = 0.1
	listfile = list_file
	# read in newick tree
	t = Tree(tree_file)

	# read in list of taxa into a dictionary
	# first create a dictionary
	nearby_leaves = = defaultdict(list)
	nearby_leaves_nr = = {}
	notfound_leaves = = defaultdict(list)
	
				
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
    main(sys.argv[1:])
