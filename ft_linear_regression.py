import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import json

dict: dict

km: list[int] = []
price: list[int] = []

with open('data.csv', newline='', encoding='utf-8') as data_csv:
	lecteur: csv.DictReader = csv.DictReader(data_csv)
	for l in lecteur:
		km.append(int(l['km']))
		price.append(int(l['price']))

# normalisation des valeurs de km car grandes (pas besoin de normaliser price car y, pas utilise dans les calculs)
km: np.array = np.array(km)
# Va creer une nouvelle liste ou chaque valeure va etre normalisee pour etre entre 0 et 1
rangeKm: int = (np.max(km) - np.min(km))
km_normalized: np.array = (km - np.min(km)) / rangeKm

# Definition de teta0 et teta1 (respectivement b et a)
theta0: float = 0
theta1: float = 0

# Fonction qui calcul le cout par rapport au killometrage
def estimatePrice(mileage: int) -> int: # mileage = x
    return (theta0 + (theta1 * mileage)) # = ax + b

"""
fonction cout:
J(a,b) = (1 / 2m) * Somme de i=0 a m-1(a*xi + b - yi)²

axi + b - yi correspond pour la ligne i et les paramettre a et b actuel
a la difference entre la valeure que donne notre prediction avec a et b,
moins la vraie valeure yi, ce qui correspond a l'erreure.

On met cela au carre pour ne pas avoir de valeure negative.

La somme de i=0 a m correspond a la somme des erreures pour chaques lignes.

Puis le total / 2m fait une moyenne de l'erreure (le 2 sert simplement a simplifier la notation par la suite
et n'a pas d'influence sur le calcul final)

Selon les variables du sujet:

J(theta1, theta0) = (1 / 2m) * Somme de i=0 a m-1 (estimatePrice(mileage[i]) - price[i])²

Pour obtenir les deux formules du sujet, on va deriver J par rapport a a(teth1)
puis par rapport a b(teth0) pour pouvoir apres faire une descente de gradient sur 
J(a,b) et trouver pour quelles a et b le cout est minimal

La derivee par raport a a donne:
(1 / m) * Somme de i=0 a m-1 (estimatePrice(mlieage[i]) - price[i]) * mlieage[i]

car on a :
(1 / 2m) * Somme de i=0 a m-1 * f**2 avec f = teth1*mileage[i] + teth0
et on a:
f(x)² = 2*f(x)+f'(x)
puisque l'on derive par rapport a a(teth1) -> f(teth1) = mileage[i] * teth1 + teth0
derivee -> mileage[i]
(comme ax + b deviendrait x)

ce qui donne 2(teth1 * mileage[i] + teth0) *  mileage[i]
Donc: 
(1 / 2m) * Somme de i=0 a m-1 2(estimatePrice(mlieage[i]) - price[i]) * mlieage[i]
<=> (1 / m) * Somme de i=0 a m-1 (estimatePrice(mlieage[i]) - price[i]) * mlieage[i]

De meme pour b:
(f(teth0) = teth1*mileage[i] + teth0 -> f'(teth0) = 1 (comme f(x) = b + x -> f'(x) = 1))

Donc:
(1 / 2m) * Somme de i=0 a m-1 2(estimatePrice(mlieage[i]) - price[i]) * 1 
<=> (1 / m) * Somme de i=0 a m-1 (estimatePrice(mlieage[i]) - price[i])

Les formules du sujet ajoutent learningRate * au debut qui correspond a alpha dans la descente gradiente, qui est la vitesse d'apprentissage / de deplacement dans la fonction

"""

isTheta0Opti: bool = False
isTheta1Opti: bool = False

def gradientDescentStepTetha1(learningRate: float) -> float :
    global isTheta1Opti
    m: int = len(km_normalized)
    somme: int = 0
    for i in range(0, m):
        somme += (estimatePrice(km_normalized[i]) - price[i]) * km_normalized[i]
    result:int = learningRate * (1 / m) * somme
    if abs(result) < 0.1 :
        isTheta1Opti = True
    return result

def gradientDescentStepTetha0(learningRate: float) -> float :
    global isTheta0Opti
    m: int = len(km_normalized)
    somme: int = 0
    for i in range(0, m):
        somme += (estimatePrice(km_normalized[i]) - price[i])
    result: int = learningRate * (1 / m) * somme
    if abs(result) < 0.1 :
        isTheta0Opti = True
    return result

thetaHistory: list[(float, float)] = [(theta0, theta1)]

def saveValues():
	global rangeKm, km
	parameters = {"theta0": float(theta0), "theta1": float(theta1), "min": float(np.min(km)), "rangeKm": float(rangeKm)}
	with open('values.json', 'w') as f:
		json.dump(parameters, f)

def gradientDescentStep() :
    global theta1, theta0, isTheta0Opti, isTheta1Opti
    learningRate: float = 1.3
    tmpTheta0: float = theta0
    tmpTheta1: float = theta1
    tmpTheta0 -= gradientDescentStepTetha0(learningRate)
    tmpTheta1 -= gradientDescentStepTetha1(learningRate)
    theta0 = tmpTheta0
    theta1 = tmpTheta1

while 1:
	thetaHistory.append((theta0, theta1))
	gradientDescentStep()
	if (isTheta0Opti & isTheta1Opti) :
		print("Optimal value: theta1(a):", theta1, " | theta0(b): ", theta0)
		thetaHistory.append((theta0, theta1))
		saveValues()
		break

y_line: list[int] = theta1 * km_normalized + theta0

fig, ax = plt.subplots()
line, = ax.plot(km, y_line, color='red', label=f'Droite de régression: y = {theta1}x + {theta0}')
plt.scatter(km, price)
plt.xlabel('Km')
plt.ylabel('Prices')
plt.title('Nuage de points')

# Fonction de mise à jour pour l'animation
def update(frame):
    theta0, theta1 = thetaHistory[frame]
    y_line = theta1 * km_normalized + theta0
    line.set_ydata(y_line)  # Mettre à jour les données de la droite
    ax.set_title(f'Progression de la régression linéaire')
    return line,

# Création de l'animation
ani = FuncAnimation(fig, update, frames=range(0, len(thetaHistory), 1), interval=100, blit=True)

plt.show()
