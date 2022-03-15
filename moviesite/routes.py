import os
from flask import render_template, url_for, flash, redirect, request, abort
from moviesite import app, db, bcrypt
from moviesite.forms import RegistrationForm, LoginForm, movie, search_field 
from moviesite.models import User, Movie, category_movie_list
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

 



@app.route("/")
@app.route("/home")
def home():
    form= search_field()
    movies= Movie.query.all()
    search= request.args.get('search_movie')
    if search:
         return redirect(url_for('search',movie_name=search))
    else:
        return render_template('home.html',movies=movies, form=form)



@app.route("/search/<movie_name>")
def search(movie_name):
    '''
    View function to display the search results
    '''
    ms= Movie.query.filter_by(movie_title=movie_name).first()
    if ms:
        return render_template('search.html', 
                            movies = ms)
    else :
        flash('No such film found ','success')
        return redirect('/')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        us = User(username=form.username.data, email=form.email.data, password=hash_password , is_admin=False)
        db.session.add(us)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:

        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'{current_user.username} have been logged in!', 'success')
            return  redirect(url_for('home'))    
        else:
            flash('your logging is unsuccesful,Please check your email id and password ', 'danger')
    return render_template('login.html', title='Login', form=form)  


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home')) 

@app.route("/Upload", methods=['GET', 'POST'])
def Upload():
    if current_user.is_authenticated:

        if current_user.is_admin != True :
            abort(403)
        else:
            form=movie()
            if form.validate_on_submit():
                
                f = form.image_file.data
                filename = secure_filename(f.filename)
                mv = Movie(movie_title = form.movie_title.data, movie_desc=form.movie_desc.data, image_file= filename,movie_link = form.movie_link.data,action = form.action.data, suspense = form.suspense.data, adventure = form.adventure.data, horror = form.horror.data, comedy = form.comedy.data, scifci = form.scifci.data, release_date = form.release_date.data) 
                db.session.add(mv)
                db.session.commit()

                f.save(os.path.join(
                    app.root_path, 'static/movieimage', filename
                ))
                return redirect(url_for('Admin'))
                
            return render_template('Upload.html', form=form, legend="New Movie")
    else:
        abort(403)        
@login_required
@app.route("/Admin")
def Admin():
    if current_user.is_authenticated:

        if current_user.is_admin != True :
            abort(403)
        else:
            movies= Movie.query.all()
            return render_template('Admin.html',movies=movies)
    else:
        abort(403)



        
@app.route("/Admin/<int:m_id>/update",  methods=['GET', 'POST'])
def update_movie(m_id):
     if current_user.is_authenticated:

        if current_user.is_admin != True :
            abort(403)
        else:   
            ms= Movie.query.filter_by(m_id=m_id).first()
            form = movie()
            if form.validate_on_submit():
                ms.movie_title = form.movie_title.data
                ms.movie_desc = form.movie_desc.data
                ms.movie_link = form.movie_link.data
                ms.action = form.action.data
                ms.suspense = form.suspense.data
                ms.adventure = form.adventure.data
                ms.horror = form.horror.data
                ms.comedy = form.comedy.data
                ms.scifci = form.scifci.data
                ms.release_date = form.release_date.data
                if form.image_file.data == None:
                    db.session.commit()
                else:  
                        f = form.image_file.data
                        filename = secure_filename(f.filename)
                        ms.image_file=filename
                        db.session.commit() 
                    
                flash(f' {ms.movie_title} has been updated!', 'success')
                return redirect(url_for('Admin'))
            elif request.method == 'GET':
                    form.movie_title.data = ms.movie_title
                    form.movie_desc.data = ms.movie_desc
                    form.image_file.data = ms.image_file
                    form.movie_link.data = ms.movie_link
                    form.action.data = ms.action
                    form.suspense.data = ms.suspense
                    form.adventure.data = ms.adventure
                    form.horror.data = ms.horror
                    form.comedy.data =  ms.comedy
                    form.scifci.data = ms.scifci
                    form.release_date.data = ms.release_date

            return render_template('upload.html',form=form, legend="Update Movie")
     else:
         abort(403)

@app.route("/Admin/<int:m_id>/delete")

def delete_movie(m_id):
    ms= Movie.query.filter_by(m_id=m_id).first()
    
    db.session.delete(ms)
    db.session.commit()
    flash(f' {ms.movie_title} has been Deleted!', 'success')
    return redirect(url_for('Admin'))



@app.route("/movies/<int:id>")
def movies(id):
    if current_user.is_authenticated:
        ms= Movie.query.filter_by(m_id=id).first()
        image_path=ms.image_file
        movie_desc=ms.movie_desc
        movie_title=ms.movie_title
        movie_link = ms.movie_link
        return render_template('movies.html',image_path=image_path,
                                movie_title=movie_title,
                                movie_desc=movie_desc ,
                                movie_link=movie_link,
                                ms=ms
                                )
    else:
         return redirect(url_for('login')) 




