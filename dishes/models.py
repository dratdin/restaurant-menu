from django.urls import reverse
from django.db import models
from django.utils import timezone

from app.models import TimeStampMixin


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name="Name")
    slug = models.SlugField(unique=True, verbose_name="Slug for category")

    def get_absolute_url(self):
        return reverse("dishes:list", kwargs={"category_slug": self.slug})

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return "Category %s" % self.name


def upload_location(instance, filename):
    return "dishes/%s" % (filename)


class Dish(TimeStampMixin):
    name = models.CharField(max_length=128, verbose_name="Name")
    description = models.TextField()
    image = models.ImageField(
        upload_to=upload_location,
        width_field="width_field",
        height_field="height_field",
        verbose_name="Image",
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    preparing_time = models.DurationField(default=timezone.timedelta(minutes=5))
    for_vegan = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, verbose_name="Slug for dish")
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse("dishes:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Dish"
        verbose_name_plural = "Dishes"
        ordering = ["-created_at"]
