# Django Telegram Bot
currently designed to help you learn new words

### Commands:
- /start - welcome message with information
- /new - show new word to learn it
- /repeat - repeat shown word to remember it
- /admin - list of admin's commands

----
### How to run via Docker

#### 1) Create folder for bot (for example, _LeTestDeBotDePython_) and open it

#### 2) Copy `docker-compose.yml` from repository

#### 3) Create folder `project`, inside it create `.env` file and put this info
(Replace `DJANGO_SECRET_KEY`, `TELEGRAM_TOKEN` and `ADMIN_ID` with your parameters)
```
DATABASE_URL=postgres://postgres:postgres@db:5432/postgres
DJANGO_SECRET_KEY=a1b2c3d4e5f6g7h8i9j0
TELEGRAM_TOKEN=1234567890:AAABACABADABACABAEABACABADABACABAAA
ADMIN_ID=123456789
```

#### 4) Make sure file locations look like this
![image](https://user-images.githubusercontent.com/61323493/121154839-f4cd5100-c84f-11eb-9f65-c8087d832175.png)

#### 5) Open _LeTestDeBotDePython_ folder in Terminal and execute
```
docker-compose up
```
to see real-time logs or, for silently run,
```
docker-compose up -d
```

#### 6) Send /start command to your bot and try to open Django admin panel (http://localhost:8000/tgadmin/)

#### 7) To create super user use these commands
```
docker exec -it bot bash
python manage.py createsuperuser
```

----
### How to run via hands

#### 1) Clone repository and install required packages
```
git clone https://github.com/Rigorich/LeBotDePython
cd LeBotDePython
pip install -r requirements.txt
```

#### 2) Create `.env` file in `project` directory and put info
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
