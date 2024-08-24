from django.contrib import admin
from .models import Client,Questionnaire,Question

# Registering the Client model with the admin site
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # Specifies the fields to display in the list view of the Client model in the admin interface
    list_display = ('name', 'email')
    
# Registering the Questionnaire model with the admin site
@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    # Specifies the fields to display in the list view of the Questionnaire model in the admin interface
    list_display = ('title', 'client', 'created_at')
    
# Registering the Question model with the admin site
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # Specifies the fields to display in the list view of the Question model in the admin interface
    list_display = ('text', 'questionnaire')
