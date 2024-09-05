from flask import Flask, render_template, request
import mysql.connector
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object('config.Config')

# MySQL Database connection
db = mysql.connector.connect(
    host="localhost",
    user="your_mysql_username",  # Replace with your MySQL username
    password="your_mysql_password",  # Replace with your MySQL password
    database="crm_db"  # Database name created in MySQL Workbench
)

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/complaint_form')
def complaint_form():
    return render_template('complaint_form.html')

@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    customer_name = request.form['name']
    email = request.form['email']
    complaint = request.form['complaint']
    scooter_id = request.form['scooter_id']

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO complaints (customer_name, email, complaint, scooter_id) VALUES (%s, %s, %s, %s)",
        (customer_name, email, complaint, scooter_id)
    )
    db.commit()

    cursor.execute("SELECT * FROM scooter_data WHERE id = %s", (scooter_id,))
    scooter_data = cursor.fetchone()

    msg = Message('Complaint Acknowledgment', sender='your_email@gmail.com', recipients=[email])
    msg.body = f"Dear {customer_name},\n\nWe have received your complaint regarding scooter ID {scooter_id}.\n\nThank you!"
    mail.send(msg)

    return render_template('display_complaint.html', name=customer_name, complaint=complaint, scooter_data=scooter_data)

if __name__ == '__main__':
    app.run(debug=True)