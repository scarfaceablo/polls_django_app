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

    def update(self, instance, validated_data):
        choices_data = validated_data.pop('choices')

        instance = super().update(instance, validated_data)

        instance.choices.all().delete()

        # update or create choices, remove choices that were not included in the update request
        choice_ids = []

        for choice_data in choices_data:
            choice_id = choice_data.get('id')
            choice_text = choice_data.get('choice_text')

            if choice_id:
                try:
                    choice = Choice.objects.get(pk=choice_id)
                    choice.choice_text = choice_text
                    choice.save()
                    choice_ids.append(choice_id)
                except Choice.DoesNotExist:
                    raise serializers.ValidationError(f"Choice with id {choice_id} does not exist.")
            else:
                choice = Choice.objects.create(question=instance, choice_text=choice_text)
                choice_ids.append(choice.id)

        # Remove choices that were not included in the update request
        instance.choices.exclude(id__in=choice_ids).delete()

        return instance

    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        question = Question.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(question=question, choice_text=choice_data.get('choice_text'))
        return question
