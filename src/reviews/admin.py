from django.contrib.admin import ModelAdmin
from django.contrib.admin import site

from reviews.models import Book
from reviews.models import BookContributor
from reviews.models import Contributor
from reviews.models import Publisher
from reviews.models import Review


class BookAdmin(ModelAdmin):  # type: ignore
    date_hierarchy = "publication_date"
    list_display = ("title", "isbn")
    list_filter = ("publisher", "publication_date")


# def initialled_name(obj):
#     """ obj.first_names='Jerome David', obj.last_names='Salinger'
#         => 'Salinger, JD' """
#     initials = ''.join([name[0] for name in obj.first_names.split(' ')])
#     return "{}, {}".format(obj.last_names, initials)

# class ContributorAdmin(admin.ModelAdmin):
#     list_display = ('last_names', 'first_names')
#     list_filter = ('last_names',)
#     search_fields = ('last_names__startswith', 'first_names')


site.register(Publisher)
site.register(Contributor)
site.register(Book, BookAdmin)
site.register(BookContributor)
site.register(Review)
