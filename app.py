from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #postavljanje baze
db = SQLAlchemy(app) #inicijalizacija baze

#kreiranje tabele u bazi

class Book(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    published = db.Column(db.DateTime, default=datetime.utcnow)

    #definisanje sta zelimo da bude prikaz knjige (id)
    def __repr__(self):
        return '<Book %r>' % self.id
    
#with app.app_context():
 #   db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        book_title = request.form['title']
        book_author = request.form['author']
        book_published = datetime. strptime(request.form['published'], '%Y-%m-%d')
        new_book = Book(title=book_title, author=book_author, published=book_published)
        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"
    else:
        books = Book.query.order_by(Book.title).all()
        return render_template('index.html', books=books)

@app.route('/delete/<int:id>')
def delete(id):
    book_to_delete = Book.query.get_or_404(id)
    try:
        #SQLAlchemy query API
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that book'
    

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    book_to_update = Book.query.get_or_404(id)
    if request.method == 'POST':
        book_to_update.title = request.form['title']
        book_to_update.author = request.form['author']
        book_to_update.published = datetime. strptime(request.form['published'], '%Y-%m-%d')
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your book'
    else:
        return render_template('update.html', book=book_to_update)

if __name__ == '__main__':
    app.run(debug=True)