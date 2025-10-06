from django import forms
from .models import Event, User, Ticket, Review

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
            