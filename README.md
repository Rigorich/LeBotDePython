# Django Telegram Bot
currently designed to help you learn new words

### Commands:
- /start - welcome message with information
- /new - show new word to learn it
- /repeat - repeat shown word to remember it
- /admin - list of admin's commands

----
### How to run

#### 1) Clone repository and install required packages
```
git clone https://github.com/Rigorich/LeBotDePython
cd LeBotDePython
pip install -r requirements.txt
```

#### 2) Create `.env` file in root directory and put info
```
DEBUG=0
DJANGO_SECRET_KEY=a1b2c3d4e5f6g7h8i9j0
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/DATABASE_NAME
TELEGRAM_TOKEN=1234567890:AAABACABADABACABAEABACABADABACABAAA
ADMIN_ID=123456789
```

#### 3) Create PostgreSQL database with name _DATABASE_NAME_ and run migrations
```
sudo -u postgres psql -c "CREATE DATABASE DATABASE_NAME;"
python manage.py migrate
```

#### 4) Run bot in pooling mode
```
python run_pooling.py 
```

#### 5) Create super user and run Django admin panel (http://localhost:8000/tgadmin/)
```
python manage.py createsuperuser
python manage.py runserver
```

----
