#!/usr/bin/env python3
import json


def estimate_price(mileage, theta0, theta1):
	"""Calcule le prix estimé selon le modèle linéaire."""
	return theta0 + (theta1 * mileage)


def load_model_params():
	"""Charge les paramètres du modèle depuis le fichier JSON."""
	try:
		with open("model_params.json", "r") as f:
			params = json.load(f)
		return params
	except FileNotFoundError:
		print("Erreur: Fichier de paramètres non trouvé. Veuillez d'abord entraîner le modèle.")
		return None
	except Exception as e:
		print(f"Erreur lors du chargement des paramètres: {e}")
		return None


def predict():
	"""Programme principal de prédiction."""
	params = load_model_params()
	if not params:
		theta0 = 0
		theta1 = 0
	else:
		theta0 = params["theta0"]
		theta1 = params["theta1"]

	try:
		mileage = float(input("Entrez le kilométrage de la voiture: "))
		price = estimate_price(mileage, theta0, theta1)
		print(f"Prix estimé pour un kilométrage de {mileage} km: {price:.2f}")
	except ValueError:
		print("Erreur: Veuillez entrer un nombre valide.")


if __name__ == "__main__":
	predict()
