# Makefile for Linear Regression Project

PYTHON = python3
TRAIN_SCRIPT = train.py
PREDICT_SCRIPT = predict.py
EVALUATE_SCRIPT = evaluate.py
UTILS = utils.py
DATA = data.csv
MODEL = model_params.json
REQUIREMENTS = requirements.txt

TRAIN_SOURCES = $(TRAIN_SCRIPT) $(UTILS) $(DATA)

.PHONY: all train predict evaluate run clean help install fclean re

all: help

install:
	@if [ -f $(REQUIREMENTS) ]; then \
		echo "Installing Python dependencies..."; \
		$(PYTHON) -m pip install -r $(REQUIREMENTS); \
	else \
		echo "No requirements.txt found. Ensuring basic dependencies..."; \
		$(PYTHON) -c "import numpy, matplotlib" 2>/dev/null || \
		$(PYTHON) -m pip install numpy matplotlib; \
	fi

$(MODEL): $(TRAIN_SOURCES)
	@echo "Training model..."
	$(PYTHON) $(TRAIN_SCRIPT)

train: $(MODEL)

predict: $(MODEL)
	@echo "Starting prediction program..."
	$(PYTHON) $(PREDICT_SCRIPT)

evaluate: $(MODEL)
	@echo "Evaluating model accuracy..."
	$(PYTHON) $(EVALUATE_SCRIPT)

run: train
	@echo "Running prediction..."
	@echo "42000" | $(PYTHON) $(PREDICT_SCRIPT) || true
	@echo ""
	@echo "Running evaluation..."
	@$(PYTHON) $(EVALUATE_SCRIPT)

test: $(MODEL)
	@echo "Testing model with sample inputs..."
	@echo "50000" | $(PYTHON) $(PREDICT_SCRIPT)
	@echo "100000" | $(PYTHON) $(PREDICT_SCRIPT)
	@echo "200000" | $(PYTHON) $(PREDICT_SCRIPT)

clean:
	@echo "Cleaning generated files..."
	rm -f $(MODEL)
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

fclean: clean
	@echo "Full clean..."
	rm -f *.png *.jpg *.pdf
	rm -rf .pytest_cache/ .coverage htmlcov/

re: fclean train

check:
	@echo "Checking project files..."
	@for file in $(TRAIN_SCRIPT) $(PREDICT_SCRIPT) $(EVALUATE_SCRIPT) $(UTILS) $(DATA); do \
		if [ ! -f $$file ]; then \
			echo "ERROR: Missing file: $$file"; \
			exit 1; \
		else \
			echo "✓ $$file"; \
		fi; \
	done
	@echo "All required files present."

help:
	@echo "Linear Regression Project Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  make install   - Install Python dependencies"
	@echo "  make train     - Train the linear regression model"
	@echo "  make predict   - Run prediction program (interactive)"
	@echo "  make evaluate  - Evaluate model accuracy with metrics"
	@echo "  make run       - Full pipeline: train + predict + evaluate"
	@echo "  make test      - Test model with sample inputs"
	@echo "  make check     - Verify all required files exist"
	@echo "  make clean     - Remove generated files (model, cache)"
	@echo "  make fclean    - Full clean (including plots)"
	@echo "  make re        - Rebuild from scratch (fclean + train)"
	@echo "  make help      - Show this help message"
	@echo ""