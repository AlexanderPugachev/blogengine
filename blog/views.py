from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Post, Tag
from .utils import *
from .forms import TagForm, PostForm
from django.db.models import Q

# выдача карточек с постами в блоке карточек
def posts_list(request):
    # фильтр для постов
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()
    amount = 4 # число выводимых постов на страницу
    paginator = Paginator(posts, amount)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    # отвечает за функционирование кнопок previous, next в навигации
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context={
    'page_object': page,
    'is_paginated': is_paginated,
    'next_url': next_url,
    'prev_url': prev_url
    }
    return render(request, 'blog/index.html', context=context)

# выдача списка с тегами
def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})

# работа с постами
class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'

class PostCreate(ObjectCreateMixin, View):
    form_model = PostForm
    template = 'blog/post_create.html'

class PostUpdate(ObjectUpdateMixin, View):
    model = Post
    form_model = PostForm
    template = 'blog/post_update.html'

class PostDelete(ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete.html'
    return_url = 'post_list_url'

# работа с тегами
class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'

class TagCreate(ObjectCreateMixin, View):
    form_model = TagForm
    template = 'blog/tag_create.html'

class TagUpdate(ObjectUpdateMixin, View):
    model = Tag
    form_model = TagForm
    template = 'blog/tag_update.html'

class TagDelete(ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete.html'
    return_url = 'tags_list_url'
