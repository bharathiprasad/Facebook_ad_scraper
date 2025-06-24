from flask import Flask, render_template, redirect, request, url_for, flash, Markup, session
from forms import SignupForm, LoginForm
import sqlite3
import ad_scraper, plots

app = Flask(__name__)
app.secret_key = 'development_key'

@app.route('/facebook/<user>')
def scrape(user):
    s = ad_scraper.FacebookScraper()
    s.generate_file(user)
    s.start_browser()
    s.start()
    return redirect(url_for('homepage',user=user))

@app.route('/home/<user>')
def homepage(user):
    if 'username' in session:
        return render_template('homepage.html', user=user)
    return redirect(url_for('login'))


@app.route('/logout', methods=['POST','GET'])
def logout():
    if 'username' in session:
        session.pop('username',None)
        return redirect('/login')
    return redirect('/login')

@app.route('/home/<user>/plots/<plot>')
def show_plot(user, plot):
    if 'username' in session:
        if plot=='frequency_plot.html':
            plots.frequency_plot(session['username'])
        if plot=='top_five_most_frequent.html':
            plots.top_five_most_frequent(session['username'])
    return redirect(url_for('plots_page', user=session['username']))

@app.route('/home/<user>/plots')
def plots_page(user):
    if 'username' in session:
        return render_template('plots.html')

@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()

    if request.method=='POST':
        if form.validate()==False:
            flash(Markup('ERROR: All fields are required.'))
            return render_template('login.html', form = form)
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('data/user_data.db') as con:
            cursor = con.cursor()
            cursor.execute("""SELECT * FROM user_data""")
            userdata = cursor.fetchall()
            for entry in userdata:
                if username == entry[0]:
                    if password == entry[1]:
                        session['username']=username
                        return redirect(url_for('homepage', user=username))
        flash(Markup('Login Failed. Enter correct username and password.'))
        return render_template('login.html', form=form)
        #write code to append 'userdata' into a json file containing all user data
        #write code to verify this 'userdata' and take appropriate actions
    elif request.method=='GET':
        if 'username' in session:
            return redirect(url_for('homepage', user=session['username']))
        return render_template('login.html', form=form)


@app.route('/signup', methods=['POST','GET'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate()==False:
            flash(Markup('ERROR: All fields are required.'))
            return render_template('signup.html', form = form)
        else:
            #write code to save username and password in a database
            with sqlite3.connect('data/user_data.db') as con:
                cur = con.cursor()

                username = request.form['username']
                password = request.form['password']
                retype_password = request.form['retype_password']

                cur.execute("""SELECT * FROM user_data""")
                userdata = cur.fetchall()
                for entry in userdata:
                    if username == entry[0]:
                        flash(Markup('ERROR: Username already exists. Choose another Username'))
                        return render_template('signup.html', form = form)

                if password==retype_password:
                    cur.execute("CREATE TABLE IF NOT EXISTS user_data(username text, password text)")
                    cur.execute("""INSERT INTO user_data(username,password)
                       VALUES (?,?)""",(username,password) )
                    con.commit()
                    flash(Markup('Successfully Registered!'))
                    return redirect(url_for('login'))
                else:
                    flash(Markup('ERROR: The passwords entered do not match.'))
                    return render_template('signup.html', form = form)
    elif request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('homepage', user=session['username']))
        return render_template('signup.html', form = form)

@app.route('/')
def enter():
    if 'username' in session:
        return redirect(url_for('homepage', user=session['username']))
    return render_template('first.html')

if __name__=='__main__':
    app.run(host='localhost', debug=True)
