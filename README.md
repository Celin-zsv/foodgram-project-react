# praktikum_new_diplom

### скопировать репозиторий
```
cd dev
git clone  https://github.com/Celin-zsv/foodgram-project-react
```
### создать и активировать виртуальное окружение:
```
python -m venv env
. env/Scripts/activate
```
### установить зависимости из requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
### выполнить миграции, создать пользователя
```
cd backend/
python manage.py migrate
python manage.py createsuperuser
```
### запустить сервер, открыть админку и спецификацию API
```
python manage.py runserver
http://127.0.0.1:8000/admin/
http://127.0.0.1:8000/redoc/
```
### открыть админку, войти под созданным-выше пользователем, открыть(ниже URL) REST API
* http://127.0.0.1:8000/api/
### доступны следующие URL -> Base Djoser Endpoints:
* http://127.0.0.1:8000/api/
    * Api Root
* http://127.0.0.1:8000/api/users/
    * User List
* http://127.0.0.1:8000/api/users/1/
    * User Instance	PUT, PATCH,	{    "email": "admin@gmail.com",    "id": 1,    "username": "admin"}
* http://127.0.0.1:8000/api/auth/token/login/
    * Token Create
* http://127.0.0.1:8000/api/auth/token/logout/
    * Token Destroy	post {}
* http://127.0.0.1:8000/api/users/me/
    * Me
* http://127.0.0.1:8000/api/users/confirm/
    * User Instance
* http://127.0.0.1:8000/api/users/set_password/
    * Set password	post	{    "new_password": "",    "current_password": "" }
* http://127.0.0.1:8000/api/users/reset_password/
    * Reset password	post 	{    "email": ""}
* http://127.0.0.1:8000/api/users/reset_password_confirm/
    * Reset password confirm	post	{    "uid": "",    "token": "",    "new_password": ""}
* http://127.0.0.1:8000/api/users/set_username/
    * Set username	post	{    "current_password": "",    "new_username": ""}
* http://127.0.0.1:8000/api/users/reset_username/
    * Reset username	post	{    "email": ""}
* http://127.0.0.1:8000/api/users/reset_username_confirm/
    * Reset username confirm	post	{    "new_username": ""}


----------------
ver.1_11