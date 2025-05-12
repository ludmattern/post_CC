# Makefile pour le projet de régression linéaire

# Variables
PYTHON = python3
TRAIN = train.py
PREDICT = predict.py
EVALUATE = evaluate.py
DATA = data.csv
OUTPUT = model_params.json
PLOT = regression_plot.png

# Règles
.PHONY: all train predict evaluate clean

# Règle par défaut - affiche l'aide
all: help

# Entraîner le modèle
train:
	$(PYTHON) $(TRAIN)

# Faire des prédictions
predict:
	$(PYTHON) $(PREDICT)

# Évaluer la précision du modèle
evaluate:
	$(PYTHON) $(EVALUATE)

# Exécuter toutes les étapes dans l'ordre
run: train predict evaluate

# Nettoyer les fichiers générés
clean:
	rm -f $(OUTPUT) $(PLOT)

# Afficher l'aide
help:
	@echo "Utilisation du Makefile pour le projet de régression linéaire :"
	@echo ""
	@echo "  make train     - Entraîne le modèle sur les données"
	@echo "  make predict   - Fait des prédictions avec le modèle entraîné"
	@echo "  make evaluate  - Évalue la précision du modèle"
	@echo "  make run       - Exécute toutes les étapes dans l'ordre"
	@echo "  make clean     - Supprime les fichiers générés (modèle et graphique)"
	@echo "  make help      - Affiche cette aide"