from django.urls import path, re_path
from . import views
from .views import (
    AllBooksListView,
    SearchView,
    AddBookView,
    deletebook,
    issuerequest,
    SortView,
    myissues,
    myfines,
    requestedissues,
    allfines,
    issue_book,
    return_book,
    deletefine
)

urlpatterns = [
    path('', AllBooksListView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('sort/', SortView.as_view(), name='sort'),
    path('addbook/', AddBookView.as_view(), name='addbook'),
    path('deletebook/<int:bookID>/',deletebook),
    path('my-issues/',myissues),
    path('my-fines/',myfines),
    path('request-book-issue/<int:bookID>/',issuerequest),
    path('all-fines/',allfines),
    path('issuebook/<int:issueID>/',issue_book),
    path('returnbook/<int:issueID>/',return_book),
    path('delete-fine/<int:fineID>/',deletefine),
    path('my-issues/',myissues),
    path('all-issues/',requestedissues),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.view_wishlist, name='wishlist'),
]

