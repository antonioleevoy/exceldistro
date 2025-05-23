
# Exceldistro

**Exceldistro** is a web application designed to facilitate easy splitting of large Excel files through a user-friendly interface accessible to anyone. Built with Python and HTML/CSS, it allows users to upload and download split up Excel documents seamlessly.

## Features

- **Excel File Split Automation**: Upload and share Excel files effortlessly.
- **Web Interface**: Intuitive UI for managing and accessing files.
- **Deployment Ready**: Configured for deployment on platforms like Vercel and Virtual Machines.

## Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/antonioleevoy/exceldistro.git
   cd exceldistro
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python app.py
   ```

4. Open your browser and navigate to `http://localhost:5000` to access the application.

## Deployment

The application is configured for deployment on Vercel. Ensure you have the Vercel CLI installed and run:

```bash
vercel
```

Follow the prompts to deploy your application.

## Project Structure

- `app.py` - Main application file.
- `templates/` - HTML templates for the web interface.
- `static/` - Static files like CSS and JavaScript.
- `requirements.txt` - Python dependencies.
- `vercel.json` - Configuration for Vercel deployment.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.
