from flask import Blueprint, render_template, jsonify, abort, make_response, request
import models

routes = Blueprint('routes', __name__)

@routes.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@routes.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@routes.route('/')
def index():
    movies_list = models.Movie.query.all()
    genres_list = models.Genre.query.all()
    return render_template('index.html', movies_list=movies_list, genres_list=genres_list)

@routes.route('/movies/<string:id>/', methods=['GET'])
def get_movie(id):
    movie = models.Movie.query.get(id)
    if not movie:
        print(f"No such movie at id {id}!")
        abort(404)
    
    return jsonify(movie=movie.serialize())

@routes.route('/movie/', methods=['GET'])
def get_movie_form():
    return render_template('create_movie_page.html')

@routes.route('/movie/', methods=['POST'])
def create_movie():
    if not request.json:
        abort(400)
    
    # validate user input
    assert request.json['name']
    assert request.json['major_genre']

    # TODO: sanitize user input
    movie_name = request.json.get('name', '')
    movie_major_genre = request.json.get('major_genre', '')

    new_movie = models.Movie(name=movie_name, major_genre_id=movie_major_genre)
    new_movie.save()

    return jsonify(movie=new_movie.serialize(), status=201)


@routes.route('/genre/', methods=['GET'])
def get_genre_form():
    return render_template('create_genre_page.html')

@routes.route('/genres/', methods=['GET'])
def get_genres():
    genres_list = models.Genre.query.all()
    return jsonify(genres=[ genre.serialize() for genre in genres_list ], status=201)

@routes.route('/genres/<string:id>/', methods=['GET'])
def get_genre(id):
    genre = models.Genre.query.get(id)
    if not genre:
        print(f"No such genres at id {id}!")
        abort(404)
    
    return jsonify(genre=genre.serialize())

@routes.route('/genre/', methods=['POST'])
def create_genre():
    if not request.json:
        abort(400)
    
    # validate user input
    assert request.json['name']

    # TODO: sanitize user input
    genre_name = request.json.get('name', '')

    new_genre = models.Genre(name=genre_name)
    new_genre.save()

    return jsonify(genre=new_genre.serialize(), status=201)

