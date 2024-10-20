from flask import Flask, request, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)

# Email configuration (use your email server configuration)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 465  # Use appropriate port for your server
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'kshdey@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'whpj qqdh ixvx lhij'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = ('Akash Dey', 'kshdey@gmail.com')

mail = Mail(app)

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    if not data or not all(k in data for k in ("to", "subject", "body")):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        msg = Message(
            subject=data['subject'],
            recipients=[data['to']],  # List of recipients
            body=data['body']
        )
        
        mail.send(msg)
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
