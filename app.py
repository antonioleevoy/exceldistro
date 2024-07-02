from flask import Flask, request, send_file, render_template, jsonify
import pandas as pd
import os
from zipfile import ZipFile
import tempfile
import shutil

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

        # Create a temporary directory to store CSV files
        with tempfile.TemporaryDirectory() as temp_dir:
            clients = df['Client'].unique()

            for client in clients:
                client_df = df[df['Client'] == client]
                print(f"Processing client: {client} with {len(client_df)} rows")  # Debug print
                client_csv_path = os.path.join(temp_dir, f'{prefix}{client}.csv')
                client_df.to_csv(client_csv_path, index=False)

            # Create a ZIP file of the temporary directory
            zip_filename = f'{file_base_name}_clients_csv.zip'
            shutil.make_archive(file_base_name, 'zip', temp_dir)

            # Move the created ZIP file to the current working directory
            shutil.move(f'{file_base_name}.zip', zip_filename)

        return jsonify({'filename': zip_filename})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, mimetype='application/zip', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
