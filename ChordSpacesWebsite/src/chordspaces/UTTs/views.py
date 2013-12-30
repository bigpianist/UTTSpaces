from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
#from polls.models import Choice, Poll
import string
from chordspaces import *
from music21 import stream, chord, pitch
from DijkstraShortestPath import shortestPath
from Node2D import Node2DGraph



def Graph2D(request, mode_1, major_interval_1, minor_interval_1, mode_2, major_interval_2, minor_interval_2):
    UTT1 = '(<'
    UTT1 += mode_1 + ','
    UTT1 += major_interval_1 + ','
    UTT1 += minor_interval_1 + '>,'
    UTT1 += '1,A)'
    UTT2 = '(<'
    UTT2 += mode_2 + ','
    UTT2 += major_interval_2 + ','
    UTT2 += minor_interval_2 + '>,'
    UTT2 += '1,B)'
    startChord = chord.Chord([10,1,5])
    iterChord = chord.Chord([10,1,5])#"(<-, 2, 3>, 1, S)", "(<-, 4, 5>, 5, T)"
    uttS,uttT,dGraph = createUTTSpaceFromStringsAndStartChord(UTT2, UTT1, startChord)
    context = {'d_graph': dGraph}
    print nodeGraph2DToString(dGraph)
    #for nodeX in dGraph:
    #    for nodeY in nodeX:
    #        print nodeY.chordName
    return render(request, 'UTTs/index.html', context)#UTT1 + ',' + UTT2

"""def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'polls/index.html', context)

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