from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView

from password_required.decorators import password_required

from app.forms import QuoteForm, UserForm
from app.models import Quote, Tag


@login_required
def index(request):
    quote_list = Quote.objects.all().order_by('-date')[:5]
    context = {'quote_list': quote_list}
    return render(request, 'app/index.html', context)


@login_required
def detail(request, quote_id):
    q = get_object_or_404(Quote, pk=quote_id)
    context = {'quote': q}
    return render(request, 'app/detail.html', context)


@login_required
def tag(request, tag_id):
    t = get_object_or_404(Tag, pk=tag_id)
    context = {'tag': t}
    return render(request, 'app/tag.html', context)


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
            messages.error(request, 'Invalid login details. Please try again.')
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
        tag_string = request.POST['tag_string']
        tag_texts = [
            Tag.make_valid_tag(text.strip()) for text in tag_string.split(',')]
        tags = []
        for text in tag_texts:
            tag = Tag.objects.filter(text=text)
            if tag is None:
                tag = Tag(text=text)
                tag.save()
            tags.append(tag)
        quote = Quote(
            text=request.POST['text'],
            submitter=request.user,
            date=request.POST['date'],
            tags=tags,
            num_upvotes=request.POST['num_upvotes'],
            num_downvotes=request.POST['num_downvotes'],
            )
        quote.save()
        return redirect('app/detail.html', quote=quote)
    form = QuoteForm()
    context = {'form': form}
    return render(request, 'app/submit.html', context)


class Submit(CreateView):
    template_name = 'app/submit.html'
    form_class = QuoteForm
    model = Quote

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Submit, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.submitter = self.request.user
        return super(Submit, self).form_valid(form)

    def get_success_url(self):
        return reverse('app:detail', args=(self.object.id,))
