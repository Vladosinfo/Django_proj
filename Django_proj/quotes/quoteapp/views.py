from django.shortcuts import render, redirect
from .forms import TagForm, AuthorForm, QuoteForm
from .models import Tag, Author, Quote


def main(request):
    return render(request, 'quoteapp/index.html')


def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/tag.html', {'form': form})

    return render(request, 'quoteapp/tag.html', {'form': TagForm()})


def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/author.html', {'form': form})

    return render(request, 'quoteapp/author.html', {'form': AuthorForm()})


def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == 'POST':
        # print(f"request.POST.authors: {request.POST['authors']}")
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()

            # choice_authors = Author.objects.filter(fullname__in=request.POST.getlist('authors'))
            # for author in choice_authors.iterator():
            #     new_quote.authors.add(author)

            # choice_authors = Author.objects.filter(fullname=request.POST['authors'])
            # new_quote.authors.add(choice_authors)

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)     

            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/quote.html', {"authors": authors, "tags": tags, 'form': form})

    return render(request, 'quoteapp/quote.html', {"authors": authors, "tags": tags, 'form': QuoteForm()})

