from django.contrib.auth.forms import UserCreationForm


from .models import user,movie_details,Review
from  django import forms


class XYZ_DateInput(forms.DateInput):
    input_type = "date"
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        # kwargs["format"] = "%d-%m-%Y"
        super().__init__(**kwargs)
class Video_form(forms.ModelForm):
    class Meta:
        model=movie_details
        fields = "__all__"
        widgets = {
            'my_date': XYZ_DateInput(format=["%Y-%m-%d"], )
        }
        #fields=("classname",'subjname',"title","video")

class Review_Form(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['subject','comment','rating']