# How to get the email address and the height entered by the user
# For that, need to import Flask, render_template and request
# render_template method is to render out HTML templates
# request is to be able to access these http:// request that is being made from the browser to fetch the email address and the height
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email


app = Flask(__name__)
# Creating an SQLAchemy object for flask application and then connecting the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/height_collector'
# Replace user with your username of pgAdmin, password with your pw or else web page will give error
# Now, the app knows where to look for a database
db = SQLAlchemy(app)    # Creating SQLAlchemy object to store SQLAlchemy and the name of the app


# Creating the object instances out of the blueprint.
# This DATA class will be a subclass of another class that is constructed by SQLAlchemy.
# So there's the blueprint that is designed to interact with the PostgreSQL database and it needs to be used which is already written in SQLAlchemy.
class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key = True)   # db.Integer is the data type of the ID column and that'd be primary key
    email_ = db.Column(db.String(120), unique = True)   # Don't want more than 120 characters and Do want the email unique
    height_ = db.Column(db.Integer)

    # initializing the instance variables of the object
    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_


@app.route("/")   # creating a decorator and mapping this / URL
def index():   # when the user visits the home page, index function will be executed
    return render_template("index.html")   # rendering this index.html


@app.route("/success", methods=['POST'])   # creating another decorator for the success page and mapping this /success URL
# By default, when these decorators are created, they implicitly declare a GET method.
# Need to declare POST method explicitly to be able to see the success page
def success():   # when this above URL is visited, success function will be executed
    # After the success function is executed (which means user puts email and height info and submits),
    # email and height are being passed to the server as a post method. But they need to be CAPTURED inside success method.
    if request.method == 'POST':
        email = request.form["email_name"]
        height = request.form["height_name"]   # Form element (email_name, height_name) is the same key in the index.html
        send_email(email, height)   # send_email is an Imported Function
        if db.session.query(Data).filter(Data.email_ ==  email).count() == 0:
        # The reason count = 0 is to make sure this email address is being used the first time
            data = Data(email, height)   # Creating an Object Instance of Data Class to keep record of the user email and height info
            db.session.add(data)
            db.session.commit()
            return render_template("success.html")
            # This request is being able to read the method of the request and stores that in this method object (line19)
            # When the index.html page is reloaded, that creates GET request (GET /)
            # When the data is entered by the user and submitted, that creates POST request (POST /success)
    return render_template("index.html", text = "This email address has been used already. Please try with another!")


if __name__ == '__main__':
    app.debug = True
    app.run(port = 1313)