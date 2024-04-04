from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TagForm, AuthorForm, QuoteForm
from .models import Tag, Author, Quote
from django.db.models import Count
from .features.scraping import scrapyng
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def main(request, tag_id=None):
    if request.GET.get('tag_id') != None:
        tag = Tag.objects.get(id=request.GET.get('tag_id'))
        quotes = Quote.objects.filter(tags=tag)
    else:
        quotes = Quote.objects.all()

    tag_size_block = list(range(28, 8, -2))
    most_used_tags = get_most_used_tags()

    # def main(request, tag_id=None):
    # for url
    # http://127.0.0.1:8000/2
    # if tag_id != None:
    #     # quotes = Quote.objects.all()
    #     tag = Tag.objects.get(id=tag_id)
    #     quotes = Quote.objects.filter(tags=tag)

    # Pagination
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get('page')
    try:
        quotes = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        quotes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        quotes = paginator.page(paginator.num_pages)

    return render(request, 'quoteapp/index.html', {"quotes": quotes, "tag_size_block": tag_size_block, "most_used_tags": most_used_tags})


@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/tag.html', {'form': form})

    return render(request, 'quoteapp/tag.html', {'form': TagForm()})


@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/author.html', {'form': form})

    return render(request, 'quoteapp/author.html', {'form': AuthorForm()})


@login_required
def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.author_id = request.POST['author']  
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)     

            # new_quote.save()

            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/quote.html', {"authors": authors, "tags": tags, 'form': form})

    return render(request, 'quoteapp/quote.html', {"authors": authors, "tags": tags, 'form': QuoteForm()})


def detail(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    author = get_object_or_404(Author, pk=quote.author_id)
    return render(request, 'quoteapp/detail.html', {"quote": quote, "author": author})


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quoteapp/author_detail.html', {"author": author})


def delete_quote(request, quote_id):
    Quote.objects.get(pk=quote_id).delete()
    return redirect(to='quoteapp:main')


def get_most_used_tags():
    most_used_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    return most_used_tags


@login_required
def scrapy(request):
    return render(request, 'quoteapp/scrapy.html')


@login_required
def scrapyng_quotes(request):
    scrapy = scrapyng()
    scrapy.scrapyng_quotes()

    return redirect(to='quoteapp:main')
