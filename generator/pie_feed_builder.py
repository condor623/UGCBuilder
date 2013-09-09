#! /usr/bin/env python
import time, sys, csv, re, datetime, string, random, subprocess
#sys.path.append('/Users/javier.hernandez/wip/UGCBuilder')
#from generator import mapping
from xml.etree.ElementTree import *
from optparse import OptionParser

#test

###################################################################
# Nuts and bolts
###################################################################
column_map = [
	'TransactionDate',
	'Locale',
	'EmailAddress',
	'UserID',
	'UserName', 
	'ProductId', 
	'ImageUrl', 
	'Name'
]

def populateTags(parentTag, tagTitle, tagText):
	node = SubElement(parentTag, tagTitle)
	node.text = tagText

def CheckForExistence(line, num, lineNum, errorFile):
	result = True

	try: 
		line[num].encode('UTF-8', 'strict')
	except UnicodeDecodeError:
		errorFile.write("line" + str(lineNum) + "\tcolumn: " + str(num) + "\t" + str(line) + "\n")
		result = False
	except IndexError:
		errorFile.write("line" + str(lineNum) + "\tcolumn: " + str(num) + "\t" + str(line) + "\n")
		result = False  
	return result

def parseLine (line, interactDict, errorFile):

	validColumns = True

	for column in column_map:
		try: 
			interactDict[column] = re.sub('\n\t', ' ', line[column_map.index(column)].encode('utf-8'))
 
		except UnicodeDecodeError:
			errorFile.write(str(line) + '\n')
			validColumns = False
		
	if not validColumns: 
		interactDict = {}

	return interactDict
		
def generateFeed(options):
	# Access files
	clientFile = open(options.input)
	clientProductFeed = open(options.output, 'w')
	errorFile = open('error.log', 'w')
	reader = csv.reader(clientFile, delimiter="	")

	# Define Feed tag values
	generateDateTime = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
	namespace = 'http://www.bazaarvoice.com/xs/PRR/PostPurchaseFeed/' + options.schema

	# Build necessary header
	xmlPrefix = "<?xml version='1.0' encoding='UTF-8'?>"
	root = Element('Feed')
	# root.set('name', options.clientName)
	root.set('xmlns', namespace)
	# root.set('extractDate', generateDateTime)

	#nuts and bolts
	unique_id = random.randint(10000000,99999999) * random.randint(10000000,99999999)
	products = []
	interactions = {}

	# Loop through input, assuming first line is header
	#reader.next() 
		
	for line in reader:
		_interaction = {}
		_interaction = parseLine(line, _interaction, errorFile)

		interactions[unique_id] = []
		interactions[unique_id].append(_interaction)

		for int_id in interactions.keys():

			interactionNode = SubElement(root, 'Interaction')
			# interactionNode.set('id', int_id)
		
			for interact in interactions[int_id]:

				tDateNode = SubElement(interactionNode, 'TransactionDate')
				print(interact)
				#tDateNode.text = time.strftime("%Y-%m-%dT%H:%M:%S", interact['TransactionDate'])

				emailNode = SubElement(interactionNode, 'EmailAddress')
				emailNode.text = interact['EmailAddress']
			
				localeNode = SubElement(interactionNode, 'Locale')
				localeNode.text = interact['Locale']
				
				userNameNode = SubElement(interactionNode, 'UserName')
				userNameNode.text = interact['UserName']

				userIDNode = SubElement(interactionNode, 'UserID')
				userIDNode.text = interact['UserID']

				productsNode = SubElement(interactNode, 'Products')

				productNode = SubElement(productsNode, 'Product')

				exIDNode = SubElement(productNode, 'ExternalId')
				ExIDNode.text = interact['ProductId']

				prodNameNode = SubElement(productNode, 'Name')
				prodNameNode.text = interact['Name']

				imageNode = SubElement(productNode, 'ImageUrl')
				imageNode.text = interact['ImageUrl']

	clientProductFeed.write(xmlPrefix)
	clientProductFeed.write(tostring(root))

###################################################################
# Handle command line args
###################################################################

def main(argv):
	usage = 'usage: %prog [options] arg'
	parser = OptionParser(usage)
	parser.add_option('-c', '--clientName', help='Database name for the client', action='store', dest='clientName')
	parser.add_option('-i', '--input', help='Location of the CSV input file', action='store', dest='input')
	parser.add_option('-o', '--output', help='Location of the XML output file', action='store', dest='output')
	parser.add_option('-s', '--schema', default='6.9', help='The Bazaarvoice XML schema version', action='store', dest='schema')
	
	(options, args) = parser.parse_args()

	generateFeed(options)
	#subprocess.call(['xmllint --schema http://www.bazaarvoice.com/xs/PRR/StandardClientFeed/' + options.schema + ' --noout ' + options.output], shell=True)


if __name__ == '__main__':
	main(sys.argv[1:])  





