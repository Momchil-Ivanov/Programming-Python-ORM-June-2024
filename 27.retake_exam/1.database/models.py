from django.utils import timezone
from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, RegexValidator

from main_app.managers import HouseManager

class House(models.Model):
    name = models.CharField(
        max_length=80,
        unique=True,
        validators=[MinLengthValidator(5)],
    )
    motto = models.TextField(null=True, blank=True)
    is_ruling = models.BooleanField(default=False)
    castle = models.CharField(max_length=80, null=True, blank=True)
    wins = models.PositiveSmallIntegerField(default=0)
    modified_at = models.DateTimeField(auto_now=True)

    objects = HouseManager()

class Dragon(models.Model):
    BREATH_CHOICES = [
        ('Fire', 'Fire'),
        ('Ice', 'Ice'),
        ('Lightning', 'Lightning'),
        ('Unknown', 'Unknown'),
    ]

    name = models.CharField(
        max_length=80,
        unique=True,
        validators=[MinLengthValidator(5)],
    )
    power = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=1.0,
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
    )
    breath = models.CharField(
        max_length=9,
        choices=BREATH_CHOICES,
        default='Unknown',
    )
    is_healthy = models.BooleanField(default=True)
    birth_date = models.DateField(default=timezone.now().date())
    wins = models.PositiveSmallIntegerField(default=0)
    modified_at = models.DateTimeField(auto_now=True)
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        related_name='dragons',
    )

class Quest(models.Model):
    name = models.CharField(
        max_length=80,
        unique=True,
        validators=[MinLengthValidator(5)],
    )
    code = models.CharField(
        max_length=4,
        unique=True,
        validators=[
            RegexValidator(regex=r'^[A-Za-z#]{4}$'),
            MinLengthValidator(4),
        ],
    )
    reward = models.FloatField(default=100.0)
    start_time = models.DateTimeField()
    modified_at = models.DateTimeField(auto_now=True)
    dragons = models.ManyToManyField(
        Dragon,
        related_name='quests',
    )
    host = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        related_name='quests',
    )
