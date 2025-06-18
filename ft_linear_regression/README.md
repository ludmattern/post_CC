# Linear Regression - Car Price Prediction

A complete linear regression implementation from scratch using gradient descent to predict car prices based on mileage. This project implements the mathematical formula `estimatePrice(mileage) = θ₀ + (θ₁ × mileage)` without using machine learning libraries like scikit-learn.

## Overview

This project predicts car prices based on their mileage using a linear regression model trained with gradient descent. The implementation includes automatic hyperparameter optimization, comprehensive evaluation metrics, and beautiful visualizations.

## Features

### Core Functionality

- **Pure Python Implementation**: No ML libraries (scikit-learn, etc.) - built from scratch
- **Gradient Descent Training**: Mathematical implementation with automatic convergence detection
- **Data Normalization**: Custom scaler for numerical stability during training
- **Hyperparameter Optimization**: Automatic learning rate selection via grid search
- **Model Persistence**: Save/load trained parameters in JSON format

### Advanced Features

- **Comprehensive Metrics**: R², MSE, RMSE, MAE, MAPE with visual analysis
- **Interactive Prediction**: Command-line interface for real-time price estimates  
- **Rich Visualizations**: Training convergence, residual analysis, error distribution
- **Robust Error Handling**: Validation for edge cases and invalid inputs
- **Professional Logging**: Colored console output with configurable levels

### Mathematical Accuracy

- **Numerical Stability**: Gradient clipping to prevent divergence
- **Convergence Detection**: Automatic stopping when optimal solution is reached
- **Parameter Denormalization**: Accurate conversion back to original scale
- **Mathematical Validation**: Input validation and overflow protection

## Quick Start

### Prerequisites

- Python 3.8+
- numpy >= 2.2.6
- matplotlib >= 3.10.3

### Installation

```bash
# Clone or download the project
cd ft_linear_regression

# Install dependencies
make install
# OR manually: pip install -r requirements.txt
```

### Basic Usage

```bash
# Train the model (automatic hyperparameter optimization)
make train

# Make predictions interactively
make predict

# Evaluate model performance with visualizations
make evaluate

# Run complete pipeline (train + predict + evaluate)
make run
```

## Detailed Usage

### 1. Training (`train.py`)

Trains a linear regression model with automatic hyperparameter optimization:

```bash
python3 train.py
```

**What it does:**

- Loads training data from `data.csv`
- Automatically finds optimal learning rate (0.001 to 0.5 range)
- Trains model using gradient descent with convergence detection
- Saves parameters to `model_params.json`
- Displays training visualizations (regression line, cost convergence, parameter evolution)

**Output:**

- Model parameters: θ₀ (intercept) and θ₁ (slope)
- Training convergence plots
- Saved model file for predictions

### 2. Prediction (`predict.py`)

Interactive price prediction for any car mileage:

```bash
python3 predict.py
```

**Example session:**

```
Enter the car's mileage (in km): 120000
Estimated price for 120000 km: 5925.75 units
```

**Features:**

- Input validation (no negative mileage)
- Graceful error handling
- Works with or without trained model (defaults to 0 if no model found)

### 3. Evaluation (`evaluate.py`)

Comprehensive model analysis with metrics and visualizations:

```bash
python3 evaluate.py
```

**Provides:**

- **Performance Metrics**: R², MSE, RMSE, MAE, MAPE
- **Visual Analysis**:
  - Predictions vs Actual scatter plot
  - Residuals analysis
  - Error distribution histogram
  - Performance metrics bar chart
  - Model quality pie chart
  - Detailed metrics table
- **Summary Report**: Model accuracy, example predictions, improvement suggestions

## Data Format

The training data should be in CSV format with headers:

```csv
km,price
240000,3650
139800,3800
150500,4400
...
```

- **km**: Car mileage in kilometers (positive values only)
- **price**: Car price in currency units (positive values only)

## Mathematical Details

### Linear Regression Formula

```
estimatePrice(mileage) = θ₀ + (θ₁ × mileage)
```

Where:

- **θ₀**: Intercept (base price when mileage = 0)
- **θ₁**: Slope (price change per kilometer)

### Gradient Descent Implementation

The model uses the standard gradient descent formulas:

```
θ₀ := θ₀ - α × (1/m) × Σ(h(x) - y)
θ₁ := θ₁ - α × (1/m) × Σ((h(x) - y) × x)
```

Where:

- **α**: Learning rate (automatically optimized)
- **m**: Number of training samples
- **h(x)**: Hypothesis function (θ₀ + θ₁ × x)
- **Cost Function**: J(θ) = (1/2m) × Σ(h(x) - y)²

