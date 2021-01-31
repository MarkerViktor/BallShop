from django.contrib.auth.models import User
from django.db import models


class SportType(models.Model):
    """A type of sport the ball made for"""
    name = models.CharField(max_length=255, verbose_name='The name of sport')

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    """A maker of ball model"""
    name = models.CharField(max_length=255, verbose_name='The name of ball maker company')
    link = models.URLField(verbose_name='Link to the maker site')

    def __str__(self):
        return self.name


class Material(models.Model):
    """A type of material the ball made of"""
    name = models.CharField(max_length=255, verbose_name='The name of material')

    def __str__(self):
        return self.name


class Ball(models.Model):
    """A product of the shop"""
    name = models.CharField(max_length=255, verbose_name='The title of ball product')
    description = models.TextField()
    sport_type = models.ForeignKey(SportType, on_delete=models.DO_NOTHING, verbose_name='Sport ball made for')
    maker = models.ForeignKey(Manufacturer, on_delete=models.DO_NOTHING, verbose_name='Ball made by')
    material = models.ForeignKey(Material, on_delete=models.DO_NOTHING, verbose_name='Ball made of')
    image = models.ImageField(upload_to='products', verbose_name='Image of product')
    price = models.FloatField(verbose_name='The cost of one ball')

    @property
    def feedbacks_rate(self):
        """Calculating mean of ball rates"""
        feedbacks = Feedback.objects.filter(product=self)
        if len(feedbacks) == 0:
            return '-'
        rates_sum = 0
        for feedback in feedbacks:
            rates_sum += feedback.rate
        return round(rates_sum / len(feedbacks), 1)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    """Consumer review of ball"""
    product = models.ForeignKey(Ball, on_delete=models.CASCADE, verbose_name='Reviewed product')
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Feedback got by')
    review_text = models.TextField()
    rate = models.IntegerField(verbose_name='Rate to product got from feedback author')
    creation_datetime = models.DateTimeField()

    def __str__(self):
        return f'{self.creation_datetime} {self.product} {self.author}'


class Advertisement(models.Model):
    """Advertisement showing at shop's pages"""
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='advertisement')
    url = models.URLField()

    def __str__(self):
        return self.name

