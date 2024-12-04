from .forms import LecteurForm, ChangeLecteurForm
# Create your views here.
from .models import Lecteur
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from books.models import Book

@login_required
def book_history(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    history = book.history.all().order_by('-date_borrowed')
    return render(request, 'client_library/book_history.html', {'book': book, 'history': history})
@login_required
def change_lecteur(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    if request.method == 'POST':
        form = ChangeLecteurForm(request.POST, instance=book, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('client_library:lecteur_list')  # No pk passed here
    else:
        form = ChangeLecteurForm(instance=book, user=request.user)
    return render(request, 'client_library/change_lecteur.html', {'form': form, 'book': book})

@login_required
def add_lecteur(request):
    if request.method == 'POST':
        form = LecteurForm(request.POST)
        if form.is_valid():
            lecteur = form.save(commit=False)
            try:
                client = request.user.client
                lecteur.client = client
                lecteur.save()
                return redirect('client_library:lecteur_list')
            except Client.DoesNotExist:
                return render(request, 'error.html', {'message': 'No client associated with this user.'})
    else:
        form = LecteurForm()
    return render(request, 'client_library/add_lecteur.html', {'form': form})


@login_required
def lecteur_list(request):
    try:
        client = request.user.client
        lecteurs = Lecteur.objects.filter(client=client)
    except Client.DoesNotExist:
        lecteurs = Lecteur.objects.none()
    return render(request, 'client_library/lecteur_list.html', {'lecteurs': lecteurs})