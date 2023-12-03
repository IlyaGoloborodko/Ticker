import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

#простая модель для истории запросов
class query(models.Model):
    query_text = models.TextField(max_length=100, null=True)
    add_date = models.DateTimeField("date added", auto_now_add=True)
    def __str__(self):
        return self.query_text

