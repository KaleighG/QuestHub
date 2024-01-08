from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your models here.
class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({"class":"form-control"})