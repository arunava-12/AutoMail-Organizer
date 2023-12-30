from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'  # Using SQLite for simplicity
db = SQLAlchemy(app)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))

class AutoMailOrganizer:
    def __init__(self):
        self.emails = []

    def categorize_email(self, email):
        # Basic logic for categorization
        if "work" in email.subject.lower() or "meeting" in email.subject.lower():
            email.category = "Work"
        elif "personal" in email.subject.lower():
            email.category = "Personal"
        else:
            email.category = "Other"

    def process_emails(self):
        for email in self.emails:
            self.categorize_email(email)
            db.session.add(email)
        db.session.commit()

auto_mail_organizer = AutoMailOrganizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_emails', methods=['POST'])
def process_emails():
    data = request.get_json()
    email_subject = data['subject']
    email_content = data['content']

    new_email = Email(subject=email_subject, content=email_content)
    auto_mail_organizer.emails.append(new_email)

    auto_mail_organizer.process_emails()

    # Convert emails to a dictionary for JSON response
    result_emails = [{'subject': email.subject, 'category': email.category} for email in auto_mail_organizer.emails]

    return jsonify({'emails': result_emails})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    