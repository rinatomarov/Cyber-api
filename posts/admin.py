from django.contrib import admin
from .models import Category, Post

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id","name" ,"alias"]

class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "author", "category",  "created_date"]
    # list_display = ["id", "title", "description" , "text","author", "category", "image", "video", "created_date"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post,PostAdmin)