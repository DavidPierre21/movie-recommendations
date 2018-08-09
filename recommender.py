from math import sqrt
from movielib import *

# --- Parametros

k = 50
theuser = 6041

# --- Distancias
def media(numbers, n = 2):
    return (sum(numbers) + (3.0 * n)) / float(len(numbers) + n)

def minkowski(rating1, rating2, r = 2):  #Minkowski / Manhattan / Euclidiana ---- Basta modificar o valor de r 
    """
    Verifica a distancia das avaliacoes dos filmes
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



def pearson(rating1, rating2): # Coeficiente de correlacao de Pearson
    soma_xy = 0
    soma_x = 0
    soma_y = 0
    soma_x2 = 0
    soma_y2 = 0
    n = 0
    for key in rating1:
        if key in rating2:
            n += 1
            x = rating1[key]
            y = rating2[key]
            soma_xy += x * y
            soma_x += x
            soma_y += y
            soma_x2 += x ** 2
            soma_y2 += y ** 2
            
    # para calcular o denominador
    if n == 0:
        return 1000000
    denominador = (sqrt(soma_x2 - (soma_x**2) / n) *
                  sqrt(soma_y2 -(soma_y**2) / n))
    if denominador == 0:
        return 100000000
    else:
        sim = (soma_xy - (soma_x * soma_y) / n) / denominador
        return 1.0 - sim


def lmg_rmse(rating1, rating2): #erro quadratico medio (root mean square error)
    max_rating = 5.0
    sum = 0
    count = 0
    for (key, rating) in rating1.items():
        if key in rating2:
            sum += (rating2[key] - rating) ** 2
            count += 1

    if not count:
        return 1000000 

    return sqrt(sum / float(count)) + (max_rating / count)



distance = minkowski # escolho qual tipo de distancia usar.


    
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
    print "Vizinho #", user
    
    for (movie, rating) in ratings.items():
        common = ''
        if theratings.has_key(movie):
            common = '   Usuario: %s' % theratings[movie]
        if common:
            print movies[movie], "- Nota do vizinho: ", rating, common

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
