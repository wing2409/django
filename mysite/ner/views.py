from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from ner_module import ner_model

def index(request):
    return render(request, 'index.html', {'result': '11111111'})


def vote(request):

    print(ner_model.Parser().predict('안녕 안녕 하이 방가'))


    return render(request, 'index.html', {'result': '22222222222222222'})
    #return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))