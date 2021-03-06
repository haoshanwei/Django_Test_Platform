# coding:utf-8
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import ArticleColumn,ArticlePost,Comment
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.core import serializers
from .forms import CommentForm
import json



def article_titles(request,username = None):
    if username:
        user = User.objects.get(username = username)
        article_title = ArticlePost.objects.filter(author = user)
        try:
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        article_title = ArticlePost.objects.all()
    paginator = Paginator(article_title,5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    if username:
        return render(request,"article/list/author_articles.html",{"articles":articles,"page":current_page,"userinfo":userinfo,"user":user})
    return render(request,"article/list/article_titles.html",{"articles":articles,"page":current_page})

def article_detail(request,id,slug):
    article = get_object_or_404(ArticlePost,id = id,slug = slug)
    if request.method == "POST":
        # comment_form = CommentForm(data = request.POST)
        comment_form = CommentForm(data = request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
            return HttpResponse("1")
    else:
        comment_form = CommentForm()
    # print comment_form
    return render(request,"article/list/article_detail.html",{"article":article,"comment_form":comment_form})

@csrf_exempt
@require_POST
@login_required(login_url = '/account/new-login')
def like_article(request):
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id = article_id)
            if action == "like":
                article.users_like.add(request.user)
                return HttpResponse("1")
            else:
                article.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no")


def del_comment(request):
    id = request.POST['comment_id']
    try:
        comment = Comment.objects.get(id =id)
        comment.delete()
        return HttpResponse('0')
    except:
        return HttpResponse("1")
    

##########################################
def article_titles_filter(request):
    user = User.objects.get(username = request.POST.get('username'))
    article_title = ArticlePost.objects.filter(author = user)
    try:
        userinfo = user.userinfo
    except:
        userinfo = None
    paginator = Paginator(article_title,5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_lis
    return render(request,"article/list/article_titles.html",{"articles":articles,"page":current_page})