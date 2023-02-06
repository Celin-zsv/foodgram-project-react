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

### доступны следующие URL:
* http://127.0.0.1:8000/api/tag/
    * Tag List
    * PAGINATION
        * DEFAULT_PAGINATION_CLASS
        * PageNumberPagination
        * PAGE_SIZE: 10
    * PERMISSION, RESPONSE SCHEMA: the same -> Tag Instance
    * Allow: GET, POST
    * unique fields: slug
    * ordering: id

* http://127.0.0.1:8000/api/tag/3/
    * Tag Instance
    * PERMISSION: 
        * IsAuthenticated
        * DEFAULT_PERMISSION_CLASSES
    * Allow: GET, PUT, PATCH, DELETE
    * RESPONSE SCHEMA: application/json
```
id	
integer

name	
string <= 200 characters
Название

color	
string or null <= 7 characters
Цвет в HEX

slug	
string or null <= 200 characters ^[-a-zA-Z0-9_]+$
Уникальный слаг
```

----------------
ver.1_12

### доступны следующие URL:
* http://127.0.0.1:8000/api/ingredient/
    * Ingredient List
    * PAGINATION
        * DEFAULT_PAGINATION_CLASS
        * PageNumberPagination
        * PAGE_SIZE: 10
    * PERMISSION, RESPONSE SCHEMA: the same -> Ingredient Instance
    * Allow: GET, POST
    * Поиск по частичному вхождению в начале названия ингредиента
        * РЕЗУЛЬТАТ поиска по:
            * http://127.0.0.1:8000/api/ingredient/?search=К
			* вернет ингредиент: name='Капуста' 
			* вернет ингредиент: по <начальному символу /начальным символам>
            * "при использовании базы данных sqlite поиск нечувствителен к регистру только при запросах на латинице"

* http://127.0.0.1:8000/api/ingredient/4/
    * Ingredient Instance
    * PERMISSION: 
        * IsAuthenticated
        * DEFAULT_PERMISSION_CLASSES
    * Allow: GET, PUT, PATCH, DELETE
    * RESPONSE SCHEMA: application/json
```
id	
integer

name
string <= 200 characters

measurement_unit
string <= 200 characters
```
----------------
ver.1_13

### доступны следующие URL:
* http://127.0.0.1:8000/api/recipe/{id}/
    * Recipe Instance
    * PERMISSION: 
        * IsAuthenticated
        * DEFAULT_PERMISSION_CLASSES    
    * Allow: GET, PUT, PATCH, DELETE,
    * RESPONSE SCHEMA: application/json    
```
id	
integer

tags
Array of objects (Tag)
Список тегов

in Array tags
id	
integer

in Array tags
name	
string <= 200 characters
Название

in Array tags
color	
string or null <= 7 characters
Цвет в HEX

in Array tags
slug	
string or null <= 200 characters ^[-a-zA-Z0-9_]+$
Слаг

author
object (User)
Пользователь (В рецепте - автор рецепта)

Array author : NO yet

ingredients	
Array of objects (IngredientInRecipe)
Список ингредиентов

in Array ingredients
id	
integer

in Array ingredients
name
string <= 200 characters
Название

in Array ingredients
measurement_unit
string <= 200 characters
Единицы измерения

in Array ingredients
amount	
integer >= 1
Количество

is_favorited : NO yet
boolean
Находится ли в избранном

is_in_shopping_cart : NO yet
boolean
Находится ли в корзине

name
string <= 200 characters
Название

image : NO yet
string <url>
Ссылка на картинку на сайте

text
string
Описание

cooking_time
integer >= 1
Время приготовления (в минутах)
```
----------------
ver.1_14

### доступна ЗАПИСЬ данных-> URL:
* POST http://127.0.0.1:8000/api/recipe/
* check: 'Обязательный ввод инградиннта-> id'
* Content-Type: application/json
```
{
    "ingredients": [
        {
            "id": 8,    #  need to know id Ingedient
            "amount": 11
        },
        {
            "id": 9,    #  need to know id Ingedient
            "amount": 22
        },
    ],
    "tags": [
        1,
        2
    ],
    "name": "string",
    "text": "string",
    "cooking_time": 1
}
```
### доступно ЧТЕНИЕ данных-> URL:
* GET http://127.0.0.1:8000/api/recipe/
* GET http://127.0.0.1:8000/api/recipe/{id}/
* Content-Type: application/json
```
{
    "id": 60,
    "tags": [],
    "author": null,
    "ingredients": [
        {
            "id": 8,
            "name": "Инградиент-1 from Postman",
            "measurement_unit": "кг-1 from Postman",
            "amount": 21
        },
        {
            "id": 4,
            "name": "Горчица",
            "measurement_unit": "ложка",
            "amount": 21
        }
    ],
    "name": "Postman рецепт №12",
    "text": "рецепт from zsv12",
    "cooking_time": 172
}

```
----------------
ver.1_15

### доступно ИЗМЕНЕНИЕ существующих данных-> URL:
* POST http://127.0.0.1:8000/api/recipe/{id}
* Обновление рецепта
    * в URL указать id существующего Рецепта
    * изменение истории-ингредиентов-> доступно:
        * указать id существующего ингредиента: 
            * при изменении / создании записи истории-инградиента
        * изменить количество:
            * при изменении записи истории-инградиента
        * удалить запись итории-инградиента
        * добавить запись истории-инградиента

----------------
ver.1_16

### добавлено:
* приложение users
    * пользовательская model User(AbstractUser) 
* ссылки на app users
    * Recipe.author
    * Favorite.user
    * Shopping.user

----------------
ver.1_17