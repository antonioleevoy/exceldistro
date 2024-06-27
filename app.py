from flask import Flask, request, send_file, render_template, jsonify
import pandas as pd
import os
from zipfile import ZipFile
import io

app = Flask(__name__)

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.cache_control.no_cache = True
    response.cache_control.must_revalidate = True
    response.cache_control.max_age = 0
    response.expires = 0
    response.pragma = 'no-cache'
    return response

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def handle_file_upload():
    try:
        file = request.files['file']
        prefix = request.form['prefix']

        if file.filename == '':
            return jsonify({'error': 'No file selected'})

        # Extract the file name without the extension
        file_base_name = os.path.splitext(file.filename)[0]

        # Read the specified sheet from the uploaded Excel file into a DataFrame
        df = pd.read_excel(file, sheet_name='REACHRoHs')

        # Ensure the DataFrame contains the correct columns
        if 'Client' not in df.columns:
            return jsonify({'error': 'The specified sheet does not contain a "Client" column.'})

        # Select columns B to J (assuming 0-indexed, columns 1 to 9)
        df = df.iloc[:, 1:10]

        # Split the DataFrame by 'Client' column and save CSVs to an in-memory ZIP file
        clients = df['Client'].unique()
        zip_buffer = io.BytesIO()

        with ZipFile(zip_buffer, 'a') as zip_file:
            for client in clients:
                client_df = df[df['Client'] == client]
                print(f"Processing client: {client} with {len(client_df)} rows")  # Debug print
                csv_buffer = io.StringIO()
                client_df.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)
                zip_file.writestr(f'{prefix}{client}.csv', csv_buffer.getvalue())

        zip_buffer.seek(0)

        # Save the ZIP file temporarily with a name based on the uploaded file
        zip_filename = f'{file_base_name}_clients_csv.zip'
        with open(zip_filename, 'wb') as f:
            f.write(zip_buffer.read())

        return jsonify({'filename': zip_filename})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, mimetype='application/zip', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
