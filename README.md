# Launch app

To create new server, run
`./deploy.sh`
in either game/ or game-server/ directory.
It requires configured eb and aws cli tools.

To deploy new code to existing server, run
`eb deploy`
in proper directory.

To run Django localy:
```sh
python manage.py makemigrations 
python manage.py migrate
python manage.py runserver
```

To run local game server:
`npm start`
