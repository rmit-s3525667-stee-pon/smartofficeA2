from smartoffice import app

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.run(host = '0.0.0.0', port = 80 ,debug=True)
