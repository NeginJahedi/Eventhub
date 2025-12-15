from django import forms
from .models import Event, User, Ticket, Review
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

EventsUser = get_user_model()


class EventForm(forms.ModelForm):    
    class Meta:
        model = Event
        exclude = ('organizer','status')
        
        widgets = {
            'title' : forms.TextInput( attrs={
                "class" : "form-control",
                "placeholder" : "Event Title",
            }),
            'description' : forms.Textarea( attrs={
                "class" : "form-control",
                "rows" : 5,
                "placeholder" : "A brief description of the event..." 
            }),
            'category' : forms.Select( attrs={
                "class" : "form-select"
            }),
            
            'location' : forms.TextInput(attrs={
                "placeholder" : "Event Location",
                "class":"form-control"
            }),
            'date' : forms.DateInput( attrs={
                "class" : "form-control",
                "type" : "date"
            }),
            'time' : forms.TimeInput( attrs={
                "class" : "form-control",
                "type" : "time"    
            }),
            'image' : forms.ClearableFileInput(attrs={
                "class" : "form-control"    
            }),
            'price' : forms.NumberInput( attrs={
                "class" : "form-control",
                "placeholder" : "Price per ticket"
            }),
            'tickets_available' : forms.NumberInput( attrs={
                "class" : "form-control",
                "placeholder" : "Event Capacity"
            }),
            # 'status' : forms.Select( attrs ={
            #     "class" : "form-select",
            # })
            
        }


class EventsUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "Email",
            "autocomplete": "email"
        })
    )
    class Meta(UserCreationForm.Meta):
        model = EventsUser
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "placeholder": "Username",
            "autocomplete": "username"
        })

        self.fields["password1"].widget.attrs.update({
            "placeholder": "Password",
            "autocomplete": "new-password"
        })

        self.fields["password2"].widget.attrs.update({
            "placeholder": "Confirm password",
            "autocomplete": "new-password"
        })
        self.fields["email"].widget.attrs.update({
            "placeholder": "Email",
            "autocomplete": "email"
        })

        for field in self.fields.values():
            field.help_text = None
            field.label = ""
