from django.shortcuts import render, redirect

from .forms import RegisterForm


def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='quoteapp:main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'users/signup.html', context={"form": form})

    return render(request, 'users/signup.html', context={"form": RegisterForm()})
