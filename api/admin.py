from django.contrib import admin
from .models import Review, User


class ReviewAdmin(admin.ModelAdmin):
    """
        ТЕСТОВАЯ МОДЕЛЬ
        Заменить на боевую
    """
    list_display = ['pk', 'text', 'author']


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Review, ReviewAdmin)
admin.site.register(User, UserAdmin)
