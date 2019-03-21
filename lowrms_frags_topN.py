import sys
from argparse import ArgumentParser

# we need the fragment quality for the 3mers too.
parser = ArgumentParser(description='Get the lowest rms fragments among top N')
parser.add_argument('-frag_qual', type=str, help='frag quality file where rms and score ranking')
parser.add_argument('-nbest_fragments', type=int, default=200, help='fragments among top N')
parser.add_argument('-fullmer', type=str, help='fragment file')
parser.add_argument('-out', type=str, help='output fragment file')
parser.add_argument('-ntop', type=int, default=3, help='how many fragments of lowest rmsd to take')
args = parser.parse_args()

frag_qual_file = args.frag_qual
fullmer = args.fullmer
outfile = args.out
ntop = args.ntop
nbest_fragments = args.nbest_fragments

filein = open(frag_qual_file)
dic={}
for line in filein:
	pos = int(line.split()[1])
	nfrag = int(line.split()[2])	
	rmsd  = float(line.split()[3])
	if nfrag==1:
		dic[pos]={}
	if nfrag <= nbest_fragments:
		dic[pos][nfrag]=rmsd

filein.close()
	
# find N lowest rmsd fragments
dic_top={}
for pos in dic.keys():
	frag_list = dic[pos].keys()
	frag_list.sort( lambda x,y : cmp(dic[pos][x],dic[pos][y]) )
	top_n_list = frag_list[:ntop]
	dic_top[pos] = top_n_list

	
# Take best N fragments from 00001.200.9mers
filein = open(fullmer)
fileout = open(outfile,'w')
for line in filein:
	if 'position' in line:
		pos = int(line.split()[1])
		if pos > 1:
			fileout.write('\n')
		line2 = line.replace('200','%3i' %(ntop))
		fileout.write(line2)
		prev_frag=0
		count=0
		nfrag=0
	elif line=='\n':
		nfrag+=1
		
	elif len( line.split() ) > 1: #and ( line[85]=='P' and line[90]=='F' ): # fragment line
		if nfrag in dic_top[pos]:
			this_frag = nfrag
			if this_frag != prev_frag:
				count+=1
				fileout.write('\n')
				prev_frag=this_frag
			fileout.write(line)	

