from django.contrib import admin

from .models import Comment, Review, User


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'score', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date', 'author', 'title')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date', 'author', 'review')
    empty_value_display = '-пусто-'


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)
