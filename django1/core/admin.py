from django.contrib import admin
from .models import Applicationuser,Job,Payment,Comment
# Register your models here.

admin.site.register(Applicationuser)
admin.site.register(Job)
admin.site.register(Payment)
admin.site.register(Comment)