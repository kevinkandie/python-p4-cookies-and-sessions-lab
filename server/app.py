#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# ------------------- SESSION CLEAR -------------------

@app.route('/clear')
def clear_session():
    session.clear()
    return {'message': '200: Successfully cleared session data.'}, 200

# ------------------- GET ALL ARTICLES -------------------

@app.route('/articles')
def index_articles():
    articles = Article.query.all()

    article_list = [{
        'id': article.id,
        'title': article.title
    } for article in articles]

    return jsonify(article_list), 200



# ------------------- GET ARTICLE BY ID -------------------

@app.route('/articles/<int:id>', methods=['GET'])

def get_article(id):
    # Increment page views (initialize to 0 if missing)
    session['page_views'] = session.get('page_views', 0) + 1

    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    article = db.session.get(Article, id)  # Updated here
    if not article:
        return jsonify({'error': 'Article not found'}), 404

    return jsonify({
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'author': article.author,
        'preview': article.preview,  
        'minutes_to_read': article.minutes_to_read, 
        'date': article.date.strftime('%B %d, %Y') if article.date else None,  
        'page_views': session['page_views']
    }), 200


# ------------------- SESSION INSPECTOR -------------------

@app.route('/sessions/<string:key>', methods=['GET'])
def show_session(key):
    # Default session values
    session['hello'] = session.get('hello', 'World')
    session['goodnight'] = session.get('goodnight', 'Moon')
    session['page_views'] = session.get('page_views', 0)

    value = session.get(key)
    if value is None:
        return jsonify({'error': f"Session key '{key}' not found."}), 404

    return jsonify({
        'session_key': key,
        'session_value': value,
        'page_views': session['page_views']
    }), 200

# ------------------- MAIN -------------------

if __name__ == '__main__':
    app.run(port=5555)
