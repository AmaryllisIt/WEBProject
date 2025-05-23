import flask

from . import db_session
from .news import News

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@blueprint.route('/api/news')
def get_news():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    return flask.jsonify(
        {
            'news':
                [item.to_dict(only=('title', 'content', 'user.name'))
                 for item in news]
        }
    )


@blueprint.route('/api/news/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(news_id)
    if not news:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
    return flask.jsonify(
        {
            'news': news.to_dict(only=(
                'title', 'content', 'user_id', 'is_private'))
        }
    )


@blueprint.route('/api/news', methods=['POST'])
def create_news():
    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)
    elif not all(key in flask.request.json for key in
                 ['title', 'content', 'user_id', 'is_private']):
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    news = News(
        title=flask.request.json['title'],
        content=flask.request.json['content'],
        user_id=flask.request.json['user_id'],
        is_private=flask.request.json['is_private']
    )
    db_sess.add(news)
    db_sess.commit()
    return flask.jsonify({'id': news.id})

@blueprint.route('/api/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(news_id)
    if not news:
        return flask.make_response(flask.jsonify({'error': 'Cannot delete'}), 404)
    db_sess.delete(news)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})