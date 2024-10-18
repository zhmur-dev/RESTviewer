# RESTviewer

---

## Description

**RESTviewer** is a RESTful API service based on Django REST Framework that can be used for publishing and sharing user reviews for various titles (e.g. music album, videogame, science fiction novel, etc.). Titles, and also the categories and genres these can relate to, are set up by administrator.

Developed as pure API, **RESTviewer** is not shipped with any frontend interface apart from standard DRF view.

For introductory experience, it is recommended to install the service locally, import sample database and follow the OpenAPI specification that is made available at `http://127.0.0.1:8000/redoc/` upon launching the server.

---

## Sample process

- **Administrator** account is created
- **Administrator** fills the database with **Categories** and **Genres** to be selected from when adding new **Titles**
- **Administrator** adds **Titles** to be reviewed to the database
- **Users** register
- **Users** post **Reviews** to available **Titles**
- **Users** read other users **Reviews** and post their **Comments**

---

## Stack

* Python 3.9
* Django REST Framework 3.12
* PyJWT 2.1
* SQLite3

---

## Installation and local startup

- Clone RESTviewer from GitHub:

```bash
git clone git@github.com:zhmur-dev/RESTviewer.git
```

- cd into RESTviewer directory:

```bash
cd RESTviewer
```

- Create and activate virtual environment:

```bash
# MacOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
source venv/Scripts/activate
```

- Upgrade package manager and install requirements:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

- Apply migrations:

```bash
python3 restviewer/manage.py migrate
```

- Import sample database, if you like:

```commandline
python3 restviewer/manage.py import_sample_db
```


- Launch server locally

```bash
python3 restviewer/manage.py runserver
```

**RESTviewer** is up, and a detailed OpenAPI specification is avaiable at `http://127.0.0.1:8000/redoc/`.

You can try sending API requests via your favorite client like HTTPie or Postman, or use integrated Django REST Framework interface by simply proceeding to `http://127.0.0.1:8000/api/v1/`.

---

## Author
Alexander [zhmur-dev](https://github.com/zhmur-dev) Zhmurkov