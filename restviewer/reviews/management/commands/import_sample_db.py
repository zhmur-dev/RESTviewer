import csv

from django.core.management.base import BaseCommand

from reviews.models import (
    Category,
    Comment,
    CustomUser,
    Genre,
    Review,
    Title
)

from restviewer.settings import BASE_DIR


def import_users():
    try:
        with open(BASE_DIR / 'static/sample_db/users.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                CustomUser.objects.get_or_create(**row)
    except FileNotFoundError:
        raise ValueError('users.csv not found!')
    except Exception as error:
        print(error)


def import_categories():
    try:
        with open(BASE_DIR / 'static/sample_db/category.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Category.objects.get_or_create(**row)
    except FileNotFoundError:
        raise ValueError('category.csv not found!')
    except Exception as error:
        print(error)


def import_genres():
    try:
        with open(BASE_DIR / 'static/sample_db/genre.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Genre.objects.get_or_create(**row)
    except FileNotFoundError:
        raise ValueError('genre.csv not found!')
    except Exception as exception:
        print(exception)


def import_titles():
    try:
        with open(BASE_DIR / 'static/sample_db/titles.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Title.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(id=row['category'])
                )
    except FileNotFoundError:
        raise ValueError('titles.csv not found!')
    except Exception as exception:
        print(exception)


def import_title_genre_relations():
    try:
        with open(BASE_DIR / 'static/sample_db/genre_title.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Title.genre.through.objects.get_or_create(
                    title_id=row['title_id'],
                    genre=Genre.objects.get(id=row['genre_id'])
                )
    except FileNotFoundError:
        raise ValueError('genre_title.csv not found!')
    except Exception as exception:
        print(exception)


def import_reviews():
    try:
        with open(BASE_DIR / 'static/sample_db/review.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Review.objects.get_or_create(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author=CustomUser.objects.get(id=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date']
                )
    except FileNotFoundError:
        raise ValueError('review.csv not found!')
    except Exception as exception:
        print(exception)


def import_comments():
    try:
        with open(BASE_DIR / 'static/sample_db/comments.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Comment.objects.get_or_create(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author=CustomUser.objects.get(id=row['author']),
                    pub_date=row['pub_date']
                )
    except FileNotFoundError:
        raise ValueError('comments.csv not found!')
    except Exception as exception:
        print(exception)


class Command(BaseCommand):
    help = 'Imports sample database from CSV files'

    def handle(self, *args, **options):
        import_users()
        import_categories()
        import_genres()
        import_titles()
        import_title_genre_relations()
        import_reviews()
        import_comments()
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
