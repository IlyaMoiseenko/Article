from django.views import generic
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect

from blog import models
from blog.forms import ArticleAddForm, SignInForm, SignUpForm, CommentForm


class HomeListView(generic.ListView):
    model = models.Article
    template_name = 'index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        return models.Article.objects.all().order_by('-id')


class ArticleDetailView(FormMixin, generic.DetailView):
    model = models.Article
    template_name = 'article-detail.html'
    context_object_name = 'article'

    form_class = CommentForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('article-detail', kwargs={'pk':self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.article = self.get_object()
        self.object.author = self.request.user
        self.object.save()

        return super().form_valid(form)


class ArticleCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Article
    template_name = 'user-articles.html'
    form_class = ArticleAddForm
    success_url = reverse_lazy('user-articles')
    login_url = reverse_lazy('sign-in')
    context_object_name = 'article'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        articles = models.Article.objects.filter(author=self.request.user)

        context['articles'] = articles

        return context


class ArticleEditView(LoginRequiredMixin, generic.UpdateView):
    model = models.Article
    template_name = 'article-edit.html'
    form_class = ArticleAddForm
    success_url = reverse_lazy('user-articles')
    login_url = reverse_lazy('sign-in')
    context_object_name = 'article'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()

        return kwargs


class ArticleDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Article
    template_name = 'article_confirm_delete.html'
    success_url = reverse_lazy('user-articles')
    login_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        if self.request.user != self.get_object().author:
            return self.handle_no_permission()

        self.object.delete()

        return HttpResponseRedirect(self.success_url)


class SignInView(LoginView):
    template_name = 'sign_in.html'
    form_class = SignInForm
    success_url = reverse_lazy('index')

    def get_success_url(self):
        return self.success_url


class SignUpView(generic.CreateView):
    model = User
    template_name = 'sign_up.html'
    success_url = reverse_lazy('index')
    form_class = SignUpForm

    def form_valid(self, form):
        form_valid = super().form_valid(form)

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        login(self.request,
              authenticate(username=username, password=password))

        return form_valid


class LogOutView(LogoutView):
    next_page = reverse_lazy('index')
