#create the graph for a given set of UTTs :D
import string
from music21 import stream, chord, pitch
from DijkstraShortestPath import shortestPath
from Node2D import Node2DGraph
import random
import re
song1 = 'song1.txt'
neoTest = 'NeoTest.txt'
song1X = 'song1Limited.txt'
song2 = 'song2Edited.txt'
song3 = 'song3.txt'
song12 = 'song12.txt'
song123 = 'Song123.txt'
pitchClass = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
enharmonic = ['B#', 'Db', 'D', 'D#', 'Fb', 'E#', 'Gb', 'G', 'G#', 'A', 'A#', 'B']

def chordToString(chordObj):
	return (chordObj.pitches[0].name + ' ' + chordObj.commonName).replace(' triad', '')

def chordCompare(chord1, chord2):
	return chordToString(chord1) == chordToString(chord2)#chordObj.pitches[0].name + ' ' + chordObj.commonName 

def chordToPCSet(chordObj):
	pcList = []
	for i in chordObj.pitches:
		pcList.append(i.pitchClass)
	return pcList


class UTT:
	'Defines the operations of a UTT'
	switchQuality = False
	majorRootMovement = 0 
	minorRootMovement = 0 
	space = []
	distanceUnit = 1
	looped = False
	identifier = ''

	def __init__(self, switch, majorMovement, minorMovement, _distance=1, _identifier=str(random.randint(0,9))):
		self.switchQuality = switch
		self.majorRootMovement = majorMovement
		self.minorRootMovement = minorMovement
		self.distanceUnit = _distance
		self.identifier = _identifier
		#if startTriad != None:
		#	self.computeSpaceAndDistance(startTriad)
			

	#format for a UTT string is '(<+/-,int,int>, distanceInt, identifierString)'
	@classmethod
	def fromS(self, sUTT):
		#print 'got UTT string: ' + sUTT
		justUTT = sUTT[sUTT.find("<")+1:sUTT.find(">")]
		#print 'got UTT substring: ' + justUTT
		splitUTT = justUTT.split(',')
		for i, item in enumerate(splitUTT):
			splitUTT[i] = item.strip()
		#print 'split and stripped: ' + str(splitUTT)
		switch = False
		if splitUTT[0] == '-':
			#print 'setting switch to true'
			switch = True
		UTTExtra = sUTT[sUTT.find(">"):]
		#print 'UTTextra: ' +str(UTTExtra)
		UTTExtra = UTTExtra[:UTTExtra.find(")")]
		#print 'UTTextra: ' +str(UTTExtra)
		extraStuff = UTTExtra.split(',')
		dist = float(extraStuff[1].strip())
		ident = extraStuff[2].strip()
		#print 'extra stuff: (' + str(dist) +',' + ident +')'
		return UTT(switch, int(splitUTT[1]), int(splitUTT[2]), dist, ident)

	def computeSpaceAndDistance(self, startTriad, reverse):
		self.space = self.allPossibleTransformationsFromTriad(startTriad, reverse)

	def transform(self, chordIn):
		#print 'transforming ' + chordIn.pitches[0].name + ' ' + chordIn.commonName
		#print '    normal form: ' + str(chordIn.normalForm)
		#print '    normal form = [0,3,7] = ' + str(chordIn.normalForm == [0,3,7])
		if chordIn.normalForm == [0,3,7]:
			pitchList = []
			for t in chordIn.pitches:
				pitchList.append(pitch.Pitch((t.ps + self.minorRootMovement) % 12))
			if self.switchQuality:
				pitchList[1] = pitch.Pitch(pitchList[1].ps + 1)
			#print 'pitchList is ' + str(pitchList)
			tChord = chord.Chord(pitchList)
			#print 'tChord is: ' + tChord.pitches[0].name + ' ' + tChord.commonName
			return tChord
		elif chordIn.normalForm == [0,4,7]:
			pitchList = []
			for t in chordIn.pitches:
				pitchList.append(pitch.Pitch((t.ps + self.majorRootMovement) % 12))
			if self.switchQuality:
				pitchList[1] = pitch.Pitch(pitchList[1].ps - 1)
			tChord = chord.Chord(pitchList)
			return tChord
		else:
			print 'You are not a triad!'

	def distance(self, triad1, triad2, weight=None):
		#print 'space is: ' + str(self.space)
		#print 'this is in the goddamn list: ' + str(self.space[23])
		index1 = -1
		index2 = -1
		for i, c in enumerate(self.space):
			#print 'comparing: ' + str(triad1) + ' with ' + str(c) 
			if chordCompare(c, triad1):
				#print 'yup they are equivalent'
				index1 = i
			if chordCompare(c, triad2):
				index2 = i
		#print 'index1: ' + str(index1)
		#print 'index2: ' + str(index2)
		if index1 == -1 or index2 == -1: 
			return -1
		if weight == None:
			weight = self.distanceUnit
		
		dist1 = abs((index1 - index2) * weight)
		dist2 = abs((index2 - index1) * weight)
		distWrap = dist1
		if index1 < index2:
			distWrap = abs(index1 + len(self.space) - index2)
		else:
			distWrap = abs(index2 + len(self.space) - index1)
		#print 'dist1: ' + str(dist1)
		#print 'dist2: ' + str(dist2)
		#print 'distWrap: ' + str(distWrap)
		return min([dist1,dist2,distWrap])

	def allPossibleTransformationsFromTriad(self, triad, reverse):
		chordList = []
		looped = False
		#print 'creating space from starting triad: ' + chordToString(triad)
		for i in range(27):
			for j in range(len(chordList)):
				#print 'comparing: ' + str(triad) + ' with ' + str(chordList[j]) 
				if chordCompare(triad,chordList[j]):
					looped = True
			if looped: 
				break
			if (reverse):
				chordList.insert(0, triad)
			else:
				chordList.append(triad)
			triad = self.transform(triad)
		return chordList

	def allPossiblePCSetTransformationsFromTriad(self, triad):
		pcSetList = []
		for i in range(27):
			pcSetList.append(chordToPCSet(triad))
			for j in range(len(chordList)):
				if chordCompare(triad,chordList[j]):
					break
			triad = self.transform(triad)
		print 'i is ' + str(i)
		return pcSetList


