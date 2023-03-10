import os

database_filename = "database.db"
backend_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(backend_dir, "database", database_filename)
# print(db_path)

db_uri = f'sqlite:///{db_path}'


class DevConfig:
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEVELOPMENT = True
    DEBUG = True


# These parameters are not hidden in an env file
# so that a reviewer can verify the project
class AuthConfig:
    AUTH0_DOMAIN = ''
    ALGORITHMS = ['RS256']
    API_AUDIENCE = ''
