#!/usr/bin/env python3
import csv
import json


def estimate_price(mileage, theta0, theta1):
    """Calcule le prix estimé selon le modèle linéaire."""
    return theta0 + (theta1 * mileage)


def mean(values):
    """Calcule la moyenne d'une liste de valeurs."""
    return sum(values) / len(values)


def load_model_params():
    """Charge les paramètres du modèle depuis le fichier JSON."""
    try:
        with open("model_params.json", "r") as f:
            params = json.load(f)
        return params
    except FileNotFoundError:
        print("Erreur: Fichier de paramètres non trouvé. Veuillez d'abord entraîner le modèle.")
        return None


def evaluate_model(data_file):
    """Évalue la précision du modèle sur les données."""
    params = load_model_params()
    if not params:
        return

    theta0 = params["theta0"]
    theta1 = params["theta1"]

    try:
        mileage = []
        price = []

        with open(data_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                mileage.append(float(row["km"]))
                price.append(float(row["price"]))
    except Exception as e:
        print(f"Erreur lors du chargement des données: {e}")
        return

    # Faire des prédictions
    predictions = [estimate_price(x, theta0, theta1) for x in mileage]

    # Calculer l'erreur quadratique moyenne (MSE)
    errors = [predictions[i] - price[i] for i in range(len(price))]
    squared_errors = [e**2 for e in errors]
    mse = sum(squared_errors) / len(squared_errors)

    # Calculer le coefficient de détermination (R²)
    mean_price = mean(price)
    ss_total = sum((p - mean_price) ** 2 for p in price)
    ss_residual = sum(squared_errors)
    r_squared = 1 - (ss_residual / ss_total) if ss_total != 0 else 0

    print(f"Erreur quadratique moyenne (MSE): {mse:.2f}")
    print(f"Coefficient de détermination (R²): {r_squared:.4f}")
    print(f"Plus R² est proche de 1, meilleur est le modèle.")


if __name__ == "__main__":
    data_file = "data.csv"
    evaluate_model(data_file)
