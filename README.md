# simple_chat
This repository contains an API based on DRF for simple chat

## Installation
```shell
git clone https://github.com/KirillDrago/simple_chat.git
python3 -m venv venv
source venv/bin/activate (Linux and macOS) or venv\Scripts\activate (Windows)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Getting access
- ```python manage.py createsuperuser``` - create user
- get access token via /api/token/

### Features
- JWT authenticated
- Admin panel /admin/
- Creating threads with users
- Sending message in threads

### Endpoints
- /admin - admin panel
- /threads - list of threads
- /threads/create - create a new thread
- /threads/<<int:pk>>/ - list of messages in thread
- /threads/<<int:pk>>/delete - delete thread
- /threads/<<int:pk>>/send_message - send message to the thread
- /users - list of users with count of unread messages
- api/token - get JWT token
- api/token/refresh - refresh JWT token
- api/token/verify - check if the JWT token is valid