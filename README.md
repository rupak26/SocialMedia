# Social Media APP

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

2. Create a virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install dependencies
   pip install -r requirements.txt

4. Apply Migration
   python manage.py migrate

5. Create Superuser
   python manage.py createsuperuser

6. Run on development Server
   python manage.py runserver


**API Endpoints**
**Authentication**

Method	Endpoint	Description
  1. Register a new user :: 
  
  POST	{**/user/register/**}	
  
  2. Login and receive JWT token ::
  
  POST	{**/user/login/**}	
  
  3. Logout the user :: 
  
  POST	{**/user/logout/**}
  
  4. Activate account via OTP :: 
  
  POST	{**/user/activate/**}	
  
  5. Request password reset via OTP :: 

  POST	{**/user/reset-password/**}	
  
  6. Confirm new password ::

  POST	{**/user/reset-password/confirm/**}	
  
**Blog Posts**

Method	Endpoint	Description
**List all blog posts ::**
  
  GET	{**/content/posts/**}
  
  **Create a new post ::
  
  POST	{**/content/posts/**}
  
  **Retrieve a single post ::
  
  GET	{**/content/posts/{id}/**}	
  
  **Update a post ::
  
  PUT	{**/content/posts/{id}/**}	
  
  **Delete a post ::
  
  DELETE	{**/content/posts/{id}/**}	
  
**Comments**

Method	Endpoint	Description
  **Add a comment to a post ::
  
  POST	{**/comment/posts/{id}/comments/**}
  
  **Edit a comment ::
  
  PUT	{**/comments/{id}/**}	
  
  **Delete a comment :: 
  
  DELETE	{**/comments/{id}/**}	
  
**Contribution**

Feel free to fork this repository, create a feature branch, and submit a pull request with improvements or bug fixes.

**License**
This project is licensed under the MIT License.

Made with ❤️ by Rupak Biswas
