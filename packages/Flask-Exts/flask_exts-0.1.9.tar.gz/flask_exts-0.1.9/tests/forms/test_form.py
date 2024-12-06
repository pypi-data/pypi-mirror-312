import pytest
from flask import g
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_exts.forms.form import BaseForm
from flask_exts.forms.form import FlaskForm
from flask_exts.forms.form.secure_form import SecureForm



class BasicForm(BaseForm):
    name = StringField(validators=[DataRequired()])


class SafeForm(SecureForm):
    name = StringField(validators=[DataRequired()])


class FlaskBabelCsrfForm(FlaskForm):
    name = StringField(validators=[DataRequired()])


class TestForm:
    def test_base_form(self):
        form = BasicForm()
        assert "name" in form
        assert "csrf_token" not in form
        form.process(name="test")
        assert form.name.data == "test"
        assert form.validate()

    def test_safe_form(self, app):
        with app.test_request_context():
            form = SafeForm()
            assert "name" in form
            # print(form._fields)
            assert "csrf_token" in form

    def test_flask_form(self, app):
        with app.test_request_context():
            form = FlaskBabelCsrfForm()
            assert "name" in form
            assert "csrf_token" not in form
            data = {"name": "test"}
            form.process(data=data)
            assert form.name.data == "test"
            assert form.validate()

    def test_flask_form_csrf(self, app):
        app.config.update(CSRF_ENABLED=True)
        with app.test_request_context():
            form = FlaskBabelCsrfForm()
            assert "name" in form
            # print(form._fields)
            assert "csrf_token" in form
            data = {"name": "test", "csrf_token": g.get("csrf_token")}
            form.process(data=data)
            assert form.name.data == "test"
            assert form.validate()
