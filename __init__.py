import flask
from flask import *
from DataAnalysis import TwitterCorpus as tc
import sqlite3


app = Flask('Politicize')
moc = set(map(lambda x: x[1],tc.get_mocs()))


@app.route('/', methods=['GET','POST'])
def index(): 
    if request.method == 'POST':
        return redirect('http://127.0.0.1:5000/user/'+request.form['handle'].lower())
    else:
        return flask.render_template('index.html',static_folder ='/static/')

@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/user/<handle>')
def profile(handle): 
    curs = sqlite3.connect('C:/users/alex/desktop/FlaskMoc.sqlite3').cursor()
    fetch = curs.execute("select * from Members where handle = '%s' " % handle).fetchone()
    if fetch is None:
        return 'User Not Found'
    else:
        return render_template('sirftemp.html',
                               name=fetch[0],handle=fetch[1],
                               party=fetch[2],
                               tweet_count=fetch[3],
                               img_url=handle,
                               district=fetch[5],
                               title=fetch[6],
                               color = 'red' if fetch[2] == 'R' else 'blue')
        


if __name__ == '__main__':
    app.run(debug=True)