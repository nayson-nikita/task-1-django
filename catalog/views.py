import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Book, Author, BookInstance, Genre, Language
from .forms import RenewBookForm


def index(request):
    """View function for home page of site."""
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)
#
#
# class BookListView(generic.ListView):
#     model = Book
#     paginate_by = 5
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['some_data'] = 'This is just some data'
#         return context
#
#
# class BookDetailView(generic.DetailView):
#     model = Book
#
#
# class AuthorListView(generic.ListView):
#     model = Author
#     paginate_by = 5
#
#
# class AuthorDetailView(generic.DetailView):
#     model = Author
#
#
# class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
#     """Generic class-based view listing books on loan to current user."""
#     model = BookInstance
#     template_name = 'catalog/bookinstance_list_borrowed_user.html'
#     paginate_by = 10
#
#     def get_queryset(self):
#         return (
#             BookInstance.objects.filter(borrower=self.request.user)
#             .filter(status__exact='o')
#             .order_by('due_back')
#         )
#
#
# class AllBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
#     """Generic class-based view listing all books on loan. Only for librarians."""
#     model = BookInstance
#     permission_required = 'catalog.can_mark_returned'
#     template_name = 'catalog/bookinstance_list_borrowed_all.html'
#     paginate_by = 10
#
#     def get_queryset(self):
#         return BookInstance.objects.filter(status__exact='o').order_by('due_back')
#
#
# @login_required
# @permission_required('catalog.can_mark_returned', raise_exception=True)
# def renew_book_librarian(request, pk):
#     """View function for renewing a specific BookInstance by librarian."""
#     book_instance = get_object_or_404(BookInstance, pk=pk)
#
#     # If this is a POST request then process the Form data
#     if request.method == 'POST':
#
#         # Create a form instance and populate it with data from the request (binding):
#         form = RenewBookForm(request.POST)
#
#         # Check if the form is valid:
#         if form.is_valid():
#             book_instance.due_back = form.cleaned_data['renewal_date']
#             book_instance.save()
#
#             # redirect to a new URL:
#             return HttpResponseRedirect(reverse('borrowed'))
#
#     # If this is a GET (or any other method) create the default form.
#     else:
#         proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
#         form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
#
#     context = {
#         'form': form,
#         'book_instance': book_instance,
#     }
#
#     return render(request, 'catalog/book_renew_librarian.html', context)
#
#
# class AuthorCreate(PermissionRequiredMixin, CreateView):
#     model = Author
#     fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
#     initial = {'date_of_death': '11/06/2020'}
#     permission_required = 'catalog.add_author'
#
#
# class AuthorUpdate(PermissionRequiredMixin, UpdateView):
#     model = Author
#     fields = '__all__'
#     permission_required = 'catalog.change_author'
#
#
# class AuthorDelete(PermissionRequiredMixin, DeleteView):
#     model = Author
#     success_url = reverse_lazy('authors')
#     permission_required = 'catalog.delete_author'
#
#
# class BookCreate(PermissionRequiredMixin, CreateView):
#     model = Book
#     fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
#     permission_required = 'catalog.add_book'
#
#
# class BookUpdate(PermissionRequiredMixin, UpdateView):
#     model = Book
#     fields = '__all__'
#     permission_required = 'catalog.change_book'
#
#
# class BookDelete(PermissionRequiredMixin, DeleteView):
#     model = Book
#     success_url = reverse_lazy('books')
#     permission_required = 'catalog.delete_book'
#
# class BookInstanceCreate(PermissionRequiredMixin, CreateView):
#     model = BookInstance
#     fields = ['book', 'imprint', 'due_back', 'borrower', 'status']
#     permission_required = 'catalog.add_bookinstance'
#     success_url = reverse_lazy('books')
#
#
# class BookInstanceUpdate(PermissionRequiredMixin, UpdateView):
#     model = BookInstance
#     fields = ['book', 'imprint', 'due_back', 'borrower', 'status']
#     permission_required = 'catalog.change_bookinstance'
#     success_url = reverse_lazy('books')
#
#
# class BookInstanceDelete(PermissionRequiredMixin, DeleteView):
#     model = BookInstance
#     success_url = reverse_lazy('books')
#     permission_required = 'catalog.delete_bookinstance'
#
#
# class GenreListView(generic.ListView):
#     model = Genre
#     paginate_by = 10
#
#
# class LanguageListView(generic.ListView):
#     model = Language
#     paginate_by = 10
#
#
# class BookInstanceListView(PermissionRequiredMixin, generic.ListView):
#     """List of all book copies. Only for librarians."""
#     model = BookInstance
#     permission_required = 'catalog.can_mark_returned'
#     template_name = 'catalog/bookinstance_list_all.html'
#     paginate_by = 10
#
#
# class GenreCreate(PermissionRequiredMixin, CreateView):
#     model = Genre
#     fields = ['name']
#     permission_required = 'catalog.add_genre'
#     success_url = reverse_lazy('genres')
#
#
# class LanguageCreate(PermissionRequiredMixin, CreateView):
#     model = Language
#     fields = ['name']
#     permission_required = 'catalog.add_language'
#     success_url = reverse_lazy('languages')
