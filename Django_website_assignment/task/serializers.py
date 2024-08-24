from rest_framework import serializers
from .models import Client, Questionnaire, Question

# Serializer for the Question model
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'  # Serializes all fields of the Question model

# Serializer for the Questionnaire model
class QuestionnaireSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)  # Embeds the related questions in the serialized data

    class Meta:
        model = Questionnaire
        fields = '__all__'  # Serializes all fields of the Questionnaire model

# Serializer for the Client model
class ClientSerializer(serializers.ModelSerializer):
    questionnaires = QuestionnaireSerializer(many=True, read_only=True)  # Embeds the related questionnaires in the serialized data

    class Meta:
        model = Client
        fields = '__all__'  # Serializes all fields of the Client model
