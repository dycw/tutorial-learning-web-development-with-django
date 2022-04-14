from django.contrib.admin import AdminSite

from reviews.models import Book
from reviews.models import BookContributor
from reviews.models import Contributor
from reviews.models import Publisher
from reviews.models import Review


class BookrAdminSite(AdminSite):
    title_header = "Bookr Admin"
    site_header = "Bookr administration"
    index_title = "Bookr site admin"


site = BookrAdminSite(name="bookr")
site.register(Publisher)
site.register(Contributor)
site.register(Book)
site.register(BookContributor)
site.register(Review)
