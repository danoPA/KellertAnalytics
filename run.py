from bottle import route, run, template, get
from bottle import static_file, url
import json
import os

def check_login(username, password):
	with open("login.json", 'r') as infile:
		logins = json.load(infile)
		try:
			return logins[username] == password
		except KeyError:
			return False

@route('/')
def home():
	return template("index.html", url = url)


@route('/static/<filename>', name = 'static')
def send_static(filename):
    return static_file(filename, root='static')

# Static Routes
# @get('/<filename:re:.*\.js>')
# def javascripts(filename):
#     return static_file(filename, root='static/js')

# @get('/<filename:re:.*\.css>')
# def stylesheets(filename):
#     return static_file(filename, root='static/css')

# @get('/<filename:re:.*\.(jpg|png|gif|ico)>')
# def images(filename):
#     return static_file(filename, root='static/img')

# @get('/<filename:re:.*\.(eot|ttf|woff|svg)>')
# def fonts(filename):
#     return static_file(filename, root='static/fonts')


from bottle import get, post, request # or route

@get('/login') # or @route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''

@post('/login') # or @route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"

if __name__ == "__main__":

    port = int(os.environ.get('PORT', 5000))
    main.app.run(host='0.0.0.0', port=port)