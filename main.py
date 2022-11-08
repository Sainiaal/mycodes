from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
from flask_bootstrap import Bootstrap

app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = 'shitty'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///codes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class CreatePostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    code = CKEditorField("Full Code", validators=[DataRequired()])
    submit = SubmitField("Submit")


class Codes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    code = db.Column(db.Text, nullable=False)


@app.route("/")
def home():
    codes = Codes.query.all()
    return render_template("index.html", codes=codes)


@app.route("/codes/<int:code_id>")
def show_code(code_id):
    requested_code = Codes.query.get(code_id)
    return render_template("codes.html", code=requested_code)


@app.route("/new", methods=["GET", "POST"])
def add_new():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_code = Codes(
            title=form.title.data,
            subtitle=form.subtitle.data,
            code=form.code.data
        )
        db.session.add(new_code)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
