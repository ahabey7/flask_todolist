from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Task {self.id} - {self.content}>'

# Home route
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# Add task route
@app.route('/add', methods=['POST'])
def add():
    content = request.form.get('content')
    new_task = Task(content=content)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

# Delete task route
@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

# Ensure the app context is properly set when creating the database
if __name__ == '__main__':
    with app.app_context():  # Ensure the app context is used here
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)