def createDictGraphFromNodeGraph(graph):
	outGraph = {}
	for i in graph:
		for j in i:
			neighborDict = {}
			for n in j.neighbors:
				neighborName = chordToString(graph[n[0][0]][n[0][1]].chord)
				neighborDict[neighborName] = n[1]
			outGraph[chordToString(j.chord)] = neighborDict
	return outGraph

#def createGraphFromUTTs(listOfUTTs):
	#for UTT in
	#ORDER MATTERS! You must pass these neighbors in order of the forward transformation, so that transformations can be recovered later.
def makeNeighbors(node1, node2, distanceBetweenThem, transformIdentifier, stripInverse = False):
	node1.addNeighbor(node2, distanceBetweenThem, transformIdentifier)
	#add '-1' for the inverse transform
	inverseID = transformIdentifier
	if not stripInverse:
		inverseID = inverseID + '-1'
	node2.addNeighbor(node1, distanceBetweenThem, inverseID)


def make2DNodeGraph(UTT1, UTT2, stripInverse = False):
	dGraph = []
	#create a new graph for implementing Dijkstra
	prevColSpace = None
	for x in range(len(UTT1.space)):
		#if compareChord(iterChord, startChord):
		#print 'creating row space from: ' + chordToString(UTT1.space[x])
		colSpace = UTT2.allPossibleTransformationsFromTriad(UTT1.space[x], True)
		#print 'created column space: ' + str(colSpace)
		dGraph.insert(0,[])
		for y, colChord in enumerate(colSpace):
			#create node from rowChord
			newNode = Node2DGraph(colChord, len(UTT1.space) - x - 1, y)
			dGraph[0].append(newNode)
			#if index greater than one, add an edge backwards
			#print dGraph
			if x > 0:
				#print 'y = ' + str(y)
				#print 'dGraph.len = ' + str(len(dGraph))
				#print 'dGraph[1].len = ' + str(len(dGraph[1]))
				#print 'column space is: ' + str(colSpace)
				makeNeighbors(newNode, dGraph[1][y], UTT1.distanceUnit, UTT1.identifier, stripInverse)
				#newNode.addNeighbor(dGraph[x-1][y], UTT1.distanceUnit)
				#dGraph[x-1][y].addNeighbor(newNode, UTT1.distanceUnit)
				#if chordCompare(dGraph[1][y].chord, newNode.chord):
					#print 'adding edge for identical chord at colSpace[index - 1], colSpace[index], index = ' + str(index)
			if x == len(UTT1.space) - 1:
				makeNeighbors(dGraph[-1][y], newNode, UTT1.distanceUnit, UTT1.identifier, stripInverse)
			if y > 0:
				if chordCompare(newNode.chord, dGraph[0][y - 1].chord):
					print 'adding edge for identical chord at colSpace[index], prevColSpace[index], index = ' + str(index)
				makeNeighbors(newNode, dGraph[0][y-1], UTT2.distanceUnit, UTT2.identifier, stripInverse)
				#newNode.addNeighbor(dGraph[x][y - 1], UTT2.distanceUnit)
				#dGraph[x][y - 1].addNeighbor(newNode, UTT2.distanceUnit)

		if chordCompare(colSpace[-1], colSpace[0]):
			print 'adding edge for identical chord at colSpace[-1], colSpace[0]'
		makeNeighbors(dGraph[0][0], dGraph[0][-1], UTT2.distanceUnit, UTT2.identifier, stripInverse)
		#G.add_edge(colSpace[-1], colSpace[0])
		#prevColSpace = colSpace
	return dGraph

