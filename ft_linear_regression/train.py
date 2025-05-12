#!/usr/bin/env python3
import csv
import json
import matplotlib.pyplot as plt

# Paramètres d'apprentissage
learning_rate = 0.1
n_iterations = 100000

def estimate_price(mileage, theta0, theta1):
	"""Calcule le prix estimé selon le modèle linéaire."""
	return theta0 + (theta1 * mileage)

def mean(values):
    """Calcule la moyenne d'une liste de valeurs."""
    if not values:
        return 0
    return sum(values) / len(values)

def std_dev(values):
    """Calcule l'écart type d'une liste de valeurs."""
    if not values:
        return 1
    m = mean(values)
    variance = sum((x - m) ** 2 for x in values) / len(values)
    return max(variance ** 0.5, 1e-10)

def train_model(data_file):
	"""Entraîne un modèle de régression linéaire sur les données."""
	# Charger les données
	mileage = []
	price = []
	
	try:
		with open(data_file, 'r') as f:
			reader = csv.DictReader(f)
			for row in reader:
				mileage.append(float(row['km']))
				price.append(float(row['price']))
	except Exception as e:
		print(f"Erreur lors du chargement des données: {e}")
		return None, None

	# Vérifier si les données sont suffisantes
	if len(mileage) < 2:
		print("Erreur: Pas assez de données pour l'entraînement.")
		return None, None
	# Vérifier si les données sont valides
	if len(mileage) != len(price):
		print("Erreur: Les données de kilométrage et de prix ne correspondent pas.")
		return None, None
	
	# Veritifer si il y a au moins 2 paires de valeurs différentes
	if len(set(mileage)) < 2 or len(set(price)) < 2:
		print("Erreur: Les données de kilométrage ou de prix ne contiennent pas assez de variations.")
		return None, None
 
	print(f"Données chargées : {len(mileage)} échantillons")
 
	# Normalisation des données
	mileage_mean = mean(mileage)
	mileage_std = std_dev(mileage)
	mileage_normalized = [(x - mileage_mean) / mileage_std for x in mileage]
	
	# Initialisation des paramètres
	theta0 = 0
	theta1 = 0
	m = len(mileage)  # Nombre d'échantillons
	
	# Historique pour visualisation
	cost_history = []
	
	# Descente de gradient
	print("Début de l'entraînement...")
	for i in range(n_iterations):
		# Calculer les prédictions et les erreurs
		predictions = [estimate_price(x, theta0, theta1) for x in mileage_normalized]
		errors = [predictions[j] - price[j] for j in range(m)]
		
		# Calculer les gradients temporaires
		tmp_theta0 = learning_rate * (1/m) * sum(errors)
		tmp_theta1 = learning_rate * (1/m) * sum(errors[j] * mileage_normalized[j] for j in range(m))
		
		# Mettre à jour les paramètres simultanément
		theta0 -= tmp_theta0
		theta1 -= tmp_theta1
		
		
		# Calculer la fonction de coût (MSE)
		cost = (1/(2*m)) * sum(e**2 for e in errors)
		
		# Calculer le cout previsionnel
		if i > 0:
			previous_cost = cost_history[-1] if cost_history else float('inf')

		# Vérifier la divergence
		if i > 0 and cost > previous_cost:
			print(f"Erreur: Divergence détectée à l'itération {i}, coût: {cost}")
			theta0 = 0
			theta1 = 0
			break
  
		if i > 0 and abs(cost - previous_cost) < 1e-6:
			print(f"Convergence atteinte à l'itération {i}")
			break
		
		cost_history.append(cost)
		
		# Afficher la progression
		if i % 100 == 0:
			print(f"Itération {i}, Coût: {cost}")
	
	# Dé-normalisation pour obtenir les vrais paramètres
	theta1_denorm = theta1 / mileage_std
	theta0_denorm = theta0 - theta1_denorm * mileage_mean
	
	# Sauvegarder les paramètres
	params = {
		'theta0': theta0_denorm,
		'theta1': theta1_denorm
	}
	
	with open('model_params.json', 'w') as f:
		json.dump(params, f)
	
	print(f"Entraînement terminé - Thêta0: {theta0_denorm}, Thêta1: {theta1_denorm}")
	
	# Visualiser les données et la régression
	plt.figure(figsize=(10, 6))
	plt.scatter(mileage, price, color='blue', label='Données')
	
	# Générer les points pour la ligne de régression
	min_mileage = min(mileage)
	max_mileage = max(mileage)
	line_x = [min_mileage, max_mileage]
	line_y = [estimate_price(x, theta0_denorm, theta1_denorm) for x in line_x]
	
	plt.plot(line_x, line_y, color='red', label='Régression')
	plt.xlabel('Kilométrage')
	plt.ylabel('Prix')
	plt.title('Régression linéaire: Prix vs Kilométrage')
	plt.legend()
	plt.savefig('regression_plot.png')
	plt.show()
	
	return theta0_denorm, theta1_denorm

if __name__ == "__main__":
	data_file = "data.csv"
	# Vérifier si le fichier de données existe
	try:
		with open(data_file, 'r') as f:
			pass
	except FileNotFoundError:
		print(f"Erreur: Le fichier {data_file} n'existe pas.")
		exit(1)
	train_model(data_file)