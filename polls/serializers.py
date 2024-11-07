from rest_framework import serializers

from polls.models import Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'polls:question-detail', 'lookup_field': 'id'}  # Ensure correct view name and lookup
        }