### Key Features

- **Data Normalization**: Prevents numerical instability
- **Gradient Clipping**: Avoids parameter explosion
- **Convergence Detection**: Stops when improvement < 1e-6
- **Hyperparameter Grid Search**: Tests learning rates [0.001, 0.01, 0.05, 0.1, 0.2, 0.5]

## Performance Metrics

The evaluation provides comprehensive metrics:

| Metric | Description | Good Value |
|--------|-------------|------------|
| **R²** | Coefficient of determination (variance explained) | > 0.8 |
| **MSE** | Mean Squared Error | Lower is better |
| **RMSE** | Root Mean Squared Error (typical error) | < 10% of mean price |
| **MAE** | Mean Absolute Error (average error) | < 5% of mean price |
| **MAPE** | Mean Absolute Percentage Error | < 15% |

### Quality Assessment

- **Excellent**: R² > 0.9
- **Good**: R² > 0.7
- **Fair**: R² > 0.5
- **Poor**: R² ≤ 0.5

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make install` | Install Python dependencies |
| `make train` | Train the linear regression model |
| `make predict` | Interactive prediction interface |
| `make evaluate` | Model evaluation with visualizations |
| `make run` | Complete pipeline (train + predict + evaluate) |
| `make test` | Test model with sample inputs |
| `make clean` | Remove generated files |
| `make fclean` | Full clean (including plots) |
| `make re` | Rebuild from scratch |
| `make check` | Verify all required files exist |

## Project Structure

```
ft_linear_regression/
├── train.py              # Model training with optimization
├── predict.py             # Interactive price prediction
├── evaluate.py            # Model evaluation and metrics
├── utils.py               # Shared utility functions
├── logging_config.py      # Logging configuration
├── data.csv               # Training dataset (24 samples)
├── model_params.json      # Trained model parameters
├── requirements.txt       # Python dependencies
├── Makefile              # Build automation
└── README.md             # This file
```

## Visualizations

The project generates several types of visualizations:

### Training Visualizations (`train.py`)

1. **Regression Line**: Scatter plot with fitted line
2. **Cost Convergence**: Cost function over iterations (log scale)
3. **Parameter Evolution**: How θ₀ and θ₁ change during training

### Evaluation Visualizations (`evaluate.py`)

1. **Predictions vs Actual**: Scatter plot showing prediction accuracy
2. **Residuals Analysis**: Error distribution across predictions
3. **Error Histogram**: Distribution of prediction errors
4. **Performance Metrics**: Bar chart of key metrics
5. **Model Quality**: Pie chart of explained vs unexplained variance
6. **Metrics Table**: Detailed breakdown with interpretations

## Error Handling

The implementation includes robust error handling:

- **Data Validation**: Checks for negative mileage/prices
- **File Handling**: Graceful handling of missing files
- **Numerical Stability**: Gradient clipping and overflow detection
- **Input Validation**: User input sanitization
- **Convergence Issues**: Detection and reporting of training problems

## Advanced Configuration

### Logging Levels

The logging system supports different levels:

- **DEBUG**: Detailed technical information
- **INFO**: General progress updates  
- **WARNING**: Potential issues
- **ERROR**: Error conditions

### Model Parameters

Key parameters can be adjusted in the code:

- **Learning rates**: [0.001, 0.01, 0.05, 0.1, 0.2, 0.5]
- **Max iterations**: 1000 (with early stopping)
- **Convergence tolerance**: 1e-6
- **Gradient clipping**: ±1e6

## Example Results

With the provided dataset (24 car samples):

```
MODEL EVALUATION SUMMARY
* Model accuracy: Good (R² = 0.812)
* Average error: ±412 price units  
* Relative error: 7.1% on average

PREDICTION EXAMPLES:
   • 50,000 km → 7,427 price units
   • 100,000 km → 6,355 price units
   • 150,000 km → 5,282 price units
   • 200,000 km → 4,210 price units

FORMULA: price = 8499 + (-0.021444 × mileage)

* This model provides reasonable estimates
```

## Educational Value

This project demonstrates:

- **Mathematical Implementation**: Pure gradient descent without ML libraries
- **Software Engineering**: Clean code, error handling, logging, testing
- **Data Science Pipeline**: Training, validation, prediction, evaluation
- **Visualization**: Professional plots and metrics presentation
- **Documentation**: Comprehensive README and code comments

Perfect for understanding the fundamentals of machine learning before using high-level libraries!
