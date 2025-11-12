from src import create_app

app = create_app()

app.run(debug=True)

# gunicorn -b 0.0.0.0 -w 4 'src:create_app()'