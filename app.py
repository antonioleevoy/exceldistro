from flask import Flask, request, send_file, render_template, jsonify
import pandas as pd
import os
from zipfile import ZipFile
import io
import threading
import time

app = Flask(__name__)
progress = 0

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def handle_file_upload():
    global progress
    try:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'})

        # Reset progress
        progress = 0

        # Read the specified sheet from the uploaded Excel file into a DataFrame
        df = pd.read_excel(file, sheet_name='REACHRoHs')

        # Select columns B to J (assuming 0-indexed, columns 1 to 9)
        df = df.iloc[:, 1:10]

        # Split the DataFrame by 'Client' column and save CSVs to an in-memory ZIP file
        clients = df['Client'].unique()
        zip_buffer = io.BytesIO()

        with ZipFile(zip_buffer, 'a') as zip_file:
            for i, client in enumerate(clients):
                client_df = df[df['Client'] == client]
                csv_buffer = io.StringIO()
                client_df.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)
                zip_file.writestr(f'{client}.csv', csv_buffer.getvalue())
                progress = int(((i + 1) / len(clients)) * 100)
                time.sleep(0.5)  # Simulate processing time for each client

        zip_buffer.seek(0)

        # Save the ZIP file temporarily
        zip_filename = 'clients_csv.zip'
        with open(zip_filename, 'wb') as f:
            f.write(zip_buffer.read())

        return jsonify({'filename': zip_filename})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/progress')
def get_progress():
    return jsonify({'progress': progress})

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, mimetype='application/zip', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
