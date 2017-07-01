# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError

from app.services.user import get_user_by_username_or_email, validate_email, validate_username


class LoginForm(FlaskForm):
    username_or_email = StringField(u"用户名或注册邮箱", validators=[DataRequired(u"登录名不能为空")])
    password = PasswordField(u"密码", validators=[DataRequired(u"密码不能为空")])
    remember = BooleanField(u"记住我", default=False)

    def validate_password(self, field):
        user = get_user_by_username_or_email(self.username_or_email.data)
        if user and user.is_active and user.check_password(field.data):
            return
        raise ValidationError(u"用户名或密码错误")


class RegisterForm(FlaskForm):
    username = StringField(u"用户名", validators=[DataRequired(u"用户名不能为空")])
    email = StringField(u"邮箱", validators=[DataRequired(u"邮箱不能为空")])
    password = PasswordField(u"登录密码", validators=[DataRequired(u"登录密码不能为空")])
    re_password = PasswordField(u"重复密码")
    coupon = StringField(u"邀请码")

    def validate_username(self, field):
        if validate_username(field.data):
            return
        raise ValidationError(u"用户名不可用")

    def validate_email(self, field):
        if validate_email(field.data):
            return
        raise ValidationError(u"邮箱不可用")

    def validate_password(self, field):
        if len(field.data) < 6:
            raise ValidationError(u"密码过于简单")
        if field.data != self.re_password.data:
            raise ValidationError(u"两次密码输入不一致")

