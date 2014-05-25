import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from password_required.decorators import password_required

from app.forms import QuoteForm, UserForm
from app.models import Quote, Tag, Upvote, Downvote


def _get_votes(user, quote_ids):
    curr_upvotes = []
    curr_downvotes = []
    if user.is_authenticated():
        curr_upvotes = [u.quote_id for u in
                        Upvote.objects.filter(quote__id__in=quote_ids,
                                              user=user)]
        curr_downvotes = [d.quote_id for d in
                          Downvote.objects.filter(quote__id__in=quote_ids,
                                                  user=user)]
    return curr_upvotes, curr_downvotes


@login_required
def index(request):
    quotes = Quote.objects.all().order_by('-date')
    page = None
    if quotes is not None:
        p = Paginator(quotes, settings.PER_PAGE)
        try:
            page_num = int(request.GET.get('page', '1'))
        except ValueError:
            page_num = 1
        try:
            page = p.page(page_num)
        except PageNotAnInteger:
            page = p.page(1)
        except EmptyPage:
            page = p.page(p.num_pages)
    context = {'page': page}
    return render(request, 'app/index.html', context)


@login_required
def top(request):
    # TODO: Implement voting
    quotes = Quote.objects.all().order_by('-score')
    page = None
    if quotes is not None:
        p = Paginator(quotes, settings.PER_PAGE)
        try:
            page_num = int(request.GET.get('page', '1'))
        except ValueError:
            page_num = 1
        try:
            page = p.page(page_num)
        except PageNotAnInteger:
            page = p.page(1)
        except EmptyPage:
            page = p.page(p.num_pages)
    context = {'page': page}
    return render(request, 'app/top.html', context)


@login_required
def detail(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    context = {'quote': quote}
    return render(request, 'app/detail.html', context)


@login_required
def tag(request, tag_text):
    tag = Tag.objects.filter(text=tag_text).first()
    page = None
    if tag is not None:
        quotes = tag.quotes.all().order_by('-date')
        if quotes is not None:
            p = Paginator(quotes, settings.PER_PAGE)
            try:
                page_num = int(request.GET.get('page', '1'))
            except ValueError:
                page_num = 1
            try:
                page = p.page(page_num)
            except PageNotAnInteger:
                page = p.page(1)
            except EmptyPage:
                page = p.page(p.num_pages)
    context = {'tag_text': tag_text, 'page': page}
    return render(request, 'app/tag.html', context)


@login_required
def user(request, username):
    user = User.objects.filter(username=username).first()
    page = None
    if user is None:
        context = {'username': username}
        return render(request, 'app/user_does_not_exist.html', context)
    quotes = user.quotes.all().order_by('-date')
    if quotes is not None:
        p = Paginator(quotes, settings.PER_PAGE)
        try:
            page_num = int(request.GET.get('page', '1'))
        except ValueError:
            page_num = 1
        try:
            page = p.page(page_num)
        except PageNotAnInteger:
            page = p.page(1)
        except EmptyPage:
            page = p.page(p.num_pages)
    context = {'username': username, 'page': page}
    return render(request, 'app/user.html', context)


@login_required
def search(request):
    params = request.GET.copy()
    if 'page' in params:
        del params['page']
    query = params.get('q')
    if query is None:
        return HttpResponse('Please enter a valid search query.')
    quotes = Quote.search_manager.search(query, rank_field='rank')
    page = None
    path = None
    if quotes is not None:
        p = Paginator(quotes, settings.PER_PAGE)
        try:
            page_num = int(request.GET.get('page', '1'))
        except ValueError:
            page_num = 1
        try:
            page = p.page(page_num)
        except PageNotAnInteger:
            page = p.page(1)
        except EmptyPage:
            page = p.page(p.num_pages)
        path = params.urlencode()
    context = {'params': params, 'page': page, 'path': path}
    return render(request, 'app/search.html', context)


@password_required
def signup(request):
    registered = False
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password'])
            login(request, user)
            return HttpResponseRedirect(reverse('app:index'))
        else:
            print form.errors
    else:
        form = UserForm()
    context = {'form': form, 'registered': registered}
    return render(request, 'app/signup.html', context)


def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('app:index'))
                else:
                    messages.error(request, 'Your account is disabled.')
            else:
                print 'Invalid login details: %s, %s' % (username, password)
                messages.error(
                    request, 'Invalid login details. Please try again.')
        else:
            print form.errors
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'app/login.html', context)


@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('app:login'))


@login_required
def submit(request):
    if request.method == 'POST':
        quote = Quote(
            text=request.POST['text'],
            submitter=request.user,
            )
        quote.save()
        tag_string = request.POST['tag_string']
        if len(tag_string) > 0:
            tag_texts = [Tag.make_valid_tag(text.strip()) for text in
                         tag_string.split(',')]
            for text in tag_texts:
                if len(text) > 0:
                    tag = Tag.objects.filter(text=text).first()
                    if tag is None:
                        tag = Tag(text=text)
                        tag.save()
                    quote.tags.add(tag)
        return redirect(reverse('app:detail', args=(quote.id,)))
    form = QuoteForm()
    context = {'form': form}
    return render(request, 'app/submit.html', context)


@require_POST
@login_required
def upvote(request, quote_id):
    try:
        quote = Quote.objects.get(id=quote_id)
    except ObjectDoesNotExist:
        return HttpResponse(
            json.dumps({'message': 'Quote not found'}), status=404)
    try:
        current_downvote = Downvote.objects.get(quote=quote, user=request.user)
        current_downvote.delete()
    except ObjectDoesNotExist:
        pass
    try:
        current_upvote = Upvote.objects.get(quote=quote, user=request.user)
        if request.POST.get('delete'):
            current_upvote.delete()
            return HttpResponse(
                json.dumps({'message': 'Upvote deleted'}), status=200)
        return HttpResponse(
            json.dumps({'message': 'Already upvoted'}), status=200)
    except ObjectDoesNotExist:
        if not request.POST.get('delete'):
            new_upvote = Upvote()
            new_upvote.quote = quote
            new_upvote.user = request.user
            new_upvote.save()
    return HttpResponse(
        json.dumps({'message': 'Upvote successful'}), status=200)


@require_POST
@login_required
def downvote(request, quote_id):
    try:
        quote = Quote.objects.get(id=quote_id)
    except ObjectDoesNotExist:
        return HttpResponse(
            json.dumps({'message': 'Quote not found'}), status=404)
    try:
        current_upvote = Upvote.objects.get(quote=quote, user=request.user)
        current_upvote.delete()
    except ObjectDoesNotExist:
        pass
    try:
        current_downvote = Downvote.objects.get(quote=quote, user=request.user)
        if request.POST.get('delete'):
            current_downvote.delete()
            return HttpResponse(
                json.dumps({'message': 'Downvote deleted'}), status=200)
        return HttpResponse(
            json.dumps({'message': 'Already Downvoted'}), status=200)
    except ObjectDoesNotExist:
        if not request.POST.get('delete'):
            new_downvote = Downvote()
            new_downvote.quote = quote
            new_downvote.user = request.user
            new_downvote.save()
    return HttpResponse(
        json.dumps({'message': 'Downvote successful'}), status=200)
