from flask_app.app.models import Environment, User
from flask_app.app.schemas import EnvironmentSchema


def get_environment(request_data):
    user_id = request_data.get('user_id')
    env_name = request_data.get('env_name')

    environment = Environment.query.join(
        User.environments
    ).filter(
        User.user_id == user_id,
        Environment.env_name == env_name
    ).first()

    return EnvironmentSchema(exclude=('id',)).dump(environment).data
