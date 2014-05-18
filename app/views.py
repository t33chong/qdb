from django.shortcuts import get_object_or_404, render

from app.models import Quote, Tag


def index(request):
    quote_list = Quote.objects.all().order_by('-date')[:5]
    context = {'quote_list': quote_list}
    return render(request, 'app/index.html', context)


def tag(request, tag_id):
    t = get_object_or_404(Tag, pk=tag_id)
    context = {'tag': t}
    return render(request, 'app/tag.html', context)
