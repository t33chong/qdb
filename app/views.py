from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
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
                return render(request, 'app/disabled.html', {})
        else:
            print 'Invalid login details: %s, %s' % (username, password)
            # Eventually do this with a flash message
            messages.error(request, 'Invalid login details. Please try again.')
            #return render(request, 'app/invalid.html', {})
    else:
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'app/login.html', context)


@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('app:login'))


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
