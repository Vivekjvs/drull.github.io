from flask import Flask,request,render_template,redirect,session,flash,jsonify
import requests
from flask_bcrypt import Bcrypt
import os
import json
from forms import signupForm,loginForm
from werkzeug.utils import secure_filename
from database import db,cursor,insert_user,insert_comment
import test
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'big_pp'

@app.route('/')
def index():
    return render_template('index.html',title='TwoWayTech')

@app.route('/search')
def search():
    query = request.args.get('q')
    if query:
        query = test.validation(query)
        cursor.execute('SELECT * FROM devices WHERE query LIKE %s',('%'+query+'%',))
        return render_template('search.html',res=cursor.fetchall())
    return redirect('/')

@app.route('/api/comment',methods=['GET','POST'])
def comment():
    if request.method == 'POST':
        user_id = session.get('user_id')
        if user_id:
            comment_text = request.form.get('text')
            device_id = request.form.get('device_id')
            if comment_text and device_id:
                comment = insert_comment(comment_text,user_id,device_id)
                return jsonify({'status':'OK','comment':comment,'msg':'Comment Added'})
            return jsonify({'status':'Error','msg':'text or device_id not provided'})
        return jsonify({'status':'Error','msg':'Authentication fail','course':'/login'})
    else:
        device_id = request.args.get('device_id')
        if device_id:
            cursor.execute('SELECT comment_text,created_on,device_id,user_id FROM comments WHERE device_id=%s ORDER BY ID DESC',(device_id,))
            return jsonify({'comments':[{'comment_text':i[0],'created_on':i[1],'device_id':i[2],'user_id':i[3]} for i in cursor.fetchall()]})
        return jsonify({'status':'Error','msg':'device_id not provided'})

@app.route('/api/comment',methods=['DELETE'])
def updateComment():
    val = request.args.get('comment_id')
    if val:
        if request.method == "DELETE":
            cursor.execute('SELECT * FROM comments WHERE ID = %s',(val,))
            comment = cursor.fetchone()
            if comment:
                if session.get('user_id') and session['user_id'] == comment[3]:
                    cursor.execute('DELETE FROM comments WHERE ID=%s',(val,))
                    db.commit()
                    return jsonify({'status':'ok','comment':comment})
                return jsonify({'status':'Error','msg':'Authentication Failed'})
            return jsonify({'status':'Error','msg':'Invalid Comment ID'})
        else:
            return jsonify({'status':'err','msg':'invalid method'})
    return jsonify({'status':'Error','msg':'comment id not provided'})

@app.route('/device/<sql_id>')
def device(sql_id):
    cursor.execute('SELECT * FROM devices WHERE ID = %s',(sql_id,))
    data = cursor.fetchone()
    if data:
        url = f"https://fonoapi.freshpixl.com/v1/getdevice?token=6e4012ddbffd740f66b6474af07d3a85aa6f799313955ba7&device={data[1]}"
        res = requests.get(url).json()
        formula ='SELECT comments.ID,users.ID,comment_text,comments.created_on,user_name,user_image FROM comments JOIN users on comments.user_id = users.ID where comments.device_id = %s order by comments.ID desc'
        cursor.execute(formula,(sql_id,))
        return render_template('device.html',id=sql_id,data=res,comments=cursor.fetchall())
    flash('INVALID ID')
    return redirect('/')
@app.route('/signup',methods=['GET','POST'])
def signup():
    form = signupForm()
    if request.method == 'POST' and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = insert_user(form.user_name.data,form.email.data,hashed_password)
        if user:
            f = form.photo.data
            filename = secure_filename(str(user[0])+'_'+f.filename)
            f.save(os.path.join('static','profile_pic',filename))
            formula = "UPDATE users SET user_image = %s WHERE email= %s"
            cursor.execute(formula,(filename,user[3]))
            db.commit()
            flash(f"account created {user[1]}")
            return redirect('/login')
        else:
            flash('Server Err')
    return render_template('/signup.html',form=form,title='signup')
@app.route('/login',methods=['GET','POST'])
def login():
    form = loginForm()
    if request.method == 'POST' and form.validate_on_submit():
        cursor.execute('SELECT * FROM users WHERE email=%s',(form.email.data,))
        user = cursor.fetchone()
        if user:
            if bcrypt.check_password_hash(user[4],form.password.data):
                session['user_name'] = user[1]
                session['user_id'] = user[0]
                flash('success')
                return redirect('/')
            else:
                form.password.errors.append('Invlaid Password')
        else:
            form.email.errors.append('Email Does Not Exists')
    return render_template('/login.html',form=form,title='login')
@app.route('/logout')
def logout():
    if session.get('user_id'):
        session['user_id'] = None
        session['user_name'] = None
        flash('Success')
    return redirect('/')





if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=3000)
