import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

#простая модель для истории запросов
class query(models.Model):
    query_text = models.TextField(max_length=100, null=True, verbose_name='Текст запроса')
    add_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата запроса')
    def __str__(self):
        return self.query_text

