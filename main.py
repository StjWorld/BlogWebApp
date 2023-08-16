from flask import Flask, render_template,request,flash, redirect, url_for,logging,session
from wtforms import Form, StringField, validators, PasswordField,TextAreaField
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'blog'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


class RegisterForm(Form):
    username = StringField("Username", validators=[validators.Length(min=4, max=25)])
    email = StringField('email', validators=[validators.Email(message='Not a valid email')])
    password = PasswordField('Password', validators=[
        validators.DataRequired(message='Please enter a password'),
        validators.EqualTo(fieldname='confirm', message='Password does not match'),
        validators.Length(min=4, max=25)
    ])
    confirm = PasswordField('Confirm Password')



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/articles")
def articles():
    return render_template("articles.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)

        cursor = mysql.connection.cursor()

        query = "insert into users(username,email,password) values(%s,%s,%s)"

        cursor.execute(query, (username, email, password))
        mysql.connection.commit()
        cursor.close()

        #### Data Leakage may occurr ####




        # flash("Thanks for register")
        return redirect(url_for("index"))
    else:
        return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)

