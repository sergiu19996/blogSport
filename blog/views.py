from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.contrib.postgres.search import TrigramSimilarity
from .forms import EmailPostForm, CommentForm, SearchForm
from django.views.decorators.http import require_POST
from taggit.models import Tag


# Create your views here.

def post_search(request):
    form = SearchForm()
    query = None
    results = []


    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.published.annotate(similarity=TrigramSimilarity('title', query),
                ),filter(similarity__gt=0.1).order_by('-similarity').filter(search=query)

    return render (request,
                   'blog/post/search.html',
                   {'form': form,
                    'query': query,
                    'results': results})        
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Save the comment the database 
        comment.save()
    return render(request, 'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})


class PostListView(ListView):
    """
    Alternative post list view

    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

    
def post_detail(request, id):
    post = get_object_or_404(Post,
                             id=id,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish_year=year,
                             publish_month=month,
                             publish_day=day)
    # List of active comments for this post
    Comment = post.comments.filter(active=True)
    # Form for users ro comment
    form = CommentForm()
    # List of similar posts 
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                          .exclude(id=post.id)
                                          similar_posts = similar_posts.annotate(same_tags=count('tags'))\
                                          .order_by('-same_tags', '-publish')[:4]
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts})  

def post_list(request, tag_slug=None):
    posts = Post.published.all()
    Tag = None
    if tag_slug:
    tag = get_object_or_404(Tag, slug=tag_slug)
    post_list = post_list.filter(tags__in=[tag])
    # Pagination with 3 posts per page 
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page 
        posts = paginator.page(1)
    except EmptyPage:
        #If page_number is out of range deliver last page of results 
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'tag': tag}) 

# Create your views here.
