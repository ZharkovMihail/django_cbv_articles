from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy

from .forms import ArticleForm, AuthUserForm, RegisterUserForm
from .models import Articles
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User


class HomeListView(ListView):
    model = Articles
    template_name = 'index.html'
    context_object_name = 'list_articles'


class HomeDetailView(DetailView):
    model = Articles
    slug_field = "url"
    template_name = 'detail.html'
    context_object_name = 'get_article'


class CustomSuccessMixin:
    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)


class ArticleCreateView(LoginRequiredMixin, CustomSuccessMixin, CreateView):
    model = Articles
    slug_field = "url"
    form_class = ArticleForm
    template_name = 'edit_page.html'
    success_url = reverse_lazy('edit_page')
    success_msg = "Запись добавлена"
    # login_url = 'login_page'

    def get_context_data(self, **kwargs):
        kwargs['list_articles'] = Articles.objects.all().order_by('-id')
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, CustomSuccessMixin, UpdateView):
    model = Articles
    slug_field = "url"
    form_class = ArticleForm
    template_name = 'edit_page.html'
    success_url = reverse_lazy('edit_page')
    success_msg = "Запись обновлена"

    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Articles
    slug_field = "url"
    template_name = 'edit_page.html'
    success_url = reverse_lazy('edit_page')
    success_msg = "Запись удалена"

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class MyLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('edit_page')
    form_class = AuthUserForm

    def get_success_url(self):
        return self.success_url


class RegisterUserView(CreateView):
    model = User
    template_name = 'register_page.html'
    success_url = reverse_lazy('edit_page')
    form_class = RegisterUserForm
    success_msg = "Пользователь успешно создан"

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('edit_page')


def edit_page(request):
    success = False
    mistake = False
    template = 'edit_page.html'

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
        else:
            context = {
                'form': form,
                'list_articles': Articles.objects.all().order_by('-id'),
                'success': False,
                'mistake': True,
            }
            return render(request, template, context)

    context = {
        'list_articles': Articles.objects.all().order_by('-id'),
        'form': ArticleForm(),
        'success': success,
        'mistake': mistake,
    }
    return render(request, template, context)


def update_page(request, slug):
    success_update = False
    get_article = Articles.objects.get(url=slug)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=get_article)
        if form.is_valid():
            form.save()
            success_update = True
    template = 'edit_page.html'
    context = {
        'get_article': get_article,
        'update': True,
        'form': ArticleForm(instance=get_article),
        'success_update': success_update

    }
    return render(request, template, context)


def delete_page(request, slug):
    get_article = Articles.objects.get(url=slug)
    get_article.delete()

    return redirect(reverse('edit_page'))
