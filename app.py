from flask import Flask, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_login import UserMixin
from flask_dance.contrib.google import make_google_blueprint, google
from flask import render_template
import requests
import keyring
import win32com.client

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd5a4fed0b42d05331d04d5ec09e6cb6d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://dbadmin:jogciw-miqvic-2pEkky@localhost/mydb'
db = SQLAlchemy(app)

CROWDFIBER_API_KEY = "https://shop.austinfiberoptics.com/embed/51.js"

# Configure user authentication and Flask-Dance
login_manager = LoginManager(app)
login_manager.login_view = "google.login"

google_blueprint = make_google_blueprint(
    client_id="your_client_id",
    client_secret="your_client_secret",
    scope=["profile", "email"],
)
app.register_blueprint(google_blueprint, url_prefix="/login")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class DataEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<DataEntry {self.name}>'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    profile_pic = db.Column(db.String(200), nullable=False)
    area = db.Column(db.String(100), nullable=False)

    comments = db.relationship('Comment', backref='author', lazy=True)
    tasks = db.relationship('Task', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/area_breakdown')
@login_required
def area_breakdown():
    return render_template('area_breakdown.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/api/data', methods=['POST'])
@login_required
def create_data():
    data = request.get_json()
    name = data.get("name")
    value = data.get("value")
    entry = DataEntry(name=name, value=value)
    db.session.add(entry)
    db.session.commit()
    return jsonify({"message": "Data entry created successfully"})

@app.route('/api/data', methods=['GET'])
@login_required
def get_data():
    entries = DataEntry.query.all()
    return jsonify({"data": [{"id": entry.id, "name": entry.name, "value": entry.value} for entry in entries]})

@app.route('/api/data/<int:data_id>', methods=['PUT'])
@login_required
def update_data(data_id):
    entry = DataEntry.query.get(data_id)
    if entry:
        data = request.get_json()
        entry.name = data.get("name")
        entry.value = data.get("value")
        db.session.commit()
        return jsonify({"message": "Data entry updated successfully"})
    else:
        return jsonify({"message": "Data entry not found"}), 404

@app.route('/api/data/<int:data_id>', methods=['DELETE'])
@login_required
def delete_data(data_id):
    entry = DataEntry.query.get(data_id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({"message": "Data entry deleted successfully"})
    else:
        return jsonify({"message": "Data entry not found"}), 404

@app.route('/api/orders', methods=['GET'])
@login_required
def get_orders():
    # Add your code to fetch order data from Stripe and CrowdFiber
    pass

def send_email_outlook(subject, body, recipients):
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    account = namespace.Folders.Item(1)  # Change this index to select a specific account if you have multiple accounts in Outlook
    sent_folder = account.Folders['Sent Items']

    message = outlook.CreateItem(0)
    message.Subject = subject
    message.Body = body
    message.To = ";".join(recipients)
    message.SaveSentMessageFolder = sent_folder
    message.Send()

@app.route('/api/orders/filter', methods=['POST'])
@login_required
def filter_orders():
    filters = request.json
    # Add your code to filter order data based on the provided filters
    pass

@app.route('/api/orders/search', methods=['GET'])
@login_required
def search_orders():
    search_query = request.args.get('query', '')
    # Add your code to search order data based on the provided search query
    pass

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Comment {self.id}>'

@app.route('/api/comments', methods=['POST'])
@login_required
def create_comment():
    content = request.form['content']
    comment = Comment(author_id=current_user.id, content=content)
    db.session.add(comment)
    db.session.commit()
    return jsonify({"message": "Comment added successfully"})

@app.route('/api/comments', methods=['GET'])
@login_required
def get_comments():
    comments = Comment.query.all()
    return jsonify({"comments": [comment.content for comment in comments]})

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<Task {self.title}>'

@app.route('/api/tasks', methods=['POST'])
@login_required
def create_task():
    title = request.form['title']
    description = request.form['description']
    task = Task(author_id=current_user.id, title=title, description=description)
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task added successfully"})

@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(author_id=current_user.id).all()
    return jsonify({"tasks": [{"id": task.id, "title": task.title, "description": task.description, "completed": task.completed} for task in tasks]})

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    task = Task.query.get(task_id)
    if task and task.author_id == current_user.id:
        task.completed = not task.completed
        db.session.commit()
        return jsonify({"message": "Task updated successfully"})
    else:
        return jsonify({"message": "Task not found"}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task and task.author_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"})
    else:
        return jsonify({"message": "Task not found"}), 404

def send_email_alert(subject, body):
    team_emails = ['team_member1@example.com', 'team_member2@example.com']
    send_email_outlook(subject, body, team_emails)

if __name__ == '__main__':
    app.run(debug=True)
