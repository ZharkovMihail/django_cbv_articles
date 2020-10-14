from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy

from .forms import ArticleForm
from .models import Articles
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


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


class ArticleCreateView(CustomSuccessMixin, CreateView):
    model = Articles
    slug_field = "url"
    form_class = ArticleForm
    template_name = 'edit_page.html'
    success_url = reverse_lazy('edit_page')
    success_msg = "Запись добавлена"

    def get_context_data(self, **kwargs):
        kwargs['list_articles'] = Articles.objects.all().order_by('-id')
        return super().get_context_data(**kwargs)


class ArticleUpdateView(CustomSuccessMixin, UpdateView):
    model = Articles
    slug_field = "url"
    form_class = ArticleForm
    template_name = 'edit_page.html'
    success_url = reverse_lazy('edit_page')
    success_msg = "Запись обновлена"

    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)


class ArticleDeleteView(DeleteView):
    model = Articles
    slug_field = "url"
    template_name = 'edit_page.html'
    success_url = reverse_lazy('edit_page')
    success_msg = "Запись удалена"

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)


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
