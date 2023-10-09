from django.db import models
from student.models import Student
import datetime
from django.utils import timezone

class Author(models.Model):
    name=models.CharField(max_length=350)
    description=models.CharField(max_length=450)
    def __str__(self):
        return self.name
    
class Book(models.Model):
    name=models.CharField(max_length=350)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    image=models.ImageField()
    category=models.CharField(max_length=220)

    def __str__(self):
        return self.name

    
class Issue(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    created_at=models.DateTimeField( auto_now=True)
    issued=models.BooleanField(default=False)
    issued_at=models.DateTimeField( auto_now=False,null=True,blank=True)
    returned=models.BooleanField(default=False)
    return_date=models.DateTimeField(auto_now=False,auto_created=False,auto_now_add=False,null=True,blank=True)

    def __str__(self):
        return "{}_{} book issue request".format(self.student,self.book)

    def days_no(self):
        if self.issued:
            y,m,d=str(timezone.now().date()).split('-')
            today=datetime.date(int(y),int(m),int(d))
            y2,m2,d2=str(self.return_date.date()).split('-')
            lastdate=datetime.date(int(y2),int(m2),int(d2))
            print(lastdate-today,lastdate>today)
            if lastdate > today:
                return "{} left".format(str(lastdate-today).split(',')[0])
            else:
                return "{} passed".format(str(today-lastdate).split(',')[0])
        else:
            return ""
    
class Fine(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    issue=models.ForeignKey(Issue,on_delete=models.CASCADE)
    amount=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    paid=models.BooleanField(default=False)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None) 
    datetime_of_payment = models.DateTimeField(auto_now=False,null=True,blank=True)
    
    
    def save(self, *args, **kwargs):
        if self.order_id is None:
            self.order_id = f"{self.student.student_id.username}_{timezone.now().strftime('%H%M%S')}"
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Issue {self.issue.id} fine -> {self.amount}"
    
    
    
class Wishlist(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.first_name}'s Wishlist: {self.book.name}"


class WishlistItem(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.first_name}'s Wishlist Item ({self.book.name})"
