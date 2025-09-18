# LearnPython

LearnPython is an interactive Django-based web application designed to teach Python programming to young learners in multiple languages, including English, Yoruba, Igbo, and Hausa. The platform offers gamified lessons, code previews, audio explanations, and progress tracking to make learning Python engaging and accessible.

## Features

- **Interactive Lessons**: Hands-on coding exercises and challenges to enhance learning.
- **Multilingual Support**: Lessons and audio explanations available in English, Yoruba, Igbo, and Hausa.
- **Audio Integration**: Listen to code explanations in your preferred language, powered by Spitch API.
- **User Accounts**: Sign up, log in, and track your learning journey.
- **Admin Dashboard**: Manage users, lessons, and translations efficiently.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL (recommended for production)
- [Cloudinary](https://cloudinary.com/) account for media storage

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/JoseSholly/learn_python.git
   cd learn_python/learn_python
   ```

2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Copy `.env.example` to `.env`:
     ```sh
     cp .env.example .env
     ```
   - Fill in your secrets in `.env` (e.g., Cloudinary credentials, database settings, email configuration).

4. **Run migrations and collect static files**:
   ```sh
   python manage.py migrate
   python manage.py collectstatic
   ```

5. **Start the development server**:
   ```sh
   python manage.py runserver
   ```

6. **Access the app**:
   - Visit [http://localhost:8000](http://localhost:8000) in your browser.

## Management Commands

- `python manage.py create_lessons`: Populate the database with sample lessons.
- `python manage.py generate_translation`: Generate lesson translations using the Spitch API.
- `python manage.py generate_audio`: Generate audio explanations for translations using Spitch API.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Powered by [Spitch](https://spitch.io/) for multilingual audio generation.
- Built with [Django](https://www.djangoproject.com/) and [Cloudinary](https://cloudinary.com/).