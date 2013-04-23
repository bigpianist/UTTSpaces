# Dijkstra's algorithm for shortest paths
# Adapted from David Eppstein, UC Irvine, 4 April 2002

# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117228
from priodict import priorityDictionary
from Node2D import Node2DGraph

def Dijkstra(graph,vertexCompare,start,end=None):
	"""
	Find shortest paths from the start vertex to all
	vertices nearer than or equal to the end.

	The input graph G is assumed to have the following
	representation: A vertex can be any object that can
	be used as an index into a dictionary.  G is a
	dictionary, indexed by vertices.  For any vertex v,
	G[v] is itself a dictionary, indexed by the neighbors
	of v.  For any edge v->w, G[v][w] is the length of
	the edge.  This is related to the representation in
	<http://www.python.org/doc/essays/graphs.html>
	where Guido van Rossum suggests representing graphs
	as dictionaries mapping vertices to lists of neighbors,
	however dictionaries of edges have many advantages
	over lists: they can store extra information (here,
	the lengths), they support fast existence tests,
	and they allow easy modification of the graph by edge
	insertion and removal.  Such modifications are not
	needed here but are important in other graph algorithms.
	Since dictionaries obey iterator protocol, a graph
	represented as described here could be handed without
	modification to an algorithm using Guido's representation.

	Of course, G and G[v] need not be Python dict objects;
	they can be any other object that obeys dict protocol,
	for instance a wrapper in which vertices are URLs
	and a call to G[v] loads the web page and finds its links.

	The output is a pair (D,P) where D[v] is the distance
	from start to v and P[v] is the predecessor of v along
	the shortest path from s to v.

	Dijkstra's algorithm is only guaranteed to work correctly
	when all edge lengths are positive. This code does not
	verify this property for all edges (only the edges seen
 	before the end vertex is reached), but will correctly
	compute shortest paths even for some graphs with negative
	edges, and will raise an exception if it discovers that
	a negative edge has caused it to make a mistake.
	"""
	'''Original:
		final_distances = {}	# dictionary of final distances
		predecessors = {}	# dictionary of predecessors
		estimated_distances = priorityDictionary()   # est.dist. of non-final vert.
		estimated_distances[start] = 0

		for vertex in estimated_distances:
			final_distances[vertex] = estimated_distances[vertex]
			if vertex == end: break

			for neighbor in vertex.neighbors:
				
				path_distance = final_distances[vertex] + graph[vertex][edge]
				if edge in final_distances:
					if path_distance < final_distances[edge]:
						raise ValueError, \
	  "Dijkstra: found better path to already-final vertex"
				elif edge not in estimated_distances or path_distance < estimated_distances[edge]:
					estimated_distances[edge] = path_distance
					predecessors[edge] = vertex

		return (final_distances,predecessors)
	'''
	final_distances = {}	# dictionary of final distances
	predecessors = {}	# dictionary of predecessors
	estimated_distances = priorityDictionary()   # est.dist. of non-final vert.
	estimated_distances[start] = 0
	endVertex = ''
	for vertex in estimated_distances:
		#vertex is a graph node, with chord and neighbors
		final_distances[vertex] = estimated_distances[vertex]
		if vertexCompare(vertex.chord, end): 
			endVertex = vertex
			break

		for neighbor in vertex.neighbors:
			#neighbor is a list of the neighbor's [x,y] indices @[0] and its distance @[1]
			nIndX = neighbor[0][0]
			nIndY = neighbor[0][1]
			neighborVertex = graph[nIndX][nIndY]
			path_distance = final_distances[vertex] + neighbor[1]#graph[vertex][edge]
			#if edge in final_distances:
			#if chordToString(neighbor.chord) in [chordToString(i.chord) for i in final_distances]:
			if neighborVertex in final_distances:
				if path_distance < final_distances[neighborVertex]:#probably won't trigger for dupe chords, because their objects will differ
					raise ValueError, \
  "Dijkstra: found better path to already-final vertex"
  			#elif edge not in estimated_distances or path_distance < estimated_distances[edge]:
			elif neighborVertex not in estimated_distances or path_distance < estimated_distances[neighborVertex]:
				estimated_distances[neighborVertex] = path_distance
				predecessors[neighborVertex] = vertex
	if endVertex == '':
		print 'could not find it'
	return (final_distances,predecessors,endVertex)

def shortestPath(graph,vertexCompare,start,end):
	"""
	Find a single shortest path from the given start vertex
	to the given end vertex.
	The input has the same conventions as Dijkstra().
	The output is a list of the vertices in order along
	the shortest path.
	"""
	#print 'finding path from start: ' + start.nodeToString() + ' to ' + str(end)	

	final_distances,predecessors,endVertex = Dijkstra(graph,vertexCompare,start,end)
	if endVertex =='':
		return -1

	path = []
	while 1:
		path.append(endVertex)
		if vertexCompare(endVertex.chord, start.chord): break
		endVertex = predecessors[endVertex]
	path.reverse()
	return path