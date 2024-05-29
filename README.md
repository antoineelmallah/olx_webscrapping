To run application, follow the steps:

1. Install virtualenv

`pip install virtualenv`

2. Create a virtualenv

`virtualenv venv`

3. Ensure virtualenv in activated

3.1. To activate:
`source .venv/bin/activate`

3.2. To deactivate:
`deactivate`

4. Install MariaDB and create one database

5. Create 2 environment variables on .bashrc file:

5.1. Database connection string
`export WEBSCRAPING_DB_CONNECTION_STRING=mariadb+mariadbconnector://<USERNAME>:<PASSWORD>@127.0.0.1:3306/<DATABASE_NAME>`

5.2. Zipcodestack api key (Free geocode API - https://zipcodestack.com/)
`export ZIPCODESTACK_API_KEY=...`

6. Install all dependencies

`pip install -r requirements.txt`

7. Run file main.py