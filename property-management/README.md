# Property Management Website

A modern, responsive website for a property management company built with Flask and Bootstrap 5.

## Features

- Modern, responsive design
- Hero section with property showcase
- Services overview
- Featured properties listing
- About section
- Contact form
- Mobile-friendly layout

## Technologies Used

- Python 3.13
- Flask 3.0
- Bootstrap 5
- HTML5/CSS3

## Setup

1. Clone the repository:
```bash
git clone [repository-url]
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The website will be available at: http://127.0.0.1:5000

## Project Structure

```
property-management/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── templates/         
│   └── landing.html   # Main landing page template
└── static/
    └── css/
        └── style.css  # Custom styles
```

## Development

The application runs in debug mode by default for development purposes. For production deployment, make sure to:
1. Set DEBUG = False in app.py
2. Use a production-grade WSGI server
3. Set up proper security measures

## License

MIT License 