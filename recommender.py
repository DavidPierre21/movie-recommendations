
from math import sqrt
from movielib import *

# --- Parametros

k = 50
theuser = 6041

# --- Distancias
def media(numbers, n = 2):
    return (sum(numbers) + (3.0 * n)) / float(len(numbers) + n)

def euclidiana(rating1, rating2, r = 2):
    """
    Verifica a distancia das avaliacoes dos filmes
    utilizando a distancia euclidiana(Ou minkowski com raiz quadrada)
    """
    
    distance = 0
    commonRatings = False
    for chave in rating1:
        if chave in rating2:
            distance += pow(abs(rating1[chave] - rating2[chave]), r)
            commonRatings = True
    if commonRatings: #se possuir alguma avaliacao em comum
        return pow(float(distance),  1/r)
    else:
        return 1000000 #Quando o usuario nao tem avaliacoes em comum

distance = euclidiana
    
# --- Carrega as avaliacoes dos usuarios
users = {} # userid -> {movie : rating, movie : rating, ...}
for (user, movie, rating, time) in get_data():
    user = int(user)
    movie = int(movie)
    
    ratings = users.get(user)
    if not ratings:
        ratings = {}
        users[user] = ratings

    ratings[movie] = int(rating)

# --- Encontra os k vizinhos mais proximos
neighbours = []
theratings = users[theuser]
for (user, ratings) in users.items():
    if user == theuser:
        continue

    neighbours.append((distance(theratings, ratings), user, ratings))

neighbours.sort()
neighbours = neighbours[ : k]

# --- Carrega os filmes
movies = {}
for row in get_movies():
    movie = int(row[0])
    title = row[1]
    movies[movie] = title

# --- Verifica similarididade com os vizinhos
neigh_ratings = {} # movie -> [r1, r2, r3]
for index in range(k):
    (dist, user, ratings) = neighbours[index]
    
    print "===== %s ==================================================" % index
    print "Vizinho #", user, ", distancia:", dist
    
    for (movie, rating) in ratings.items():
        common = ''
        if theratings.has_key(movie):
            common = '   Usuario: %s' % theratings[movie]
        if common:
            print movies[movie], rating, common

        rs = neigh_ratings.get(movie)
        if not rs:
            rs = []
            neigh_ratings[movie] = rs
        rs.append(rating)

# --- Pega as maiores medias
medias = [(media(ratings), movie) for (movie, ratings) in neigh_ratings.items()]
medias.sort()
medias.reverse()

print "===== Filmes recomendados ======================================================"
count = 0
for (average, movie) in medias:
    if movie in theratings:
        continue

    print movies[movie], average
    count += 1
    if count > 10:
        break

print "===== Filmes nao-recomendados ================================================="
count = 0
medias.reverse()
for (average, movie) in medias:
    if movie in theratings:
        continue

    print movies[movie], average
    count += 1
    if count > 10:
        break
