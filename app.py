import pandas as pd
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__, static_folder='movie-recommender-app/build',
            static_url_path='/')
CORS(app)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret'

# Initialize the database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    userId = db.Column(db.Integer, unique=True, nullable=False)  # Add userId field


# Create the database
with app.app_context():
    db.create_all()

# Load datasets
content_data = pd.read_csv('spacy_processed_data_tmdb.csv')  # Dataset for content-based filtering
collaborative_data = pd.read_csv('updated_movies_rating_data_tmdb.csv')  # Dataset for collaborative filtering

# Fuction to get all the movies
def getAllMovies():
    return list(content_data['title'].str.capitalize())

# Function to create content-based recommendations
def content_based_recommendations(train_data, item_name, top_n=10):
    # Check if the item name exists in the training data
    if item_name not in train_data['title'].values:
        print(f"Movie '{item_name}' not found in the dataset.")
        return []

    # Create a TF-IDF vectorizer for item descriptions
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    # Apply TF-IDF vectorization to item descriptions
    tfidf_matrix_content = tfidf_vectorizer.fit_transform(train_data['tags'])

    # Calculate cosine similarity between items based on descriptions
    cosine_similarities_content = cosine_similarity(tfidf_matrix_content, tfidf_matrix_content)

    # Find the index of the item
    item_index = train_data[train_data['title'] == item_name].index[0]

    # Get the cosine similarity scores for the item
    similar_items = list(enumerate(cosine_similarities_content[item_index]))

    # Sort similar items by similarity score in descending order
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)

    # Get the top N most similar items (excluding the item itself)
    top_similar_items = similar_items[1:top_n+1]

    # Get the indices of the top similar items
    recommended_item_indices = [x[0] for x in top_similar_items]

    # Get the titles of the top similar items as a list
    recommended_titles = train_data.iloc[recommended_item_indices]['title'].tolist()

    return recommended_titles



# Function to create collaborative filtering recommendations
def collaborative_filtering_recommendations(train_data, target_user_id, top_n=10):
    # Create the user-item matrix
    user_item_matrix = train_data.pivot_table(index='userId', columns='movieId', values='rating', aggfunc='mean').fillna(0)

    # Calculate the user similarity matrix using cosine similarity
    user_similarity = cosine_similarity(user_item_matrix)

    # Find the index of the target user in the matrix
    target_user_index = user_item_matrix.index.get_loc(target_user_id)

    # Get the similarity scores for the target user
    user_similarities = user_similarity[target_user_index]

    # Sort the users by similarity in descending order (excluding the target user)
    similar_users_indices = user_similarities.argsort()[::-1][1:]

    # Generate recommendations based on similar users
    recommended_items = set()  # Use a set to avoid duplicate recommendations

    for user_index in similar_users_indices:
        # Get items rated by the similar user but not by the target user
        rated_by_similar_user = user_item_matrix.iloc[user_index]
        not_rated_by_target_user = (rated_by_similar_user > 0) & (user_item_matrix.iloc[target_user_index] == 0)

        # Extract the item IDs of recommended items
        recommended_items.update(user_item_matrix.columns[not_rated_by_target_user][:top_n])

        # Stop collecting recommendations once the desired number is reached
        if len(recommended_items) >= top_n:
            break

    # Get the details of recommended items
    recommended_items_details = train_data[train_data['movieId'].isin(recommended_items)][['movieId', 'title']].drop_duplicates()

    # Return the titles as a list
    recommended_titles = recommended_items_details['title'].tolist()

    return recommended_titles



# Function for hybrid recommendations
def hybrid_recommendations(movie_name, user_id, top_n=20):
    # Generate content-based recommendations
    content_recs = content_based_recommendations(content_data, movie_name)

    # Check if the user exists in the collaborative dataset
    if user_id in collaborative_data['userId'].unique():
        # Generate collaborative filtering recommendations
        collaborative_recs = collaborative_filtering_recommendations(collaborative_data, user_id)
        
        # Combine content-based and collaborative recommendations, remove duplicates
        hybrid_recs = list(set(content_recs + collaborative_recs))
    else:
        # If userId doesn't exist, fall back to content-based recommendations
        hybrid_recs = content_recs

    # Limit to the top_n recommendations
    return hybrid_recs[:top_n]



@app.route('/api/register', methods=['POST'])
@cross_origin()
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user_id = data.get('userId')  # Get userId from the request

    # Validate input
    if not username or not password or not user_id:
        return jsonify({'error': 'Username, password, and userId are required'}), 400

    # Check if username or userId already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    if User.query.filter_by(userId=user_id).first():
        return jsonify({'error': 'UserId already exists'}), 400

    # Create a new user
    new_user = User(
        username=username,
        password=bcrypt.generate_password_hash(password).decode('utf-8'),
        userId=user_id.strip()  # Strip whitespace to ensure consistency
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


@app.route('/api/login', methods=['POST'])
@cross_origin()
def login():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debugging the request payload
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if not user or not bcrypt.check_password_hash(user.password, password):
            print("Authentication failed.")  # Debugging auth failure
            return jsonify({'error': 'Invalid username or password'}), 401

        access_token = create_access_token(identity=str(user.userId))  
        print("Login successful. UserId:", user.userId)  # Debug success
        return jsonify({'access_token': access_token, 'userId': user.userId}), 200
    except Exception as e:
        print("Error during login:", e)  # Log unexpected errors
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/movies', methods=['GET'])
@cross_origin()
def movies():
    # Returns all the movies in the content dataset
    movies = getAllMovies()
    result = {"arr": movies}
    return jsonify(result)


@app.route('/api/similarity/<name>', methods=['GET', 'POST'])
@cross_origin()
@jwt_required()
def similarity(name):
    movie = name.strip().lower()
    if not movie:
        return jsonify({"msg": "Invalid movie name"}), 400

    user_identity = get_jwt_identity()
    user_id = int(user_identity)  # Convert userId back to integer if necessary

    if user_id:
        recommendations = hybrid_recommendations(movie, user_id)
    else:
        recommendations = content_based_recommendations(content_data, movie)

    if type(recommendations) == type('string'):
        resultArray = recommendations.split('---')
        apiResult = {'movies': resultArray}
        return jsonify(apiResult)
    else:
        movieString = '---'.join(recommendations)
        resultArray = movieString.split('---')
        apiResult = {'movies': resultArray}
        return jsonify(apiResult)




@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    # Get the port from the environment variable
    port = int(os.environ.get("PORT", 5000))
    # Run the app
    app.run(host='0.0.0.0', port=port)

