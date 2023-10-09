from django.contrib import admin
from .models import Student
from library.admin import FineInline, IssueInline
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)
admin.site.unregister(Group)


class StudentInline(admin.TabularInline):
    model = Student

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'student', 'last_login')
    list_filter = ('is_superuser', 'is_active')
    fieldsets = (
        ('Standard info', {
            'fields': ('username', 'password',)
        }),
        ('Important Date & Time ', {
            'fields': ('last_login', 'date_joined',)
        }),
    )
    inlines = [
        StudentInline
    ]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ['student_id__username', 'first_name']
    fields = (('first_name', 'last_name'), ('student_id',))
    list_display = ('first_name', 'last_name', 'student_id')
    list_display_links = ('first_name', 'student_id')
    list_per_page = 30
    inlines = [
        IssueInline, FineInline
    ]

