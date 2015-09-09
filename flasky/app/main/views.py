from flask import render_template,request
from . import main
from ..models import Post
from forms import PostForm
from flask import request

@main.route('/post/')
def post():
    seachpage = request.args.get('id','')
    post = Post.query.get_or_404(seachpage) 
    return render_template('post.html', posts=[post])

@main.route('/', methods=['GET','POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
    	page = request.args.get('page', 1, type=int)
    	pagination = Post.query.filter_by(classify=form.body.data).order_by(Post.timestamp.desc()).paginate(
        page, per_page=5,
        error_out=False)
    	posts = pagination.items
    	return render_template('index.html', posts=posts,pagination=pagination,form=form)
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=5,
        error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts,
                           pagination=pagination,form=form)


