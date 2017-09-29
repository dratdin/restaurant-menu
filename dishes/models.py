from django.utils import timezone
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse

class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Name')
    slug = models.SlugField(unique=True, verbose_name='Slug for category')

    def get_absolute_url(self):
        return reverse('dishes:list', kwargs={"category_slug": self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return 'Category %s' % self.name

def upload_location(instance, filename):
    return "dishes/%s" %(filename)

class Dish(models.Model):
    name = models.CharField(max_length=128, verbose_name='Name')
    description = models.TextField()
    image = models.ImageField(
        upload_to=upload_location,
        width_field='width_field',
        height_field='height_field',
        verbose_name='Image'
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    preparing_time = models.DurationField(default=timezone.timedelta(minutes=5))
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)
    for_vegan = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, verbose_name='Slug for dish')
    category = models.ForeignKey(Category)

    def save(self, *args, **kwargs):
        '''
        On save, update timestamps
        https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add
        '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Dish, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(Dish, self).delete(*args, **kwargs)
        storage.delete(path)

    def get_absolute_url(self):
        return reverse('dishes:detail', kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Dish'
        verbose_name_plural = 'Dishes'
