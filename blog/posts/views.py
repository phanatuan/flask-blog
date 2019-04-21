from blog import db
from flask import Blueprint, render_template, redirect, flash, url_for, request
from blog.models import Post, load_user, Category, Comment
from blog.posts.forms import AddPostForm, UpdatePostForm, AddCommentForm
from flask_login import login_required, current_user

posts_blueprint = Blueprint('posts', __name__, template_folder='templates/')
comments_blueprint = Blueprint(
    'comments', __name__, template_folder='templates/')


@posts_blueprint.route('/add', methods=['GET', 'POST'])
def add():
    form = AddPostForm()
    if form.validate_on_submit():

        title = form.title.data
        body = form.body.data
        selected_category = form.category.data

        new_post = Post(title, body, current_user.id)

        if form.category.data is not None:
            for cat_id in form.category.data:
                cat_selected = Category.query.get(int(cat_id))
                new_post.add_category.append(cat_selected)

        db.session.add(new_post)
        db.session.commit()

        flash('Posting Successful', 'success')
        return redirect(url_for('posts.list'))

    return render_template('posts/add.html', form=form)

@posts_blueprint.route('/list')
def list():
    posts = Post.query.all()
    return render_template('posts/list.html', posts=posts)

@posts_blueprint.route('/read/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):

    post = Post.query.get(post_id)
    comment_form = AddCommentForm()
    comments = post.comments

    if comment_form.validate_on_submit():

        if current_user.is_authenticated:

            content = comment_form.content.data
            new_comment = Comment(content, current_user.id, post_id)

            db.session.add(new_comment)
            db.session.commit()

            return redirect(url_for('posts.show_post',
                                    post_id=post_id,
                                    comment_form=comment_form))

        else: 
            flash('Please log in to comment', 'warning')
            return redirect(url_for('users.login'))

    return render_template('posts/post_id.html'         
                                ,post=post
                                ,comment_form=comment_form
                                ,comments=comments)

@posts_blueprint.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):

    post = Post.query.get(post_id)
    form = UpdatePostForm()

    if current_user != post.author: 
        flash('You are not authorized to edit post of other people', 'danger')
        return redirect(url_for('posts.list'))

    if request.method == 'GET': 
        form.title.data = post.title
        form.body.data = post.body
    
    if request.method == 'POST': 
        title = form.title.data
        body = form.body.data 

        post.title = title
        post.body = body

        db.session.commit()
        flash('Post Successfully Update', 'success')
        
        return redirect(url_for('posts.edit', post_id=post_id))

    return render_template('posts/edit.html', form=form, post=post)

@posts_blueprint.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):

    delete_post = Post.query.get(post_id)
    
    if current_user != delete_post.author: 
        flash('You are not authorized to delete post of other people', 'danger')
        return redirect(url_for('posts.list'))

    db.session.delete(delete_post)
    db.session.commit()

    flash('Delete Post Successfully', 'success')
    return redirect(url_for('posts.list'))

@posts_blueprint.route('/favorite/add/<int:post_id>', methods=['GET', 'POST'])
@login_required
def add_favorite(post_id):

    favorite_post = Post.query.get(post_id)

    if favorite_post in current_user.favorite: 
        flash('You already favorite this bro', 'warning')
        return redirect(url_for('posts.list'))

    current_user.favorite.append(favorite_post)
    db.session.commit()

    flash('Favorite Post was added', 'success')
    return redirect(url_for('users.account'))


@posts_blueprint.route('/favorite/remove/<int:post_id>', methods=['GET', 'POST'])
@login_required
def remove_favorite(post_id):

    remove_favorite_post = Post.query.get(post_id)
    current_user.favorite.remove(remove_favorite_post)
    
    db.session.commit()
    flash('Favorite Removed', 'success')

    return redirect(url_for('users.account'))

@comments_blueprint.route('/delete/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):

    delete_comment = Comment.query.get(comment_id)
    post_id = delete_comment.belong_to_post.id

    if current_user != delete_comment.author: 
        flash('You are not authorized to delete comment of other people', 'warning')

    db.session.delete(delete_comment)
    db.session.commit()

    flash('Delete Comment Successfully', 'success')
    return redirect(url_for('posts.show_post', post_id=post_id))

