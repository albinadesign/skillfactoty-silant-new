# Skillfactory Silant

## Описание проекта

Проект "Skillfactory Silant" включает в себя две основные части: backend и frontend. Backend реализован с использованием Django и Django REST framework, а frontend построен на React.

## Требования

- Python 3.8 или выше
- Node.js 14 или выше
- npm (Node Package Manager)
- Git

## Установка и запуск проекта

### Шаг 1: Клонирование репозитория

Сначала клонируйте репозиторий на свой локальный компьютер:

git clone https://github.com/albinadesign/skillfactoty-silant.git

cd skillfactoty-silant

cd Diplom

### Шаг 2: Настройте backend

Перейдите в папку backend:

cd backend

Создайте и активируйте виртуальное окружение:


Для Windows:

python -m venv venv

venv\Scripts\activate


Для macOS и Linux:

python3 -m venv venv

source venv/bin/activate


Установите зависимости:

pip install -r requirements.txt


Выполните миграции базы данных:

python manage.py migrate


Создайте суперпользователя:

python manage.py createsuperuser


Запустите сервер разработки:

python manage.py runserver


### Шаг 3: Настройте frontend

Перейдите в папку frontend:

cd ../frontend


Установите зависимости:

npm install


Для разработки запустите сервер разработки:

npm start


Для продакшн-среды создайте оптимизированную сборку:

npm run build


### Шаг 4: Откройте приложения

Откройте браузер и перейдите по адресу http://localhost:3000, чтобы увидеть фронтенд часть приложения. 

Для доступа к админке Django, перейдите по адресу http://localhost:8000/admin и используйте учетные данные, созданные на шаге 2


### API Документация

Документация по API доступна по адресу http://localhost:8000/api/swagger/ после запуска сервера backend.


<img width="1501" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/05fa425d-ce8d-4979-82a5-76f1c1f5ac67">


Админ и менеджеры могут создавать, редактировать справочники (Reference) и всю остальную информацию по пользователям и машинам

Сервисные компании могут вносить изменения по свои машинам

Пользователи могут только просматривать


### Структура проекта

backend/ - папка с кодом backend.


frontend/ - папка с кодом frontend.

 
### Админ панель

по адресу http://localhost:8000/admin/  логин admin пароль admin

<img width="658" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/7feffaa1-3a65-4149-b0ed-2b039fd9eeaf">


### Сайт доступен по адресу http://localhost:3000/

Неавторизованному пользователю открывается таблица с общей доступной информацией по машинам, есть поиск по заводскому номеру машины

<img width="1436" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/832fd12a-fea7-4fd7-be67-069de268871e">


При клике на информацию из справочников, открывается страница справочника

<img width="1278" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/3fe4a45c-b1ad-469c-8dc2-c72e486223f4">


При клике на кнопку Авторизация открывается соответствующая страница. Пользователь может только войти в систему, зарегистрироваться нельзя (только через менеджера или админа)

<img width="1309" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/dfdb820d-d6bf-40d3-aa4f-36fa6152ed82">


### Вход в систему для проверки

Менеджер

логин manager

пароль 9zq-Ce4-g2i-Pun


Клиенты

логин trudnikov или  mosgorrest или Zander или SPB или Ranskiy или Minus или Krasnodar или FSN или FRP или DET и все клиенты

пароль hFu-5QN-4ed-TNQ


Сервисные компании

логин silant или Promtechnika  или FNS и все сервисные компании

пароль PXK-S7j-8SU-mU9


### Зайдем от лица менеджера, 

которому доступна вся информация. Наиболее полная таблица на всех вкладках, есть фильтры, данные сортированы по датам

<img width="1409" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/5a87e664-da45-426e-be2b-79be95dbe320">

<img width="1354" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/d78038aa-c34f-442c-8a7b-9b63692b6233">

<img width="1380" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/6191217c-716e-4161-bb5e-4fa64d339369">

<img width="1537" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/aa04b6fa-0997-44bc-bd40-2bed949a198b">


### Зайдем от лица клиента

В общей вкладке ему все еще доступна общая информация по машинам, но подробности можно увидеть только для своих машин

<img width="1508" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/41bc5977-91ed-4965-8766-0d267b1ed07c">

<img width="1424" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/be1c7e31-00c5-4e90-8fac-e55bc9bc46ee">


В остальных вкладках ему доступна информация только по своим машинам

<img width="1440" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/b786a2cb-1a4b-4126-830f-f8442f8c8662">

<img width="1362" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/e0172963-2ad0-4e9a-8462-4acbc157ef91">


### Все то же самое, если зайдем от лица сервисной компании

<img width="1463" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/1a069ba4-e1d2-43fe-a1cb-e64176c4f5dd">

<img width="1360" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/d58e52bd-4673-4052-9c13-d3f8d43b748e">

<img width="1424" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/da59e407-8288-4119-9d2d-abb2287f63cc">

<img width="1396" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/aabc0778-cf93-49b5-86d7-c442ecf3d992">


### Сайт адаптирован под мобильные устройства

<img width="497" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/ee3fcd61-f8e4-4c99-8ced-3f07abedf355">

<img width="497" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/019661e3-3eff-4e28-88b7-dba750f913fd">

<img width="419" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/fe72cf0c-2a85-4d37-9aca-84f17efed2d9">

<img width="418" alt="image" src="https://github.com/albinadesign/skillfactoty-silant/assets/117900508/02f6fd8c-22b6-47f4-aa9b-e0b878460500">
























