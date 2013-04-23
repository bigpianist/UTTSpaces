

def chordToString(chordObj):
	return (chordObj.pitches[0].name + ' ' + chordObj.commonName).replace(' triad', '')

class Node2DGraph:
	chord = ""
	xInd = -1
	yInd = -1
	# neighbors will be a sorted list of the neighboring nodes indices in the 2d graph, assigned with their corresponding distance, and their transformationID (i.e., [[1,3], 2, 'S'])
	neighbors = []

	def __init__(self, chordObj, xVal, yVal):
		self.chord = chordObj
		self.xInd = xVal
		self.yInd = yVal
		self.neighbors = []

	def addNeighbor(self, node, distance, identifier):
		neighborIndex = [node.xInd, node.yInd]
		neighborTuple = [neighborIndex, distance, identifier]
		#print 'neighbors is: ' + str(len(self.neighbors))
		if neighborTuple in self.neighbors:
			print "Already have that neighborino"
			return
		if not self.neighbors:
			self.neighbors.append(neighborTuple)
			return
		else:
			added = False
			for i, n in enumerate(self.neighbors):
				if n[1] >= distance:
					self.neighbors.insert(i, neighborTuple)
					added = True
					break
			if not added:
				self.neighbors.append(neighborTuple)


	def neighborsToString(self, graph):
		neigh = ""
		if not self.neighbors:
			print 'you have no neighbors, idiot'
			return ""
		for n in self.neighbors:
			#print 'found neighbor: ' + str(n)
			nIndices = n[0]
			neigh += graph[nIndices[0]][nIndices[1]].nodeToString() + ':' + str(n[1]) +'\n'
		return neigh 

	def nodeToString(self):
		nString = 'g[' + str(self.xInd) + ',' + str(self.yInd) + ']:'
		nString += chordToString(self.chord)
		return nString