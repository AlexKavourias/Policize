from flask import redirect, render_template, request, g
from DataAnalysis import TwitterCorpus as tc #Module provides access to Twitter data
import sqlite3
DATABASE = 'FlaskMoc.sqlite3'

app = Flask('Policize')
moc = set(map(lambda x: x[1], tc.get_mocs()))

def fetch_db():
    database = getattr(g, '_database', None)
    if not database:
        database = g._database = sqlite3.connect(DATABASE)
    return database

@app.teardown_appcontext
def close_connection(exception):
    database = getattr(g, '_database', None)
    if database:
        database.close()

@app.route('/', methods=['GET','POST'])
def index(): 
    if request.method == 'POST':
        return redirect('/user/%s' % request.form['handle'].lower())
    else:
        return render_template('index.html', static_folder ='/static/')

@app.route('/about/')
def about():
    return render_template('about.html')
    
@app.route('/user/<handle>')
def profile(handle): 
    curs = fetch_database().cursor()
    fetch = curs.execute("select * from Members where handle = '%s' " % handle).fetchone()
    if fetch is None:
        return 'User Not Found'
    else:
        return render_template('sirftemp.html',
                               name=fetch[0],
                               handle=fetch[1],
                               party=fetch[2],
                               tweet_count=fetch[3],
                               img_url=handle,
                               district=fetch[5],
                               title=fetch[6],
                               color = 'red' if fetch[2] == 'R' else 'blue')
        


if __name__ == '__main__':
    app.run()
