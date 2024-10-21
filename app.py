from flask import Flask, jsonify, send_file
from azure.storage.blob import BlobServiceClient
import os
from io import BytesIO
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


app = Flask(__name__)
CORS(app)  # Handle CORS

# Configure your Gmail credentials
GMAIL_USER = 'kshdey@gmail.com'
GMAIL_PASSWORD = 'whpj qqdh ixvx lhij'  # Use an app-specific password

@app.route('/send-email', methods=['GET'])
def send_email():
    try:
        # Get request data
        data = request.json
        recipient_email = data['to']
        subject = data['subject']
        message_body = data['message']

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach message body
        msg.attach(MIMEText(message_body, 'plain'))

        # Send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure connection
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(GMAIL_USER, recipient_email, text)
        server.quit()

        return jsonify({"status": "success", "message": "Email sent successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Replace with your Azure Blob Storage connection string and container name
AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=confistoragenew;AccountKey=CUVYY9IqDR22sF2gCiT95AyACpah67ZYByX2Je9tXfjYZ9JlUalcNtOOdCxlY7SKLlQGf0Y8bs3w+AStSsTOBA==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "conficontainer"

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

@app.route('/files', methods=['GET'])
def list_files():
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    blobs = container_client.list_blobs()

    # Organize PDF and CSV files into pairs
    file_pairs = []
    pdf_files = {}
    
    for blob in blobs:
        
        if blob.name.endswith(".pdf"):
            file_key = blob.name[:-4]  # Remove ".pdf" extension to form key
            pdf_files[file_key] = blob.name
            print(pdf_files)
            file_pairs.append({
                    "pdf": pdf_files[file_key],
                    "csv": blob.name[:-4]+".csv"
                })
    print(file_pairs)
    return jsonify(file_pairs)

@app.route('/download/<file_type>/<file_name>', methods=['GET'])
def download_file(file_type, file_name):
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    blob_client = container_client.get_blob_client(file_name)

    # Download the blob to memory
    blob_data = blob_client.download_blob().readall()

    # Serve the file
    file_extension = ".pdf" if file_type == "pdf" else ".csv"
    return send_file(BytesIO(blob_data), as_attachment=True, download_name=file_name + file_extension)










if __name__ == '__main__':
    app.run(debug=True)