def print2DNodeGraph(graph):
	for x in range(len(graph)):
		xString = ""
		for y in range(len(graph[0])):
			#if len(graph[x][y].neighbors) != 4:
				#print 'got a lot of neighbors here: ' + str(len(graph[x][y].neighbors))
			xString += chordToString(graph[x][y].chord) + '-'
		print xString

def nodeGraph2DToStringInverted(graph):
	gString = ""
	for x in range(len(graph)):
		xString = ""
		for y in range(len(graph[0])):
			#if len(graph[x][y].neighbors) != 4:
				#print 'got a lot of neighbors here: ' + str(len(graph[x][y].neighbors))
			xString += chordToString(graph[x][y].chord) + '-'
		gString += xString
		gString += '\n'
	return gString

def nodeGraph2DToString(graph):
	gString = ""
	for y in range(len(graph[0])):
		xString = ""
		for x in range(len(graph)):
			#if len(graph[x][y].neighbors) != 4:
				#print 'got a lot of neighbors here: ' + str(len(graph[x][y].neighbors))
			xString += chordToString(graph[x][y].chord) + '-'
		gString += xString
		gString += '\n'
	return gString

def createUTTSpaceFromStringsAndStartChord(sUTT1, sUTT2, startChord, stripInverse = False):
	UTT1 = UTT.fromS(sUTT1)
	UTT2 = UTT.fromS(sUTT2)
	UTT1.computeSpaceAndDistance(startChord, True)
	UTT2.computeSpaceAndDistance(startChord, True)
	return (UTT1, UTT2, make2DNodeGraph(UTT1, UTT2, stripInverse))

#add edges for every node in your graph between two nodes whose path between 
#them are the series of transformations represented by pathString
def addShortcut(graph, pathString, distanceVal, identifier = 'X', stripInverse = False):
	#make ALL THE NEIGHBORS!
	print 'identifier to add is "' + str(identifier) + '"'
	for i in range(len(graph)):
		for j in range(len(graph[i])):
			identifiers = pathString.split('|')
			shortCutX = i
			shortCutY = j
			print identifiers
			for transIndex in range(len(identifiers)):
				#print transIndex
				for neigh in graph[shortCutX][shortCutY].neighbors:
					#print 'comparing neighbor ' + str(neigh[2]) + ' with id ' + str(identifiers[transIndex])
					if neigh[2] == identifiers[transIndex]:
						#print 'found neighbor with id ' + str(identifiers[transIndex]) + ', chord: ' + chordToString(graph[neigh[0][0]][neigh[0][1]].chord)
						shortCutX = neigh[0][0]
						shortCutY = neigh[0][1]
						break
			print 'making neighbors for ' + chordToString(graph[i][j].chord) + ' and ' + chordToString(graph[shortCutX][shortCutY].chord)
			makeNeighbors(graph[i][j], graph[shortCutX][shortCutY], distanceVal, identifier, stripInverse)

