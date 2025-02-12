# Social Media API

A fully functional social media backend built with Django Rest Framework (DRF). This API provides user authentication, blog post management, a commenting system, and advanced filtering/searching capabilities.

## Features

### User Authentication & Authorization
- User registration and login
- JWT-based authentication for secure access
- Account activation via OTP sent to the user's email
- Password reset functionality using OTP verification

### Blog Management
- Registered users can create, edit, and delete blog posts
- Posts can be saved as "Draft" or marked as "Published" for visibility control

### Commenting System
- Logged-in users can comment on blog posts
- Users can edit or delete their comments

### Additional Features
- Pagination for posts to improve navigation
- Filtering and keyword-based search for quick access to specific content

## Technology Stack
- **Backend:** Django Rest Framework (DRF)
- **Database:** MySQL
- **Authentication:** JWT (JSON Web Tokens)

## Installation

1. Clone the repository:
   git clone https://github.com/rupak26/SocialMedia.git
   cd SocialMedia
2.Create a virtual environment and activate it:
  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3.Install dependencies
  pip install -r requirements.txt
4.Apply Migration
  python manage.py migrate
5.Create Superuser
  python manage.py createsuperuser
6.Run on development Server
  python manage.py runserver

**API Endpoints**
Authentication
Method	Endpoint	Description
  POST	/api/auth/register/	Register a new user
  POST	/api/auth/login/	Login and receive JWT token
  POST	/api/auth/logout/	Logout the user
  POST	/api/auth/activate/	Activate account via OTP
  POST	/api/auth/reset-password/	Request password reset via OTP
  POST	/api/auth/reset-password/confirm/	Confirm new password
Blog Posts
Method	Endpoint	Description
  GET	/api/posts/	List all blog posts
  POST	/api/posts/	Create a new post
  GET	/api/posts/{id}/	Retrieve a single post
  PUT	/api/posts/{id}/	Update a post
  DELETE	/api/posts/{id}/	Delete a post
Comments
Method	Endpoint	Description
  POST	/api/posts/{id}/comments/	Add a comment to a post
  PUT	/api/comments/{id}/	Edit a comment
  DELETE	/api/comments/{id}/	Delete a comment
Contribution
Feel free to fork this repository, create a feature branch, and submit a pull request with improvements or bug fixes.

License
This project is licensed under the MIT License.

Made with ❤️ by Rupak Biswas
