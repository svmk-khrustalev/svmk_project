from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User,verbose_name='Студент', on_delete=models.CASCADE)
    qr = models.ImageField(upload_to='qr')
    text = models.TextField(max_length=10000)
    textqr = models.TextField(max_length=1000, default='qr')
    textot = models.TextField(max_length=1000, default='еще не ответили')
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(auto_now=True)
    YES = 'РЕШЕНО'
    NO = 'В ОЖИДАНИИ ОТВЕТА'
    YEAR_IN_SCHOOL_CHOICES = [
        (YES, 'РЕШЕНО'),
        (NO, 'В ОЖИДАНИИ ОТВЕТА'),
    ]
    year_in_school = models.CharField(
        max_length=200,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=NO,
    )
    def get_absolute_url(self):
        return reverse("account:Product_single", kwargs={'pk': self.pk})

    def __str__(self):
        return self.text