def chordFromString(sChord):
	saveString =sChord
	pitchClasses = []
	isMinor = False
	if 'm' in sChord:
		isMinor = True
		sChord = sChord.replace('m', '')
	sChord = sChord.strip()
	sChord = sChord.replace('7', '')
	for i, p in enumerate(pitchClass):
		if p == sChord or enharmonic[i] == sChord:
			pitchClasses.append(i)
	if len(pitchClasses) == 0:
		print "couldn't find chord from string: " + saveString
		return
	if isMinor:
		pitchClasses.append(pitchClasses[0] + 3 % 12)
	else:
		pitchClasses.append(pitchClasses[0] + 4 % 12)
	pitchClasses.append(pitchClasses[0] + 7 % 12)
	return chord.Chord(pitchClasses)

def splitChordsFileLine(line):
	retArray = []
	stringArray = line.split('|')
	for s in stringArray:
		tokenSplit = s.split('.')
		for t in tokenSplit:
			tokenSplitSplit = t.split(' ')
			for ts in tokenSplitSplit:
				if ts != ' ' and ts != '' and ts != '\n':
					retArray.append(ts)
	for i, c in enumerate(retArray):
		if i < len(retArray) - 1 and c == retArray[i + 1]:
			del retArray[i]
	return retArray
			
def parseChordsFile(filename):
	f = open(filename, 'r')
	chordList = [] 
	for line in f:
		chordList.append(splitChordsFileLine(line))
	return chordList

def computePathsForChordPhrase(graph, chordPhrase):
	if len(chordPhrase) == 0:
		return None
	path = shortestPath(graph, chordCompare, graph[-1][0], chordPhrase[0])
	paths = []
	#print 'finding path for ' + str(chordPhrase)
	for c in chordPhrase[1:]:
		path = shortestPath(graph, chordCompare, path[-1], c)
		paths.append(path)
	#print 'path found is ' + str(paths)
	return paths

def getDistAndTransFromChordPhrase(graph, phrase):
	if phrase is None or len(phrase) == 0:
		return []
	distTrans = []
	#print 'finding distance for phrase: ' + str(phrase)
	for path in phrase:
		pathDist,pathTrans = getDistancesAndTransformationsFromPath(graph, path)
		distTrans.append([pathDist, pathTrans])
	return distTrans

def getDistAndTransForSong(graph, songChords):
	phraseDists =[]
	lastChordInPrevPhrase = None
	for phrase in songChords:
		if lastChordInPrevPhrase is not None:
			transitionPath = computePathsForChordPhrase(graph, [lastChordInPrevPhrase, phrase[0]])
			phraseDists.append(getDistAndTransFromChordPhrase(graph,transitionPath))
		else:
			lastChordInPrevPhrase = phrase[-1]
		phrasePaths = computePathsForChordPhrase(graph, phrase)
		phraseDists.append(getDistAndTransFromChordPhrase(graph,phrasePaths))
		lastChordInPrevPhrase = phrase[-1]
	return phraseDists

def getDistancesAndTransformationsFromPath(graph, path):
	#print 'finding distances for ' + str(path)
	prevNode = None
	distTrans =[]
	for i, node in enumerate(path):
		if prevNode == None:
			prevNode = node
			continue
		for n in prevNode.neighbors:
			if graph[n[0][0]][n[0][1]] == node:
				distTrans.append(n[1:])
				break
		prevNode = node
	totalDist = 0
	transforms = ""
	for dt in distTrans:
		totalDist += float(dt[0])
		transforms += dt[1] +'|'
	return (totalDist,transforms[:-1])

def printDistancesForSong(songDistances):
	totalDist = 0
	for p in songDistances:
		totalPhraseDist = 0
		for d in p:
			totalPhraseDist += d[0]
		print str(p) + " phraseDist: " + str(totalPhraseDist)
		totalDist += totalPhraseDist
	print 'totalDist = ' + str(totalDist)
	return totalDist

