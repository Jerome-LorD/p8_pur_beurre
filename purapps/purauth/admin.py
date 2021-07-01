from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .models import User
from .forms import UserChangeForm, UserCreationForm

admin.site.register(User)  # , UserAdmin)
# Register your models here.


class UserAdmin(AuthUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    # list_display = ("")
