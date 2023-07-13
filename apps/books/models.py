import datetime
import uuid

from PyPDF4 import PdfFileReader
from django.core.validators import RegexValidator, ValidationError
from django.db.models import Model, CharField, IntegerField, FileField, ForeignKey, CASCADE, ImageField

from books.tasks import convert_pdf_to_jpg

FILE_TYPES = {
    r'^(jpg|jpeg|png|JPG)$': 'images',
    r'^(pdf)$': 'documents',
    r'^(mp4)$': 'videos'
}


def upload_name(instance, filename):
    file_type = filename.split('.')[-1]
    date = datetime.datetime.now().strftime('%Y/%m/%d')

    for regex, folder in FILE_TYPES.items():
        try:
            RegexValidator(regex).__call__(file_type)
            instance.type = folder
            return '%s/%s/%s/%s.%s' % (folder, instance._meta.model_name, date, uuid.uuid4(), file_type)
        except ValidationError:
            pass
    raise ValidationError('File type is unacceptable')


class Category(Model):
    name = CharField(max_length=255)


class Author(Model):
    name = CharField(max_length=255)


class Book(Model):
    name = CharField(max_length=255)
    price = IntegerField(default=0)
    year_pub = IntegerField()
    author = ForeignKey(Author, CASCADE)
    pdf = FileField(upload_to=upload_name)
    # page_pdf = models.FileField(
    #     upload_to=upload_name, validators=[FileExtensionValidator(allowed_extensions=["pdf"])]
    # )
    page_count = IntegerField(default=0)
    category = ForeignKey(Category, CASCADE)
    image = ImageField(upload_to=upload_name, null=True, blank=True)

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     file = self.pdf.open()
    #     pdf = PdfFileReader(file)
    #     self.page_count = pdf.getNumPages()
    #     return super().save()

    # @property
    # def year_pub(self):
    #     return self.created_at.strftime('%Y')

    def set_page_book(self):
        import pdfplumber
        with pdfplumber.open(self.pdf.file) as pdf:
            self.page_count = len(pdf.pages)

    def get_image_url(self):
        from uuid import uuid4
        image_url = f"{upload_name(self, f'{uuid4()}.jpg')}"
        return image_url

    def get_pdf_url(self):
        return self.pdf.url

    def convert_pdf_to_image(self):
        pdf_url = self.get_pdf_url()
        image_url = self.get_image_url()
        img_name = image_url.split('/')[-1]
        img_url = "/".join(image_url.split('/')[0:-1]) + '/'
        convert_pdf_to_jpg.delay(pdf_url, img_url, img_name)
        return image_url

    def save(self, *args, **kwargs):
        self.set_page_book()
        if not self.image:
            super().save(*args, **kwargs)
            self.image = self.convert_pdf_to_image()
            return self.save()
        super().save(*args, **kwargs)


class ViewCount(Model):
    book = ForeignKey(Book, CASCADE)
    user = ForeignKey('users.User', CASCADE)