def printDistancesAndChordPhrasesForSong(songDistances, chordObjList):
	totalDist = 0
	for i, p in enumerate(songDistances):
		totalPhraseDist = 0
		for d in p:
			totalPhraseDist += d[0]
		print str(p) + " phraseDist: " + str(totalPhraseDist)
		totalDist += totalPhraseDist
		if (i % 2) == 0:
			phraseNum = i/ 2
			strPhrase = ""
			for j in chordObjList[phraseNum]:
				strPhrase += chordToString(j) + ", "
			strPhrase = strPhrase[:-2]
			print strPhrase
	print 'totalDist = ' + str(totalDist)
	return totalDist

def checkUTTSpace(graph):
	chords = []
	for i in range(12):
		maj3 = i + 4 % 12
		min3 = i + 3 % 12
		fifth = i + 7 % 12
		chords.append(chord.Chord([i, maj3, fifth]))
		chords.append(chord.Chord([i, min3, fifth]))
	for c in chords:
		chordIsThere = False
		for i in graph:
			for j in i:
				if chordToString(c) == chordToString(j.chord):
					chordIsThere = True
		if chordIsThere is False:
			return False
	return True			

def computeDistanceForAllK11UTTs(songChordPhrases):
	dMinor = chord.Chord([2,5,9])#used as starting chord
	totalDistances=[]
	uttStrings = []
	for i in range(12):
		uttString = '<-, ' + str(i) + ', ' + str((i + 1) %12) + '>'
		uttStrings.append(uttString)
	for i in range(12):
		uttString = '<+, ' + str(i) + ', ' + str(i) + '>'
		uttStrings.append(uttString)
	print uttStrings

	totalDists = []
	uttSets = []
	for index, u in enumerate(uttStrings):
		for index2, u2 in enumerate(uttStrings):
			if index2 > index:
				uttString = '(' + u + ', 1, A)'
				uttString2 = '(' + u2 + ', 1, B)'
				uttSets.append([uttString, uttString2])
	print uttSets
	for utts in uttSets:
		print 'computing for utts: ' + utts[0] +' and ' + utts[1]
		uttA,uttB,nGraph = createUTTSpaceFromStringsAndStartChord(utts[0], utts[1], dMinor)
		#make sure all chords exist in the UTT space
		if checkUTTSpace(nGraph):
			songDistances = getDistAndTransForSong(nGraph, songChordPhrases)
			totalDists.append(printDistancesForSong(songDistances))
		else:
			totalDists.append(-1)
	uttFailedSets = []
	minDist = 10000000
	minDex = -1
	minDices = []
	for i, d in enumerate(totalDists):
		if d < minDist and d != -1:
			minDist = d
	for i in range(len(totalDists)):
		if totalDists[i] == minDist:
			minDices.append(i)
		if totalDists[i] == -1:
			uttFailedSets.append(uttSets[i])
	print uttFailedSets
	utts = []
	for m in minDices:
		utts.append(uttSets[m])
	return [minDist, utts]


