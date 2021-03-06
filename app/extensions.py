from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from jaeger_client import Config

from app.util.user_display import plan_display, plan_type_display, user_display

db = SQLAlchemy()
login_manager = LoginManager()
tool_bar = DebugToolbarExtension()

tracer_config = Config(
    config={
        'sampler': {
            'type': 'const',
            'param': 1,
        },
        'local_agent': {
            'reporting_host': "jaeger_host",
        },
        'logging': True,
    },
    service_name='info_sub_web',
)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("view.login"))


# Jinja2 Global Template
def display_user(user):
    if user in user_display:
        return user_display[user]
    return user


def display_play(plan):
    if plan in plan_display:
        return plan_display[plan]
    return plan


def display_plan_type(plan_type):
    if plan_type in plan_type_display:
        return plan_type_display[plan_type]
    return plan_type
