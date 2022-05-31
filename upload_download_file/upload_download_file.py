# How to Upload/Download Files From the Web App

# render_template method is to render out HTML templates
# request is to be able to access these http:// request that is being made from the browser to fetch the email address and the height
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename


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
    global file
    if request.method == 'POST':
        file = request.files["file"]   # "file" should be the same with the name="file" in the index.html
        # content = file.read()        -- to read the file
        file.save(secure_filename("uploaded"+file.filename))   # Writing the file; need to save the file in to directory first!
        # User is able to upload a file to the directory, that's why it's important to use a secure way to upload the file.
        # secure_filename is basically secures the file name of the file that is entered by user (that user may be a hacker!!)
        with open("uploaded"+file.filename, "a") as f:
            f.write("This was added later!")
            # if csv file is not empty, "w" will delete whatever is written before and only will write "This was added later!"
            # "a" will append, means keeps the previous info and adds "This was added later!" at the end
        return render_template("index.html", btn="download.html")
            # Instead of success page, rendering a DOWNLOAD button in the index page


@app.route("/download")
def download():
    return send_file("uploaded"+file.filename, attachment_filename="yourfile.csv", as_attachment=True)
    # send_file is a method in flask that sends the contents of a file to the client.


if __name__ == '__main__':
    app.debug = True
    app.run(port = 1313)