def main():
	'''print 'In main'
	UTT1 = UTT.fromS('<-,2,3>')
	chordIn = chord.Chord([0,3,7])
	print chordIn.pitches
	print chordIn.normalForm
	minorMovement = 3
	print chordIn.pitches
	
	tChord = UTT1.transform(chordIn)
	chordIn2 = chord.Chord([10,1,5])
	oldChord = chord.Chord(chordIn2)
	oldChord2 = chord.Chord(chordIn2)
	print 'old chord is: ' + chordIn2.pitches[0].name + ' ' + chordIn2.commonName
	for i in range(5):
		chordIn2 = UTT1.transform(chordIn2)
		print 'transformed chord is: ' + chordIn2.pitches[0].name + ' ' + chordIn2.commonName

	#print tChord.pitches
	#print tChord.commonName
	print 'new chord is: ' + chordIn2.pitches[0].name + ' ' + chordIn2.commonName
	print '__________________________'
	chordListString = ""
	chordSpace = UTT1.allPossibleTransformationsFromTriad(chordIn2)
	for c in chordSpace:
		chordListString += str(c) + ', '
	print chordListString

	pcSetListString = ""
	pcSetSpace = UTT1.allPossiblePCSetTransformationsFromTriad(chordIn2)
	for c in pcSetSpace:
		pcSetListString += str(c) 
	print pcSetListString

	print str(pcSetSpace)
	G = nx.Graph()
	G.add_nodes_from(chordSpace)

	UTT2 = UTT(True, 2, 3, oldChord)
	print oldChord == oldChord2
	dist = UTT2.distance(oldChord, chordIn2)
	print 'distance is: ' + str(dist)'''
	


	#UTT1 = UTT(True, 2, 3, 1, 'S')
	#UTT2 = UTT(True, 4, 5, 5, 'T')

	#print str(UTT2.space)

	'''G = nx.Graph()
	prevColSpace = None
	for i in range(len(UTT1.space)):
		#if compareChord(iterChord, startChord):
		print 'creating column space from: ' + chordToString(UTT1.space[i])
		colSpace = UTT2.allPossibleTransformationsFromTriad(UTT1.space[i])
		for index, colChord in enumerate(colSpace):
			G.add_node(colSpace[index])
			#if index greater than one, add an edge backwards
			if index > 0:
				G.add_edge(colSpace[index - 1], colSpace[index])
				#G.add_edge(colSpace[index], colSpace[index - 1])
				if chordCompare(colSpace[index - 1], colSpace[index]):
					print 'adding edge for identical chord at colSpace[index - 1], colSpace[index], index = ' + str(index)
			if prevColSpace != None:
				#print 'creating edge: ['
				if chordCompare(colSpace[index], prevColSpace[index]):
					print 'adding edge for identical chord at colSpace[index], prevColSpace[index], index = ' + str(index)
				G.add_edge(colSpace[index], prevColSpace[index])
				#G.add_edge(prevColSpace[index], colSpace[index])
		if chordCompare(colSpace[-1], colSpace[0]):
			print 'adding edge for identical chord at colSpace[-1], colSpace[0]'
		#G.add_edge(colSpace[-1], colSpace[0])
		prevColSpace = colSpace'''

	#dGraph = make2DNodeGraph(UTT1, UTT2)
	
	startChord = chord.Chord([10,1,5])
	iterChord = chord.Chord([10,1,5])
	
	uttS,uttT,dGraph = createUTTSpaceFromStringsAndStartChord("(<-, 2, 3>, 1, S)", "(<-, 4, 5>, 5, T)", startChord)

	print2DNodeGraph(dGraph)
	'''print "0,7 neighbors are: " + dGraph[0][7].neighborsToString(dGraph)
	print "0,1 neighbors are: " + dGraph[0][1].neighborsToString(dGraph)

	endChord = chord.Chord([2,6,9])

	#print "start is " + str(dGraph[-1][0])
	#note, you have to pass a NODE for the starting position, and a CHORD for the end position
	shortPath = shortestPath(dGraph, chordCompare, dGraph[-1][0], endChord)
	print str(shortPath)

	print [chordToString(i.chord) + ':'  for i in shortPath]


	addShortcut(dGraph, uttS, uttT, 'STT', 2.2, identifier = 'X')
	print 'added shortcut "STT"'
	shortPath = shortestPath(dGraph, chordCompare, dGraph[-1][0], endChord)
	print str(shortPath)

	print [chordToString(i.chord) + ':'  for i in shortPath]

	'''

	#pitch.Pitch("Db minor")
	seedChord = chord.Chord([7,11,2])
	cSharpMinor = chord.Chord([1,4,8])
	cMinor = chord.Chord([0,3,7])
	eMinor = chord.Chord([4,7,11])
	gMinor = chord.Chord([7,10,2])
	fMinor = chord.Chord([5,8,0])
	aMinor = chord.Chord([9,0,4])
	dMinor = chord.Chord([2,5,9])
	bbMinor = chord.Chord([10,1,5])
	cSharpMinor = chord.Chord([1,4,8])
	cMajor = chord.Chord([0,4,7])
	fMajor = chord.Chord([5,9,0])

	chordLineStrings = parseChordsFile(neoTest)
	chordObjList = []
	for cl in chordLineStrings:
		phrase = []
		for cs in cl:
			phrase.append(chordFromString(cs))
		chordObjList.append(phrase)

	totalChords = 0
	for phrase in chordObjList:
		strPhrase = ""
		for i in phrase:
			strPhrase += chordToString(i) + ", "
			totalChords += 1
		strPhrase = strPhrase[:-2]
		#print strPhrase
	#print 'numchords in song ' + str(totalChords)

	#allPaths = []
	#for phrase in chordObjList:
	'''
	uttStrings = []
	for i in range(12):
		uttString = '<-, ' + str(i) + ', ' + str((i + 1) %12) + '>'
		uttStrings.append(uttString)
	for i in range(12):
		uttString = '<+, ' + str(i) + ', ' + str(i) + '>'
		uttStrings.append(uttString)
	print uttStrings

	totalDists = []
	uttSets = []
	for index, u in enumerate(uttStrings):
		for index2, u2 in enumerate(uttStrings):
			if index2 > index:
				uttString = '(' + u + ', 1, A)'
				uttString2 = '(' + u2 + ', 1, B)'
				uttSets.append([uttString, uttString2])
	print uttSets
	
	minDices = [95,103,146,154]
	for m in minDices:
		print uttSets[m]
	minDist, uttPairs = computeDistanceForAllK11UTTs(chordObjList)
	print 'min dist: ' + str(minDist)
	print 'uttPairs: ' + str(uttPairs)
	'''
				
	

	#uttA,uttB,nGraph = createUTTSpaceFromStringsAndStartChord("(<-, 0, 0>, 1, A)", "(<-, 0, 2>, 2, B)", fMajor)
	#uttA,uttB,nGraph = createUTTSpaceFromStringsAndStartChord("(<-, 4, 3>, 1, A)", "(<+, 4, 4>, 1, B)", fMajor)
	#uttA,uttB,nGraph = createUTTSpaceFromStringsAndStartChord("(<-, 4, 5>, 1, A)", "(<+, 2, 2>, 1, B)", eMinor)
	#uttA,uttB,nGraph = createUTTSpaceFromStringsAndStartChord("(<-, 1, 2>, 1, A)", "(<-, 2, 3>, 1, B)", eMinor)
	#uttA,uttB,nGraph = createUTTSpaceFromStringsAndStartChord("(<-, 4, 5>, 1, A)", "(<+, 2, 2>, 1, B)", eMinor)
	#uttA,uttB,nGraph = createUTTSpaceFromStringsAndStartChord("(<-, 1, 2>, 1, A)", "(<+, 2, 2>, 1, B)", eMinor)
	'''uttA,uttB,nGraph = createUTTSpaceFromStringsAndStartChord("(<-, 0, 0>, 1, P)", "(<+, 7, 7>, 100, X)", cMinor, True)
	
	#uttA,uttB,nGraph = createUTTSpaceFromStringsAndStartChord("(<-,0,0>, 1, P)", "(<-, 9, 3>, 1, R)", cMinor)

	print checkUTTSpace(nGraph)

	addShortcut(nGraph, 'X|X|X|P', 1, 'R', True)
	addShortcut(nGraph, 'X|X|X|X|P', 1, 'L', True)
	addShortcut(nGraph, 'R|L', 1.9, 'RL', True)

	#searchPath = shortestPath(nGraph, chordCompare, nGraph[-1][0], bbMinor)
	#print getDistancesAndTransformationsFromPath(nGraph, searchPath)
	#print [chordToString(i.chord)  for i in searchPath]
	
	print2DNodeGraph(nGraph)
	#paths = computePathsForChordPhrase(nGraph, chordObjList[0])
	songDistances = getDistAndTransForSong(nGraph, chordObjList)
	printDistancesForSong(songDistances)'''
	#printDistancesAndChordPhrasesForSong(songDistances, chordObjList)
	#for path in paths:
	#	print path
	#print paths[0][1].chord
	#print str(getDistancesAndTransformationsFromPath(nGraph, paths[0]))

	
	'''
	def setDistance(triad1, triad2):
		return min(UTT1.distance(triad1,triad2), UTT2.distance(triad1,triad2)) / 2

	for e in G.edges():
		print str(e)
	endChord = chord.Chord([2,6,9])
	chordSpace = UTT1.space + UTT2.space

	print str(UTT1.distance(startChord, endChord))
	#G.add_nodes_from(chordSpace)
	#G.add_edge(startChord, endChord)
	print(nx.astar_path(G, G.nodes()[12], G.nodes()[20], setDistance))'''

if __name__ == "__main__":
    main()