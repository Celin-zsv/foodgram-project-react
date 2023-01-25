# praktikum_new_diplom

# скопировать репозиторий
cd dev
git clone  https://github.com/Celin-zsv/foodgram-project-react

# создать и активировать виртуальное окружение:
python -m venv env
. env/Scripts/activate

# установить зависимости из requirements.txt:
python -m pip install --upgrade pip
pip install -r requirements.txt

# выполнить миграции, создать пользователя
cd backend/
python manage.py migrate
python manage.py createsuperuser

# запустить сервер, открыть админку и спецификацию API
python manage.py runserver
http://127.0.0.1:8000/admin/
http://127.0.0.1:8000/redoc/