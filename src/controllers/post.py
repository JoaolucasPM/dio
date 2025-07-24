from flask import Blueprint, request
from src.app import Post, db
from http import HTTPStatus
from sqlalchemy import inspect
#Criação do blueprint -> nome_blueprint + caminho_arquivo + nome_rota
app = Blueprint("post", __name__, url_prefix = '/posts')

#Cria post
def _created_Post():
    data = request.json
    post = Post(
         title = data["title"],
         body = data["body"],
         author_id = data["author_id"]
    )
    db.session.add(post)
    db.session.commit()

#Lista usuario ALL
def _list_GET_All():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()
    
    return [
        {
            'id': post.id,
            'title': post.title,
            'body': post.body,
            'created': post.created,
            'author_id': post.author_id,
            
        }
        for post in posts
    ]
    


@app.route("/", methods = ['GET', 'POST'])
#Verifica se a request é POST ou GET
def handle_post():
    if request.method == "POST":
        _created_Post()
        return {"Post message": []}
    else:
        return {'Posts':_list_GET_All()},HTTPStatus.CREATED

# Get user filter
@app.route("/<int:post_id>")
def get_user(post_id):
    post = db.get_or_404(Post, post_id)
    return{
            'id': post.id,
            'title': post.title,
            'body': post.body,
            'created': post.created,
            'author_id': post.author_id,
            }

# update
@app.route("/<int:post_id>", methods = ['PATCH'])
def update_post (post_id):
    post = db.get_or_404(Post, post_id)
    data = request.json
    mapper = inspect(Post)
    
    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])
    db.session.commit()
    return{
            'id': post.id,
            'title': post.title,
            'body': post.body,
            'created': post.created,
            'author_id': post.author_id,
            }

@app.route("/<int:post_id>", methods = ['DELETE'])
def delete_post (post_id):
    post = db.get_or_404(Post, post_id)  
    db.session.delete(post)
    db.session.commit()
    return "[]", HTTPStatus.NO_CONTENT
 