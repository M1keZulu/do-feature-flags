from flask import Flask, request, render_template, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'testing_secret_key'

features = {
    'addition': False,
    'multiplication': False,
    'subtraction': False,
    'division': False,
    'submit': False,
    'input': False,
    'title': False
}

admin_username = 'admin'
admin_password = 'password'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_username and password == admin_password:
            session['logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/admin_panel', methods=['GET', 'POST'])
def admin_panel():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        for feature in features:
            if feature in request.form:
                features[feature] = not features[feature]
    return render_template('admin_panel.html', features=features)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/api/features')
def get_features_status():
    return jsonify(features)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
