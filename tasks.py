from invoke import task


@task
def build(c):
    c.run("docker-compose build")


@task
def db(c):
    c.run("docker-compose up -d postgres")


@task
def down(c):
    c.run("docker-compose down")


@task
def seed(c):
    c.run("python manage.py create_example_data")


@task
def admin(c):
    c.run("python manage.py createsuperuser")


@task
def migrate(c):
    c.run("python manage.py migrate")


@task
def reset_db(c):
    c.run("python manage.py reset_db -c --noinput")


@task
def setup(c):
    reset_db(c)
    migrate(c)
    seed(c)
