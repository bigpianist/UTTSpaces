from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
#from polls.models import Choice, Poll
import string
from chordspaces import *
from music21 import stream, chord, pitch
from DijkstraShortestPath import shortestPath
from Node2D import Node2DGraph


def createUTTStrings(mode_1, major_interval_1, minor_interval_1, name_1, mode_2, major_interval_2, minor_interval_2, name_2):
    UTT1 = '(<'
    UTT1 += mode_1 + ','
    UTT1 += major_interval_1 + ','
    UTT1 += minor_interval_1 + '>,'
    UTT1 += '1,' 
    UTT1 += name_1 + ')'
    UTT2 = '(<'
    UTT2 += mode_2 + ','
    UTT2 += major_interval_2 + ','
    UTT2 += minor_interval_2 + '>,'
    UTT2 += '1,' 
    UTT2 += name_2 + ')'
    UTTs = []
    UTTs.append(UTT1)
    UTTs.append(UTT2)
    return UTTs

def Graph2D(request, mode_1, major_interval_1, minor_interval_1, name_1, mode_2, major_interval_2, minor_interval_2, name_2):
    [UTT1, UTT2] = createUTTStrings(mode_1, major_interval_1, minor_interval_1, name_1, mode_2, major_interval_2, minor_interval_2, name_2)
    
    startChord = chord.Chord([0,4,7])
    uttS,uttT,dGraph = createUTTSpaceFromStringsAndStartChord(UTT1, UTT2, startChord)

    yMax = len(dGraph[0]) - 1
    xMax = len(dGraph) - 1
    context = {'d_graph': dGraph, 'mode_1': mode_1, 'major_interval_1': major_interval_1, 'minor_interval_1': minor_interval_1, 'name_1': name_1, 'mode_2': mode_2, 'major_interval_2': major_interval_2, 'minor_interval_2': minor_interval_2, 'name_2': name_2, 'isValidGraph' : checkUTTSpace(dGraph), 'xMax': xMax, 'yMax': yMax}
    print nodeGraph2DToString(dGraph)
    #for nodeX in dGraph:
    #    for nodeY in nodeX:
    #        print nodeY.chordName
    return render(request, 'UTTs/graphxml.html', context)#UTT1 + ',' + UTT2

#Since both the front end and back end have access to the same graph, 
#I just passed the indices of the nodes that I want to search
#There is a problem with that, which is that sometimes the shortest path points to a closer node
def GraphPath(request, mode_1, major_interval_1, minor_interval_1, name_1, mode_2, major_interval_2, minor_interval_2, name_2, x1, y1, x2, y2):
    [UTT1, UTT2] = createUTTStrings(mode_1, major_interval_1, minor_interval_1, name_1, mode_2, major_interval_2, minor_interval_2, name_2)

    startChord = chord.Chord([0,4,7])
    uttS,uttT,dGraph = createUTTSpaceFromStringsAndStartChord(UTT1, UTT2, startChord)

   
    #print "finding path from chord '" + dGraph[int(x1)][int(y1)].chordName + "' to '" + dGraph[int(x2)][int(y2)].chordName + "'"
    #print "finding path from chord '" + chordToString(dGraph[int(x1)][int(y1)].chord) + "' to '" + chordToString(dGraph[int(x2)][int(y2)].chord) + "'"
    shortPath = shortestPath(dGraph, chordCompare, dGraph[int(x1)][int(y1)], dGraph[int(x2)][int(y2)].chord)
    distTransTuple = getDistancesAndTransformationsFromPath(dGraph, shortPath)
    #print [chordToString(i.chord) + ':'  for i in shortPath]
    context = {'shortestPath': shortPath, 'distance': distTransTuple[0], 'transformations': distTransTuple[1]}
    #print nodeGraph2DToString(dGraph)
    #for nodeX in dGraph:
    #    for nodeY in nodeX:
    #        print nodeY.chordName
    return render(request, 'UTTs/path.html', context)#UTT1 + ',' + UTT2

def GraphWithShortcut(request, mode_1, major_interval_1, minor_interval_1, name_1, mode_2, major_interval_2, minor_interval_2, name_2, transString):
    [UTT1, UTT2] = createUTTStrings(mode_1, major_interval_1, minor_interval_1, name_1, mode_2, major_interval_2, minor_interval_2, name_2)
    print "adding shortcut"
    startChord = chord.Chord([0,4,7])
    uttS,uttT,dGraph = createUTTSpaceFromStringsAndStartChord(UTT1, UTT2, startChord)
    distanceDefault  = transString.count('|') + .9
    transReplaced = transString.replace(".", "|")
    print "inputting this into addShortcut: " + transReplaced
    addShortcut(dGraph, transReplaced, distanceDefault, transReplaced)
    yMax = len(dGraph[0]) - 1
    xMax = len(dGraph) - 1
    print "xMax is: " + str(xMax) +", yMax is: " + str(yMax)
    context = {'d_graph': dGraph, 'mode_1': mode_1, 'major_interval_1': major_interval_1, 'minor_interval_1': minor_interval_1, 'name_1': name_1, 'mode_2': mode_2, 'major_interval_2': major_interval_2, 'minor_interval_2': minor_interval_2, 'name_2': name_2, 'isValidGraph' : checkUTTSpace(dGraph), 'xMax': xMax, 'yMax': yMax}
    print nodeGraph2DToString(dGraph)
    return render(request, 'UTTs/graphxml.html', context)


def index(request):
    print "got to index"
    return render(request, 'UTTs/index.html', {})
"""
def detail(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    return render(request, 'polls/detail.html', {'poll': poll})

def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/results.html', {'poll': poll})

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))"""