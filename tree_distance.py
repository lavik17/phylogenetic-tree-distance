#!/usr/bin/python


# Needs the following files:
# tree.nwk - Newick formatted tree file
# taxa-list.txt - List of taxa to check


import sys, getopt, csv, subprocess
from ete3 import Tree

#get the arguments from the user
def userhelp():
	print ()
	print ()
	print ()
	print ('The script takes a newick tree, list of taxa, and a uses a set distance of 0.5')
	print ('The output is taxa-output.csv')
	print ()
	print ('Syntax: tree-distance.py -t <tree.nwk> -l <list.txt>')
	print ()
	print ('-t Newick tree file')
	print ('-l List of taxa of interest, each taxon in a new line')
	
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
	threshold = 0.05
	listfile = list_file
	# read in newick tree
	t = Tree(tree_file)

	# read in list of taxa into a dictionary
	# first create a dictionary
	nearby_leaves = {}
	nearby_leaves_nr = {}
	
	with open(listfile) as file:
		for line in file:
			indicator = line.strip()
			#set the distance counter to zero
			distance = float(0)
			#jump to that taxon in the tree
			target = t&indicator
			#see who is the parent of the taxon in question
			nearby_leaves [indicator]=[]
			for leaf in t:
				distance = target.get_distance(leaf)
				if distance <= threshold:
					nearby_leaves[indicator].append(leaf.name)
	
	# remove taxa hits that are present in the taxa list file 
	nearby_leaves_nr = nearby_leaves
	with open(listfile) as file:
		for line in file:
			print (line)
			for key,value in nearby_leaves_nr.items():
				for v in value:
					if v == line.strip():
						value.remove(v)
					
						
	#write the output file
	with open('taxa-output.csv', 'wb') as csv_file:
		w = csv.writer(open('taxa-output.csv', "w"))
		for key, val in nearby_leaves.items():
			w.writerow([key, val])     
	csv_file.close()

	#write the output-nr file
	with open('taxa-output-nr.csv', 'wb') as csv_file:
		w = csv.writer(open('taxa-output-nr.csv', "w"))
		for key, val in nearby_leaves_nr.items():
			w.writerow([key, val])     
	csv_file.close()
	
#start the main body of the script
#get the arguments
if __name__ == "__main__":
    main(sys.argv[1:])
