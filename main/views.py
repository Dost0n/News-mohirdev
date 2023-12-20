from pyexpat import model
from turtle import title
from django.shortcuts import render, get_object_or_404
from main.forms import ContactForm, CommentForm
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, DetailView, CreateView
from main.models import News, Category, Comment
from datetime import date
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from News.custom_permission import OnlyLoggedSuperUser
from django.db.models import Q
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountDetailView, HitCountMixin

def home(request):
    categories = Category.objects.all()
    important_posts = News.objects.all()[:3]
    popular_posts = News.objects.order_by('-publish_time')[:4]
    business_posts = News.objects.filter(category__name='Biznes')[:5]
    technology_posts = News.objects.filter(category__name='Texnologiya')[:5]
    nationality_posts = News.objects.filter(category__name='Mahalliy')[:5]
    context = {
        'categories':categories,
        'important_posts':important_posts,
        'popular_posts':popular_posts,
        'business_posts':business_posts,
        'technology_posts':technology_posts,
        'nationality_posts':nationality_posts,
        'date':date.today().strftime("%d.%m.%Y")
    }
    return render(request, 'index.html', context)


class Homeview(ListView):
    template_name = 'index.html'
    model = News
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = self.model.objects.all()
        context['categories'] = Category.objects.all()
        context['important_posts'] = News.objects.all()[:3]
        context['popular_posts'] = News.objects.order_by('-publish_time')[:4]
        context['business_posts'] = News.objects.filter(category__name='Biznes')[:5]
        context['technology_posts'] = News.objects.filter(category__name='Texnologiya')[:5]
        context['nationality_posts'] = News.objects.filter(category__name='Mahalliy')[:5]
        context['date'] = date.today().strftime("%d.%m.%Y")
        return context


class NewsCreateView(LoginRequiredMixin, CreateView):
    template_name = 'news_create.html'
    model = News
    fields = ('title','title_en','title_ru','body','body_en','body_ru', 'image', 'category', 'status')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)


class NewsUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'news_update.html'
    model = News
    fields = ('title','title_en','title_ru','body','body_en','body_ru', 'image', 'category')


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    template_name = 'news_delete.html'
    model = News
    success_url = reverse_lazy('home')


def category(request, pk):
    news = News.objects.all().filter(category__id=pk)
    category_name = Category.objects.get(id=pk)
    categories = Category.objects.all()
    important_posts = News.objects.all()[:3]
    latest_posts = News.objects.all().order_by('-publish_time')[:5]
    popular_posts = News.objects.order_by('-publish_time')[:4]
    context = {
        'categories':categories,
        'category_name':category_name,
        'latest_posts':latest_posts,
        'important_posts':important_posts,
        'popular_posts':popular_posts,
        'date':date.today().strftime("%d.%m.%Y"),
        'news':news,
    }
    return render(request, 'category.html', context)


def error(request):
    categories = Category.objects.all()
    popular_posts = News.objects.order_by('-publish_time')[:4]
    context = {
        'categories':categories,
        'popular_posts':popular_posts,
        'date':date.today().strftime("%d.%m.%Y")
    }
    return render(request, '404.html', context)


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        form.save()
        return HttpResponse("<h2> Biz bilan bog'langaniz uchun tashakkur! <h2>")
    else:
        categories = Category.objects.all()
        popular_posts = News.objects.order_by('-publish_time')[:4]
        context = {
            'categories':categories,
            'popular_posts':popular_posts,
            "form": form,
            'date':date.today().strftime("%d.%m.%Y")
        }
        return render(request, 'contact.html', context)


class ContactView(TemplateView):
    template_name = 'contact.html'
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form":form,
            'date':date.today().strftime("%d.%m.%Y")
        }
        return render(request, 'contact.html', context)
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method=="POST" and form.is_valid():
            form.save()
            return HttpResponse("<h2> Biz bilan bog'langaniz uchun tashakkur! <h2>")
        context = {
            "form":form
        }
        return render(request, 'contact.html', context)



def single(request, news):
    post = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(post)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits+=1
        hitcontext['hit_count'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits


    comments = post.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None
    if request.method=="POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = post
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    categories = Category.objects.all()
    popular_posts = News.objects.order_by('-publish_time')[:4]
    related_posts = News.objects.filter(category__name = post.category).order_by('-publish_time')[:3]
    context = {
        'categories':categories,
        'popular_posts':popular_posts,
        'related_posts':related_posts,
        'post':post,
        'comments':comments,
        'comment_form':comment_form,
        'date':date.today().strftime("%d.%m.%Y"),
        'new_comment':new_comment,
        'comment_count':comment_count
    }
    return render(request, 'news_detail.html', context)


class SearchList(ListView):
    model = News
    template_name = 'search.html'
    context_object_name = 'news'

    def get_queryset(self):
        query = self.request.GET.get('search')
        return News.objects.filter(Q(title__icontains = query) | Q(body__icontains = query))