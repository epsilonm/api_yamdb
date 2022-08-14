import csv
import os

from django.core.management.base import BaseCommand
from users.models import User


def read_csv(name_file):
    path = os.path.join('static/data', name_file)
    data_list = []
    with open(path, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            data_list.append(row)
    return data_list


class Command(BaseCommand):
    help = 'Импортирует пользователей из csv в базу данных'

    def handle(self, *args, **options):
        data_list = read_csv('users.csv')
        users = [
            User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
            )
            for row in data_list
        ]
        User.objects.bulk_create(users)

        self.stdout.write('Пользователи загружены в БД')
