#!/usr/bin/python

'''
This tool uses an orthology group txt file output from OrthoMCl to extract
fasta accessions from a goodProteins.fa file.
'''

from sets import Set
import sys,argparse
from collections import defaultdict
import re

#-----------------------------------------------------
# Step 1
# Import variables & load input files
#-----------------------------------------------------

ap = argparse.ArgumentParser()
ap.add_argument('--orthogroups',required=True,type=str,help='text file output of OrthoMCl orthogroups')
ap.add_argument('--fasta',required=True,type=str,help='the fasta file of proteins used for the orthology analysis.')
ap.add_argument('--out_dir',required=True,type=str,help='the directory where fasta files containing orthogroups will be written ')
conf = ap.parse_args()

with open(conf.orthogroups) as f:
    ortho_lines = f.readlines()

with open(conf.fasta) as f:
    fasta_lines = f.readlines()

#-----------------------------------------------------
# Step 2
# Build a dictionary of orthogroups
#-----------------------------------------------------

ortho_dict = defaultdict(list)
for line in ortho_lines:
    line = line.rstrip()
    split_line = line.split()
    orthogroup = split_line[0].replace('orthogroup', '')
    orthogroup = orthogroup.replace(':', '')
    for gene in split_line[1:]:
        ortho_dict[orthogroup].append(gene)

#-----------------------------------------------------
# Step 3
# Extract fasta accessions for orthogroups
#-----------------------------------------------------
# For each orthogroups, add the constituent genes to
# a set. Go through the fasta file identifying any
# fasta accessions that match the name. For each match
# append the fasta accession to a list ready to be
# printed. Then remove that title from the set. Once
# the set is empty, finish the search. If the bottom
# of the file is reached before then print an error
# showing unfound elements in the set.
# Following each orthogroup, print the found accessions
# into a fasta file named by the orthogroup into the
# directory specified at stdin.

    #-----------------------------------------------------
    # Step 3a - Function A
    # extract_func
    # Extract fasta sequences that match orthogroup
    # contents
    #-----------------------------------------------------
    # Overview:
    #
    #-----------------------------------------------------

def extract_func(group_name):
    print ("Extracting fasta sequences from orthogroup: " + str(group_name))
    outlines=[]
    ortho_set = Set([])
    i = 0
    for gene in ortho_dict[group_name]:
        ortho_set.add(gene)
    print_accession = False
    for line in fasta_lines:
        line = line.rstrip()
        if re.search(r"^>", line):
            print_accession = False
            if len(ortho_set) == 0:
                continue
            header = line.replace('>', '')
            if header in ortho_set:
                ortho_set.remove(header)
                outlines.append(line)
                i += 1
                print_accession = True
        elif print_accession == True:
            outlines.append(line)
        else:
            continue
    print "\tnumber of accessions in this group:\t" + str(i)
    return(outlines)

keys = []
sorted_keys = []
keys = ortho_dict.keys()

keys.sort(key=int)
ortho_list = []
for group_name in keys:
    print ("orthogroup" + str(group_name))
    ortho_fasta = extract_func(group_name)
    outfile = str(conf.out_dir) + "/orthogroup" + str(group_name) + ".fa"
    with open(outfile, 'w') as o:
        for line in ortho_fasta:
            o.write(line + "\n")