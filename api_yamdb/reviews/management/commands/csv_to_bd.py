import csv
import os

from django.core.management.base import BaseCommand
from reviews.models import Comment, Review, Category, Genre, Title, GenreTitle
from users.models import User

DATA_DICT = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv'
}


def read_csv(name_file):
    path = os.path.join('static/data', name_file)
    data_list = []
    with open(path, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            data_list.append(row)
    return data_list


def write_in_bd(data_dict):
    for key, value in data_dict.items():
        data_list = read_csv(name_file=value)
        for i in data_list:
            key.objects.create(**i)

# [field.name for field in Title._meta.get_fields()]


class Command(BaseCommand):
    help = 'Импортирует данные из csv в базу данных'

    def handle(self, *args, **options):
        # write_in_bd(data_dict=data)
        for model, name_file in DATA_DICT.items():
            path = os.path.join('static/data', name_file)
            with open(path, encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in reader)

        self.stdout.write('Данные загружены в БД')
