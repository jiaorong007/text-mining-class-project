#! /usr/bin/env python

######### The only Area needs to be modified ######
path = '/Users/jiaorong007/Desktop/UTHouston/courses/Spring2017/python/project/'
geneName=path+"genelist.txt"
relationName=path+"Network.txt"
###################################################


# PART I: Extract all the PMID codes from xml files
from os import listdir
import xml.etree.ElementTree as ET
import io
PMIDName=path+"PMIDlist.txt"
PMIDfile=open(PMIDName,'w')
for filename in listdir(path):
	if not filename.endswith('.xml'): continue
	fullname = path+filename
	tree = ET.parse(fullname)
	root = tree.getroot()
	for pmid in root.iter('PMID'):
		text=pmid.text+'\n'
		PMIDfile.write(text)

PMIDfile.close()


# PART II: Get combinations from gene list
from itertools import *
genefile=open(geneName,'rU')
genelist=[]

for gene in genefile:
	gene=gene.strip("\n")
	gene=str(gene)
	genelist.append(gene)

genefile.close()
comb=list(combinations(genelist, 2))


# PART III: Check Association
from pattern import web
import requests
relationfile=open(relationName,'w')
Line='Gene1'+'\t'+'Gene2'+'\t'+'Association'+'\n'
relationfile.write(Line)
LEN=len(comb)
for i in range(LEN):
	word1=comb[i][0]
	word2=comb[i][1]
	print "Check association between "+word1+" and "+word2+" ..."
	PMIDfile=open(PMIDName,'rU')
	noassociation=True
	for id in PMIDfile:
		if noassociation:
			url = "http://www.ncbi.nlm.nih.gov/pubmed/{0}".format(id)
			page = requests.get(url).text.encode('ascii', 'ignore')
			dom = web.Element(page)
			bytag=dom.by_tag("abstracttext")
			if len(bytag)>0:
				text=dom.by_tag("abstracttext")[0].content
				if word1 in text:
					if word2 in text:
						print  "Association exists between " + word1 +" and " + word2 +"!"
						Line=word1+'\t'+word2+'\t'+'TRUE'+'\n'
						relationfile.write(Line)
						noassociation=False
	if noassociation:
		Line=word1+'\t'+word2+'\t'+'FALSE'+'\n'
		relationfile.write(Line)
		
	PMIDfile.close()
print "Checking Finished!"
relationfile.close()
