from flask import Flask, render_template, request, jsonify, redirect, url_for
import random
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img'
number_to_guess = random.randint(1, 100)
guess_history = []

movies = [
    {'name': 'Inception', 'director': 'Christopher Nolan', 'year': 2010, 'comment': 'hahahahaha', 'poster': 'inception.jpg'},
    {'name': 'Alien', 'director': 'Christopher Nolan', 'year': 2008, 'comment': 'hahaffffffffffffffhahaha', 'poster': 'alien.jpg'},
    {'name': 'driver', 'director': 'Christopher Nolan', 'year': 2010, 'comment': 'Pas encore vue', 'poster': 'driver.jpg'},
    {'name': 'Shining', 'director': 'Stanley Kubrick', 'year': 1980, 'comment': 'Tres bon film', 'poster': 'shining.jpg'},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    global number_to_guess
    data = request.get_json()
    guess = int(data['guess'])
    print(f"User a rentre : {guess}") 
    if guess < number_to_guess:
        message = "C'est plus"
    elif guess > number_to_guess:
        message = "C'est moins"
    else:
        message = "C'est gagné!"
        number_to_guess = random.randint(1, 100)  # Reset the number after a correct guess
        guess_history.clear()  # Clear the guess history after a correct guess
    return jsonify(message=message)

@app.route('/movies', methods=['GET'])
def visuALL():
    return render_template('movies.html', movies=movies)

@app.route('/view/<int:id>', methods=['GET'])
def visuId(id):
    if id < len(movies):
        return render_template('view_movie.html', movie=movies[id])
    else:
        return "Movie not found", 404

@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        name = request.form['name']
        director = request.form['director']
        year = request.form['year']
        comment = request.form['comment']
        poster = request.files['poster']
        
        if poster:
            poster_filename = poster.filename
            poster.save(os.path.join(app.config['UPLOAD_FOLDER'], poster_filename))
        else:
            poster_filename = 'default.jpg'  # Default image if no poster is uploaded

        new_movie = {
            'name': name,
            'director': director,
            'year': year,
            'comment': comment,
            'poster': poster_filename
        }
        movies.append(new_movie)
        return redirect('/movies')
    return render_template('add_movie.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_movie(id):
    if id >= len(movies):
        return "Movie not found", 404
    if request.method == 'POST':
        movies[id]['name'] = request.form['name']
        movies[id]['director'] = request.form['director']
        movies[id]['year'] = request.form['year']
        movies[id]['comment'] = request.form['comment']
        poster = request.files['poster']
        
        if poster:
            poster_filename = poster.filename
            poster.save(os.path.join(app.config['UPLOAD_FOLDER'], poster_filename))
            movies[id]['poster'] = poster_filename

        return redirect('/movies')
    return render_template('update_movie.html', movie=movies[id])

@app.route('/delete/<int:id>', methods=['POST'])
def delete_movie(id):
    if id < len(movies):
        del movies[id]
        return redirect('/movies')
    else:
        return "Movie not found", 404

if __name__ == '__main__':
    app.run(debug=True)