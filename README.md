# Social Media Api

RESTful API for a social media platform. The API allow users to create profiles, follow other users, create and retrieve posts, manage likes and comments, and perform basic social media actions.

# Features
- JWT authentication
- Admin panel /admin/
- Documentation is located at /api/doc/swagger/ and /api/doc/redoc/
- Managing posts, likes and comments in service
- Creating user at /api/user/
- Login user at /api/user/token/
- Logout user at /api/user/logout/
- Creating posts at /api/post/
- Managing followers and followings
- Run PR in docker

# Installing using GitHub
```
git clone https://github.com/MarynaProkhorenko/social-media-api
cd social_media_api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# .env file
Open file .env.sample and change environment variables to yours. Also rename file extension to .env
# Run on local server

- Install PostgreSQL, create DB and User
- Connect DB
- Run:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
# Run with Docker
Docker should be already installed
```
docker-compose build
docker-compose up
```

# Create/Authenticate User

- Path to create user: api/users
- Path to login user: api/users/token
- Authorize Bearer

# Stop server:
```
dokcer-compose down
```