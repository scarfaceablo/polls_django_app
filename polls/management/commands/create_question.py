from django.core.management import BaseCommand
from polls.utils.question_generator import QuestionGenerator


class Command(BaseCommand):

    def handle(self, *args, **options):
        QuestionGenerator().generate_question()
