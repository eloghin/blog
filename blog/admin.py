from django.contrib import admin
from .models import Post, Comment, Profile

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'published_date','status')
    list_filter = ('status', 'created_date', 'published_date', 'author')
    search_fields = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',) #The widget to select related objects for the author field of the Post model
    date_hierarchy = 'published_date'
    ordering = ('status', 'published_date')


admin.site.register(Comment)
admin.site.register(Profile)
