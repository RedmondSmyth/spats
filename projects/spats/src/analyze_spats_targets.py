#!/usr/bin/env python

#Written by Ray Zhuang 2013 to analysis input target fasta files for Spats
#Looks for 3' uniqueness (defines default for min_read_len), as well as 
#minimum required length of adapter to search for with clipper (defines trim-match by default)

#Edited by Kyle Watters in September 2014 to include automatic error calculation for cutadapt

import sys
import os
import getopt
import re
from sys import stdout
from collections import OrderedDict


present_dir = os.getcwd()+"/"

name = "analyze_spats_targets.py"
help_message = '''
{0} takes a targets file for alignment in spats and determines how many nucleotides
at the 3' end are required for unique alignment as well as to search for A_adapter_b similarity to set 
a proper trim-match value for adapter clipping.

Usage: 
    {0} <targets.fa> <adapter sequence>

Options:
-h,--help           brings up help
-v,--version        displays version number
--verbose           increases details of text output
'''.format(name)

class Usage(Exception):
   def __init__(self,msg):
       self.msg = msg

def get_version():
    return "0.0.2"

class Params:
    def __init__(self):
       pass

    def parse_options(self, argv):
        
        try:
            opts, args = getopt.getopt(argv[1:],"hvq",["help","version","verbose"])            

        except getopt.error, msg:
            raise Usage(msg)
        
        quiet = True
 
        for option, arg in opts:
            if option in ("-v", "--version"):
                print "targets_analysis v%s" % (get_version())
                exit(0)
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("--verbose"):
                quiet = False
            else:
                quiet = True
                
        if len(args) != 1:
            raise Usage(help_message)
    
        return args,quiet
        
    def check(self):
        pass           

def readFasta(fasta):
    #Check that the file is fasta
    extension = fasta.split(".")[-1]
    if extension != "fa" and extension != "fasta":
        print >> sys.stderr, "File is not a fasta extension (fa,fasta)"
    
    #Check file exists
    elif not os.path.isfile(fasta):
        print("No such file as {0}".format(fasta))
        
    else:    
        #Load the fasta file to parse
        targets = file(fasta,"r")
            
        lines = []
        for line in targets:
            read_line = line.strip()
            if read_line != "":
                if read_line[0] == ">":
                    read_line = read_line + " "
                lines.append(read_line)
        split_lines = ''.join(lines).split(">")[1:]
        all_targets = OrderedDict()
        for target in split_lines:                                
            #Takes the target name and sequence pairs, and splits them into a dictionary
            all_targets[target.split(" ")[0]] = target.split(" ")[1].strip()
        
        return all_targets        

def rev(s):
                              
    #This section was taken from Cole's code
    nuc_table = { 'A' : 'T',
                'T' : 'A',
                'C' : 'G',
                'G' : 'C',
                'a' : 't',
                't' : 'a',
                'c' : 'g',
                'g' : 'c'  }
    sl = list(s)
    
    try:
        rsl = [nuc_table[x] for x in sl]
    except KeyError, k:
        print >> sys.stderr, "Error: adapter sequences must contain only A,C,G,T"
        exit(1)
    rsl.reverse()
    
    return ''.join(rsl) 
    
def analyze_unique(inputfile,quiet=False):
    
    #Load fasta formatted targets  
    targets = readFasta(inputfile)
      
    #Search for the 3' end for uniqueness across all targets to find the minimum length to uniquely align
    #each target to a set of reads with bowtie
    
    #Scan through all possible sequences on the 3' end, getting successively larger, until find unique
	## Starting search at 1 nt from the 3' end
	## Compare given number of nucleotides at three prime end
	## If the number of unique sequences is fewer than the number of targets, continue search
    
    finished = False
    unique = 1 #Number of nucleotides on the 3' end to provide complete uniqueness among all targets, initialized
    while not finished:
        uniqArray = []
        for seq in targets.values():
            seq_end = seq[-unique:].upper()
            if not seq_end in uniqArray:
                uniqArray.append(seq_end)
        if len(uniqArray) == len(targets):
            break
            finished = True
        else:
            unique += 1
    
    if quiet == False:
        print >> sys.stderr, "Number of nucleotides from 3' end needed to be unique: {0}\n".format(unique)
        
    return unique

             
def analyze_clip_min(inputfile,adapter,quiet=True):             
    
    #Load fasta formatted targets  
    targets = readFasta(inputfile)

    #adapter comes in reads as a revcomp
    #First obtain reverse complement of the file, 
    #then add beginning of adapter at the front 
    #(to mimic it coming up randomly in the handle sequence (RRRY)
    allseqs = ""
    for seq in targets.values():
        #concatenate sequences w/ adapter for easy searching, buffer with space
        #Note that beginning of adapter addition is to mimic the index appearing
        allseqs += (adapter[0:4].upper() + rev(seq).upper()  + " ")
    
    #upper bound on search for adapter sequence
    upper_bound = len(adapter)
    
    for clip_min in range(4,upper_bound):  #start with 4, since index could have first four
        min_adapter = adapter[0:clip_min]
        match = re.search(min_adapter,allseqs)
        if not match:
            break
  
    #Add 2 to clip_min to buffer against point mutations in sequencing data
    clip_min += 2             
             
    #Establish an error rate based on the sequence length of the adapter being searched
    if clip_min < 10:
        error_rate = 0
    elif clip_min in range(10,20):
        error_rate = 0.1                                                     
    else:
        error_rate = 0.05 #lower error rate compensates for high RNA sequence 
                          #similarity with long adapter sequences
                                                                                                                                                                                                                                                                                              
    if quiet == False:
        print >> sys.stderr, "Adapter clipping search length recommended: {0}".format(clip_min)  
        print >> sys.stderr, "Suggested error rate for cutadapt is: {0}\n".format(error_rate)
    
    return clip_min,error_rate
    
    
def main(argv=None):

    params = Params()
    
    try:
        if argv is None:
            argv = sys.argv
            args,quiet = params.parse_options(argv)
            params.check()     

        inputfile = args[0]
        
        try:
            adapter = args[1]
        except IndexError:
	    adapter = "AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC" #default (5' end of Illimuna multiplexing R2 adapter)
	    if quiet == False:
	       stdout.write("Using default sequence for adapter: {0}\n".format(adapter))
	       stdout.flush()     
        
	unique = analyze_unique(inputfile,quiet)           
        clip_min,error_rate = analyze_clip_min(inputfile,adapter,quiet)

        return clip_min,unique,error_rate

    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, ""
        return 2     

if __name__ == "__main__":
    sys.exit(main())

