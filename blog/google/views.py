from flask_dance.contrib.google import make_google_blueprint, google
from flask import url_for, redirect, render_template, flash

google_bp = make_google_blueprint(
        client_id='929432084569-usdl52gktsmqebaov7najvd3mnlrtj6n.apps.googleusercontent.com', 
        client_secret='JVzcWEcK4qefRnD7POaeP9m5', 
        offline=True, 
        scope=['profile', 'email'])

@google_bp.route('/google')
def google_login(): 

    if not google.authorized: 
        return redirect(url_for('google.login'))
    
    resp = google.get('/oauth2/v2/userinfo')
    
    assert resp.ok, resp.text
    email = resp.json()['email']
    print('******' + email)

    return render_template('test.html', email=email)
