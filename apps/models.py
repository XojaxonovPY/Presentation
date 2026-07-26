from ckeditor.fields import RichTextField
from django.db.models import Model, CharField, ImageField, ForeignKey, CASCADE, TextField


class Sprint(Model):
    name = CharField(max_length=125)

    def __str__(self):
        return self.name


class Product(Model):
    title = CharField(max_length=125)
    image = ImageField(upload_to='products/')

    def __str__(self):
        return self.title


class Feature(Model):
    title = CharField(max_length=125)
    description = TextField()
    product = ForeignKey('apps.Product', related_name='features', on_delete=CASCADE, db_index=True)
    sprint = ForeignKey('apps.Sprint', related_name='features', on_delete=CASCADE, db_index=True)

    def __str__(self):
        return self.title


class FeatureFile(Model):
    image = ImageField(upload_to='features/')
    feature = ForeignKey('apps.Feature', related_name='features_files', on_delete=CASCADE, db_index=True)
    image_id = TextField(null=True)

    def __str__(self):
        return self.feature.title
