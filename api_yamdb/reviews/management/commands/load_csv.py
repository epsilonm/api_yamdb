import csv
import os

from django.core.management.base import BaseCommand

from reviews.models import Comment, Review, Category, Genre, Title
from users.models import User


def read_csv(name_file):
    path = os.path.join('static/data', name_file)
    data_list = []
    with open(path, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            data_list.append(row)
    return data_list


def load_users():
    data_list = read_csv('users.csv')
    users = [
        User(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            role=row['role']
        )
        for row in data_list
    ]
    User.objects.bulk_create(users)


def load_categories():
    data_list = read_csv('category.csv')
    categories = [
        Category(
            id=row['id'],
            name=row['name'],
            slug=row['slug']
        )
        for row in data_list
    ]
    Category.objects.bulk_create(categories)


def load_genres():
    data_list = read_csv('genre.csv')
    genres = [
        Genre(
            id=row['id'],
            name=row['name'],
            slug=row['slug']
        )
        for row in data_list
    ]
    Genre.objects.bulk_create(genres)


def load_titles():
    data_list = read_csv('titles.csv')
    titles = [
        Title(
            id=row['id'],
            name=row['name'],
            year=row['year'],
            category=Category.objects.get(id=row['category'])
        )
        for row in data_list
    ]
    Title.objects.bulk_create(titles)


def load_genre_title():
    data_list = read_csv('genre_title.csv')
    [
        Title.objects.get(id=row['title_id']).genre.add(row['genre_id'])
        for row in data_list
    ]


def load_review():
    data_list = read_csv('review.csv')
    reviews = [
        Review(
            id=row['id'],
            text=row['text'],
            author=User.objects.get(id=row['author']),
            title=Title.objects.get(id=row['title_id']),
            score=row['score'],
            pub_date=row['pub_date']
        )
        for row in data_list
    ]
    Review.objects.bulk_create(reviews)


def load_comments():
    data_list = read_csv('comments.csv')
    comments = [
        Comment(
            id=row['id'],
            text=row['text'],
            author=User.objects.get(id=row['author']),
            review=Review.objects.get(id=row['review_id']),
            pub_date=row['pub_date']
        )
        for row in data_list
    ]
    Comment.objects.bulk_create(comments)


class Command(BaseCommand):
    help = 'Импортирует таблицы из csv в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--all',
            action='store_true',
            help='Импортирует все таблицы из csv в базу данных'
        )

    def handle(self, *args, **options):
        if options['all']:
            try:
                load_users()
                load_categories()
                load_genres()
                load_titles()
                load_genre_title()
                load_review()
                load_comments()
                self.stdout.write(
                    self.style.SUCCESS('Таблицы загружены в БД'))
            except Exception as e:
                self.stdout.write(self.style.ERROR('Ошибка загрузки данных:'
                                                   ' "%s"' % e))
        else:
            self.stdout.write(
                self.style.SQL_KEYWORD('Команда используется с ключом -a,'
                                       ' или --all'))
