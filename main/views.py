from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User
from .models import Post, Category, Comment


from django.core.paginator import Paginator

from .forms import PostForms

from django.contrib import messages

from django.urls import reverse

from django.views.generic import (
    DetailView,
    UpdateView,
    DeleteView,
)

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)

from django.shortcuts import get_object_or_404

import datetime

from django.db.models import Q
# Create your views here.


def home(request):
    objects = Post.objects.all().order_by('-date_posted')
    paginator = Paginator(objects, 3)

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {
        'posts': posts
    }
    return render(request, 'home.html', context)


def postDetail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    comments = post.comment_set.filter(parent=None)
    replies = post.comment_set.filter().exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.id in replyDict:
            replyDict[reply.parent.id].append(reply)
        else:
            replyDict[reply.parent.id] = [reply]

    context = {
        'post': post,
        'comments': comments,
        'replies': replyDict,
    }
    return render(request, 'post_detail.html', context)


def postCreate(request):
    if request.method == "POST":
        form = PostForms(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "New Post Created Successfully!")
            return redirect(reverse('post-detail', kwargs={'pk': post.id}))
    else:
        form = PostForms()

    context = {
        'form': form
    }
    return render(request, 'post_create.html', context)


class postUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'slug', 'category']
    template_name = 'post_update.html'

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        print(self.request.META.get('HTTP_REFERER'))
        return redirect('profile')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class postDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = '/profile'

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False


def postUser(request, name):
    user = get_object_or_404(User, username=name)
    objects = user.post_set.all()

    paginator = Paginator(objects, 3)

    page_num = request.GET.get('page')
    posts = paginator.get_page(page_num)
    context = {
        'posts': posts,
        'author': user,
        'total_post': objects.count()
    }
    return render(request, 'post_user.html', context)


def postCategory(request, name):
    category = get_object_or_404(Category, name=name)
    objects = category.post_set.all()

    paginator = Paginator(objects, 3)

    page_num = request.GET.get('page')

    posts = paginator.get_page(page_num)
    context = {
        'posts': posts,
        'category': category,
        'total_post': objects.count()
    }
    return render(request, 'post_category.html', context)


def postSearch(request):
    query = request.GET.get('query',"")
    if len(query) > 78:
        posts = Post.objects.none()
    else:
        time1 = datetime.datetime.now()
        objects = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        paginator = Paginator(objects, 3)
        page_num = request.GET.get('page')
        posts = paginator.get_page(page_num)
        time2 = datetime.datetime.now()
        time = time2.microsecond - time1.microsecond
    context = {
        'posts': posts,
        'total_posts': posts.paginator.count,
        'time': str(time)[0:2],
        "query":query
    }
    return render(request, 'post_search.html', context)


def comment(request, pk):
    if request.method == "POST":
        post = Post.objects.get(id=pk)
        user = request.user
        comment = request.POST.get('comment')
        parentid = request.POST.get('parentid')

        if parentid:
            parent = Comment.objects.get(id=parentid)
            commentPost = Comment(post=post, user=user,
                                  comment=comment, parent=parent)
            commentPost.save()
        else:
            commentPost = Comment(post=post, user=user, comment=comment)
            commentPost.save()

    return redirect(reverse('post-detail', kwargs={'pk': pk}))
