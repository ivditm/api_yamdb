from django.contrib import admin


from .models import User, Category, Genre, Title


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role'
    )
    list_editable = (
        'role',
    )
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
