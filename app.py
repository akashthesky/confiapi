from flask import Flask, jsonify, send_file
from azure.storage.blob import BlobServiceClient
import os
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


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


from flask import Flask, request, jsonify
from flask_mail import Mail, Message

# Email configuration (use your email server configuration)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 465  # Use appropriate port for your server
app.config['MAIL_USE_SSL'] = False
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
