from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/jaquar'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lhrxxkiccognqo:5c1ccad8a0351d32ae3099ad2bd6d8c02c4d3182cdba009b5b550880182e48fa@ec2-34-227-120-94.compute-1.amazonaws.com:5432/d2mtevvo9igha7'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(250), unique=True)
    dealer = db.Column(db.String(250))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
    rating = request.form['rating']
    comments = request.form['comments']
    # print(customer, dealer, rating, comments)
    if customer == '' or dealer == '':
        return render_template('index.html', message='Please enter required fields')
    if db.session.query(Review).filter(Review.customer == customer).count() == 0:
        data = Review(customer, dealer, rating, comments)
        db.session.add(data)
        db.session.commit()
        send_mail(customer, dealer, rating, comments)
        return render_template('success.html')
    return render_template('index.html', message='You have already submitted review')


if __name__ == '__main__':
    app.run(debug=True)
