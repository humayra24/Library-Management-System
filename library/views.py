from django.shortcuts import render,redirect
from .models import Book,Author,Issue,Fine, Wishlist, WishlistItem
from student.models import Student
# from student.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
import datetime
from django.utils import timezone
import datetime
from .utilities import calcFine,getmybooks
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import auth
from django.conf import settings
from django.views.generic import ListView, DeleteView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import BookForm
from django.urls import reverse_lazy
from .forms import WishlistForm
from django.contrib import messages


class AllBooksListView(ListView):
    model = Book
    template_name = 'library/home.html'
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        requestedbooks, issuedbooks = getmybooks(self.request.user)
        context['issuedbooks'] = issuedbooks
        context['requestedbooks'] = requestedbooks
        return context



class SortView(View):
    template_name = 'library/home.html'

    def get(self, request, *args, **kwargs):
        sort_type = request.GET.get('sort_type')
        sort_by = request.GET.get('sort')
        requested_books, issued_books = getmybooks(request.user)

        context = {
            'issuedbooks': issued_books,
            'requestedbooks': requested_books,
            'selected': 'author' if 'author' in sort_type else 'book',
        }

        if 'author' in sort_type:
            author_results = Author.objects.filter(name__startswith=sort_by)
            context['author_results'] = author_results
        else:
            books_results = Book.objects.filter(name__startswith=sort_by)
            context['books_results'] = books_results

        return render(request, self.template_name, context)



class SearchView(View):
    template_name = 'library/home.html'

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search-query')
        search_by_author = request.GET.get('author')
        requestedbooks, issuedbooks = getmybooks(request.user)

        if search_by_author is not None:
            author_results = Author.objects.filter(name__icontains=search_query)
            return render(request, self.template_name, {
                'author_results': author_results,
                'issuedbooks': issuedbooks,
                'requestedbooks': requestedbooks,
            })
        else:
            books_results = Book.objects.filter(Q(name__icontains=search_query) | Q(category__icontains=search_query))
            return render(request, self.template_name, {
                'books_results': books_results,
                'issuedbooks': issuedbooks,
                'requestedbooks': requestedbooks,
            })


class AddBookView(View):
    template_name = 'library/addbook.html'

    def get(self, request):
        authors = Author.objects.all()
        form = BookForm()
        return render(request, self.template_name, {'authors': authors, 'form': form})

    def post(self, request):
        authors = Author.objects.all()
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            author_id = form.cleaned_data['author']
            author = Author.objects.get(id=author_id)
            image = form.cleaned_data['image']
            newbook, created = Book.objects.get_or_create(
                name=name, image=image, category=category, author=author
            )
            messages.success(request, 'Book - {} Added successfully'.format(newbook.name))
            return redirect('add-book')
        else:
            messages.error(request, 'Invalid form data. Please check the input.')
        
        return render(request, self.template_name, {'authors': authors, 'form': form})


@login_required(login_url='/student/login/')
@user_passes_test(lambda u: u.is_superuser,login_url='/student/login/')
def deletebook(request,bookID):
    book=Book.objects.get(id=bookID)
    messages.success(request,'Book - {} Deleted succesfully '.format(book.name))
    book.delete()
    return redirect('/')




@login_required(login_url='/student/login/')
@user_passes_test(lambda u: not u.is_superuser,login_url='/student/login/')
def issuerequest(request,bookID):
    student=Student.objects.filter(student_id=request.user)
    # student=CustomUser.objects.filter(student_id=request.user)
    
    if student:
        book=Book.objects.get(id=bookID)
        issue,created=Issue.objects.get_or_create(book=book,student=student[0])
        messages.success(request,'Book - {} Requested succesfully '.format(book.name))
        return redirect('home')
    
    messages.error(request,'You are Not a Student !')
    return redirect('/')


