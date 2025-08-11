from django.contrib import admin
from .models import Product, Comment, Profile

admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Profile)