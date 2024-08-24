from django.db import models
from django.contrib.auth.models import User

# Model representing a client, linked to a Django user account
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    # Method to return the client's name
    def getClientName(self):
        return self.name

# Model representing a questionnaire associated with a specific client
class Questionnaire(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='questionnaires')
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    # Method to return the title of the questionnaire
    def getQuestionnaireTitle(self):
        return self.title

# Model representing a question within a questionnaire
class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=200)
    option_1 = models.CharField(max_length=100)
    option_2 = models.CharField(max_length=100)
    option_3 = models.CharField(max_length=100, blank=True, null=True)
    option_4 = models.CharField(max_length=100, blank=True, null=True)
    option_5 = models.CharField(max_length=100, blank=True, null=True)
    answer = models.IntegerField(blank=True, null=True)  # Stores the correct answer as an integer (1-5)

    # Method to return the text of the question
    def getQuestionText(self):
        return self.text

# Model representing a client's response to a question in a questionnaire
class ClientResponse(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='responses')
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.IntegerField(blank=True, null=True)  # Stores the client's selected answer as an integer
    answered_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the answer was submitted
