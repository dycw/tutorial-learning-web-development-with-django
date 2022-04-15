from django.forms import BooleanField
from django.forms import CharField
from django.forms import ChoiceField
from django.forms import DateField
from django.forms import DateInput
from django.forms import DecimalField
from django.forms import EmailField
from django.forms import FloatField
from django.forms import Form
from django.forms import HiddenInput
from django.forms import IntegerField
from django.forms import MultipleChoiceField
from django.forms import PasswordInput
from django.forms import RadioSelect
from django.forms import Textarea


RADIO_CHOICES = (
    ("Value One", "Value One Display"),
    ("Value Two", "Text For Value Two"),
    ("Value Three", "Value Three's Display Text"),
)

BOOK_CHOICES = (
    (
        "Non-Fiction",
        (
            ("1", "Deep Learning with Keras"),
            ("2", "Web Development with Django"),
        ),
    ),
    ("Fiction", (("3", "Brave New World"), ("4", "The Great Gatsby"))),
)


class ExampleForm(Form):
    text_input = CharField(max_length=3)
    password_input = CharField(min_length=8, widget=PasswordInput)
    checkbox_on = BooleanField()
    radio_input = ChoiceField(choices=RADIO_CHOICES, widget=RadioSelect)
    favorite_book = ChoiceField(choices=BOOK_CHOICES)
    books_you_own = MultipleChoiceField(required=False, choices=BOOK_CHOICES)
    text_area = CharField(widget=Textarea)
    integer_input = IntegerField(min_value=1, max_value=10)
    float_input = FloatField()
    decimal_input = DecimalField(max_digits=5, decimal_places=3)
    email_input = EmailField()
    date_input = DateField(widget=DateInput(attrs={"type": "date"}))
    hidden_input = CharField(widget=HiddenInput, initial="Hidden Value")
