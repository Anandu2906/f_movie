from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(user)
admin.site.register(category)
#admin.site.register(movie_details)

@admin.register(movie_details)
class movieAdmin(admin.ModelAdmin):
    list_display = ['title', 'poster', 'description','rdate','actors', 'video', 'category','user']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['movie_details', 'comment','rating','created_at']
    readonly_fields = ['created_at']
    
    


