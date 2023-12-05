from django.contrib import admin
from .models import query

# Register your models here.


@admin.register(query)
class history(admin.ModelAdmin):
    list_display = ('query_text','add_date')


