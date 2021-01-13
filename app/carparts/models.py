
from django.db import models
from django.dispatch import receiver
import os
from django.utils.text import slugify
from django.urls import reverse
from django.utils.safestring import mark_safe
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, SmartResize

PRODUCER = [
        ('AUD', 'Audi'),
        ('ACU', 'Acura'),
        ('BMW', 'Bmw'),
        ('MER', 'Mercedes-Benz'),
        ('BEN', 'Bentley'),
        ('FER', 'Ferrari'),
        ('MAS', 'Maserati'),
        ('LAM', 'Lamborghini'),
        ('POR', 'Porsche'),
        ('ROL', 'Rolls-Royce'),
        ('MCL', 'McLaren'),
        ('AST', 'Aston Martin'),
        ('BUG', 'Bugatti'),
        ('LAN', 'Land-Rover'),
        ('LOT', 'Lotus'),
    ]


class Product(models.Model):
    producer = models.CharField(max_length=3, choices=PRODUCER, null=True)
    name = models.CharField(max_length=120, verbose_name='Product name', unique=True)
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    part_number = models.CharField(max_length=64, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=120)

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('product', kwargs=kwargs)

    def save(self, *args, **kwargs):
        # if not self.id:
            # self.slug = slugify(self.name, allow_unicode=True)
        super(Product, self).save(*args, **kwargs)

    def images_with_product(self):
        return self.productimage_set.select_related('product').order_by('pk')

    def other_products_from_category(self):
        products = Product.objects.filter(producer=self.producer).exclude(pk=self.pk)[:5]

        return products

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to='parts_photos', verbose_name="Photos")
    use_as_main = models.BooleanField(null=True, blank=True)
    image_thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFill(279, 217)],
                                      format='JPEG',
                                      options={'quality': 60})

    image_thumbnail_mobil = ImageSpecField(source='image',
                                      processors=[ResizeToFill(102, 85)],
                                      format='JPEG',
                                      options={'quality': 100})



    def image_tag(self):
        if self.image:
            # return mark_safe('<img src="%s" style="width: 30px; height: 30px" />' % self.image.url)
            return self.image.url
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'

    def __str__(self):
        return self.image.url


@receiver(models.signals.post_delete, sender=ProductImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=ProductImage)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
     Deletes old file from filesystem
     when corresponding `MediaFile` object is updated
     with new file.
     """
    if not instance.pk:
        return False

    try:
        old_file = ProductImage.objects.get(pk=instance.pk).image
    except ProductImage.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class Logo(models.Model):
    logo_image = models.ImageField(null=True, upload_to='logo_images', verbose_name="Logo")

    def image_tag(self):
        if self.logo_image:
            # return mark_safe('<img src="%s" style="width: 30px; height: 30px" />' % self.image.url)
            return self.logo_image.url
        else:
            return 'No logo Found'

    image_tag.short_description = 'Logo'

    def __str__(self):
        return self.logo_image.url


class Bodykit(models.Model):
    for_producer = models.CharField(max_length=3, choices=PRODUCER, null=True, blank=True)
    image = models.ImageField(null=True, upload_to='bodykits_images', verbose_name="Bodykits")
    collection = models.CharField(max_length=16, null=True, blank=True)

    def image_tag(self):
        if self.image:
            # return mark_safe('<img src="%s" style="width: 30px; height: 30px" />' % self.image.url)
            return self.image.url
        else:
            return 'No Image Found'

    image_tag.short_description = 'Bodykit-image'

    def producer_name(self):
        return self.get_for_producer_display()

    def __str__(self):
        return self.image.url


class SubscribeModel(models.Model):
    email = models.EmailField(null=False, blank=True, max_length=50, unique=True)
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField( auto_now_add=True, null=False, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=False, blank=True)

    # class Meta:
    #     app_label = "appname"
    #     db_table = "appname_subscribe"

    def __str__(self):
        return self.email