@login_required(login_url='/student/login/')
@user_passes_test(lambda u: not u.is_superuser ,login_url='/student/login/')
def myissues(request):
    if Student.objects.filter(student_id=request.user):
    # if CustomUser.objects.filter(student_id=request.user):
        student=Student.objects.filter(student_id=request.user)[0]
        # student=CustomUser.objects.filter(student_id=request.user)[0]
        
        if request.GET.get('issued') is not None:
            issues=Issue.objects.filter(student=student,issued=True)
        elif request.GET.get('notissued') is not None:
            issues=Issue.objects.filter(student=student,issued=False)
        else:
            issues=Issue.objects.filter(student=student)

        return render(request,'library/myissues.html',{'issues':issues})
    
    messages.error(request,'You are Not a Student !')
    return redirect('/')



@login_required(login_url='/admin/')
@user_passes_test(lambda u:  u.is_superuser ,login_url='/admin/')
def requestedissues(request):
    if request.GET.get('studentID') is not None and request.GET.get('studentID') != '':
        try:
            user= User.objects.get(username=request.GET.get('studentID'))
            student=Student.objects.filter(student_id=user)
            # student=CustomUser.objects.filter(student_id=user)
            if student:
                student=student[0]
                issues=Issue.objects.filter(student=student,issued=False)
                return render(request,'library/allissues.html',{'issues':issues})
            messages.error(request,'No Student found')
            return redirect('/all-issues/') 
        except User.DoesNotExist:
            messages.error(request,'No Student found')
            return redirect('/all-issues/')

    else:
        issues=Issue.objects.filter(issued=False)
        return render(request,'library/allissues.html',{'issues':issues})



@login_required(login_url='/admin/')
@user_passes_test(lambda u:  u.is_superuser ,login_url='/student/login/')
def issue_book(request,issueID):
    issue=Issue.objects.get(id=issueID)
    issue.return_date=timezone.now() + datetime.timedelta(days=15)
    issue.issued_at=timezone.now()
    issue.issued=True
    issue.save()
    return redirect('/all-issues/')



@login_required(login_url='/student/login/')
@user_passes_test(lambda u:  u.is_superuser ,login_url='/admin/')
def return_book(request,issueID):
    issue=Issue.objects.get(id=issueID)
    calcFine(issue)
    issue.returned=True
    issue.save()
    return redirect('/all-issues/')


@login_required(login_url='/student/login/')
@user_passes_test(lambda u: not u.is_superuser ,login_url='/student/login/')
def myfines(request):
    if Student.objects.filter(student_id=request.user):
        student=Student.objects.filter(student_id=request.user)[0]
        issues=Issue.objects.filter(student=student)
        for issue in issues:
            calcFine(issue)
        fines=Fine.objects.filter(student=student)
        return render(request,'library/myfines.html',{'fines':fines})
    messages.error(request,'You are Not a Student !')
    return redirect('/')


@login_required(login_url='/student/login/')
@user_passes_test(lambda u:  u.is_superuser ,login_url='/admin/')
def allfines(request):
    issues=Issue.objects.all()
    for issue in issues:
        calcFine(issue)
    return redirect('/admin/library/fine/')




@login_required(login_url='/student/login/')
@user_passes_test(lambda u:  u.is_superuser ,login_url='/admin/')
def deletefine(request,fineID):
    fine=Fine.objects.get(id=fineID)
    fine.delete()
    return redirect('/all-fines/')


@login_required(login_url='/student/login/')
@user_passes_test(lambda u: not u.is_superuser, login_url='/student/login/')
def add_to_wishlist(request):
    if request.method == 'POST':
        form = WishlistForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data['book']
            student = request.user.student
            
            #Check if the book is already in the wishlist
            if WishlistItem.objects.filter(student=student, book=book).exists():
                messages.error(request, f"{book.name} is already in your wishlist.")
            else:
                # Create a new wishlist item
                wishlist_item = WishlistItem(student=student, book=book)
                wishlist_item.save()
                messages.success(request, f"{book.name} has been added to your wishlist.")
                
            return redirect('wishlist')
    else:
        form = WishlistForm()
    
    return render(request, 'library/add_to_wishlist.html', {'form': form})


@login_required(login_url='/student/login/')
@user_passes_test(lambda u: not u.is_superuser, login_url='/student/login/')
def view_wishlist(request):
    student = request.user.student
    wishlist_items = WishlistItem.objects.filter(student=student)
    
    return render(request, 'library/view_wishlist.html', {'wishlist_items': wishlist_items})
