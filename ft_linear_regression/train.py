#!/usr/bin/env python3
"""
Linear regression with automatic hyperparameter optimization.
Implements the formula: estimatePrice(mileage) = θ₀ + (θ₁ * mileage)
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from utils import load_data
from logging_config import get_logger

# Setup logger for training module
logger = get_logger(__name__)


class ManualScaler:
    """Manual implementation of data normalization to avoid sklearn dependency."""

    def __init__(self):
        self.mean_ = None
        self.std_ = None

    def fit_transform(self, X):
        """Fit the scaler and transform the data."""
        self.mean_ = np.mean(X)
        self.std_ = np.std(X)
        if self.std_ == 0:
            self.std_ = 1
        return (X - self.mean_) / self.std_

    def inverse_transform(self, X):
        """Transform normalized data back to original scale."""
        return X * self.std_ + self.mean_


class LinearRegression:
    """Linear regression model using gradient descent with normalization."""

    def __init__(self, learning_rate=0.5, n_iterations=1000):
        """Initialize the model with hyperparameters."""
        if learning_rate <= 0:
            raise ValueError("Learning rate must be positive")
        if learning_rate > 1.0:
            logger.warning(f"High learning rate ({learning_rate}), risk of divergence")

        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.theta0 = self.theta1 = 0.0
        self.scaler_x = ManualScaler()
        self.scaler_y = ManualScaler()
        self.cost_history = []
        self.theta_history = []

    def _normalize_data(self, X, y):
        """Normalize input data using ManualScaler for numerical stability."""
        X_norm = self.scaler_x.fit_transform(X)
        y_norm = self.scaler_y.fit_transform(y)
        return X_norm, y_norm

    def _denormalize_parameters(self):
        """Convert normalized parameters back to original scale."""
        dummy_mileage = np.array([[0], [1]])
        dummy_price = np.array([[self.theta0], [self.theta0 + self.theta1]])
        original_mileage = self.scaler_x.inverse_transform(dummy_mileage)
        original_price = self.scaler_y.inverse_transform(dummy_price)
        theta1_final = (original_price[1][0] - original_price[0][0]) / (original_mileage[1][0] - original_mileage[0][0])
        theta0_final = original_price[0][0] - theta1_final * original_mileage[0][0]
        return theta0_final, theta1_final

    def predict(self, X):
        """Make predictions using current parameters (for normalized data)."""
        return self.theta0 + (self.theta1 * X)

    def fit(self, X, y, verbose=True):
        """Train the model using gradient descent with automatic convergence detection."""
        X_norm, y_norm = self._normalize_data(X, y)
        m = len(X)
        if verbose:
            logger.info(f"Training on {m} samples...")

        prev_cost, tolerance = float("inf"), 1e-6

        for i in range(self.n_iterations):
            predictions = self.predict(X_norm)
            errors = predictions - y_norm

            # Gradient descent formulas: tmp_θ = learningRate * (1/m) * Σ(errors)
            # np.mean() computes (1/m) * Σ automatically
            tmp_theta0 = self.learning_rate * np.mean(errors)
            tmp_theta1 = self.learning_rate * np.mean(errors * X_norm)
            max_gradient = 1e6
            tmp_theta0 = np.clip(tmp_theta0, -max_gradient, max_gradient)
            tmp_theta1 = np.clip(tmp_theta1, -max_gradient, max_gradient)

            self.theta0 -= tmp_theta0
            self.theta1 -= tmp_theta1

            if not (np.isfinite(self.theta0) and np.isfinite(self.theta1)):
                if verbose:
                    logger.error(f"Divergence detected - LR too high: {self.learning_rate}")
                raise ValueError("Numerical divergence")

            cost = np.mean(errors**2) / 2
            if not np.isfinite(cost):
                logger.error("Infinite cost detected during training")
                raise ValueError("Infinite cost")

            self.cost_history.append(cost)

            should_store = i == 0 or (i < 10 and i % 2 == 0) or (i < 50 and i % 5 == 0) or (i < 200 and i % 20 == 0) or (i % 50 == 0)

            if should_store:
                current_theta0, current_theta1 = self._denormalize_parameters()
                self.theta_history.append((i, current_theta0, current_theta1))

            if abs(prev_cost - cost) < tolerance:
                if verbose:
                    logger.info(f"Converged after {i + 1} iterations")
                break
            prev_cost = cost
        else:
            logger.info(f"Training completed: {self.n_iterations} iterations")

        self.theta0_final, self.theta1_final = self._denormalize_parameters()

        final_iteration = len(self.cost_history) - 1
        if not self.theta_history or self.theta_history[-1][0] != final_iteration:
            self.theta_history.append((final_iteration, self.theta0_final, self.theta1_final))

        return self

    def predict_price(self, mileage):
        """Predict price for given mileage using trained model (original scale)."""
        return self.theta0_final + (self.theta1_final * mileage)

    def save_model(self, filename="model_params.json"):
        """Save trained model parameters to JSON file."""
        params = {"theta0": float(self.theta0_final), "theta1": float(self.theta1_final)}
        with open(filename, "w") as f:
            json.dump(params, f, indent=2)
        logger.info(f"Model saved to {filename}")

    def plot_results(self, X, y):
        """Plot training results: regression line, cost convergence, and training evolution."""
        plt.figure(figsize=(20, 6))

        plt.subplot(1, 3, 1)
        plt.scatter(X, y, color="blue", label="Training Data", alpha=0.6)
        line_x = np.linspace(np.min(X), np.max(X), 100)
        plt.plot(line_x, self.predict_price(line_x), color="red", label="Linear regression", linewidth=2)
        plt.xlabel("Mileage (km)")
        plt.ylabel("Price")
        plt.title("Linear Regression: Price vs Mileage")
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.subplot(1, 3, 2)
        plt.plot(self.cost_history, color="green", linewidth=2)
        plt.xlabel("Iterations")
        plt.ylabel("Cost (MSE/2)")
        plt.title("Cost Convergence")
        plt.grid(True, alpha=0.3)
        plt.yscale("log")

        plt.subplot(1, 3, 3)
        plt.scatter(X, y, color="blue", alpha=0.6, s=30, label="Training Data", zorder=5)

        colors = plt.cm.viridis(np.linspace(0, 1, len(self.theta_history)))

        line_x = np.linspace(np.min(X), np.max(X), 100)

        for i, (iteration, theta0, theta1) in enumerate(self.theta_history):
            y_pred = theta0 + theta1 * line_x

            alpha = 0.4 + 0.6 * (i / max(1, len(self.theta_history) - 1))
            linewidth = 1 + 1.5 * (i / max(1, len(self.theta_history) - 1))

            if i == 0:
                label = f"Iter {iteration}: θ₀={theta0:.0f}, θ₁={theta1:.4f} (Start)"
                style = "--"
            elif i == len(self.theta_history) - 1:
                label = f"Iter {iteration}: θ₀={theta0:.0f}, θ₁={theta1:.4f} (Final)"
                style = "-"
                linewidth += 1
            else:
                label = f"Iter {iteration}: θ₀={theta0:.0f}, θ₁={theta1:.4f}"
                style = "-"

            plt.plot(line_x, y_pred, color=colors[i], alpha=alpha, linewidth=linewidth, linestyle=style, label=label, zorder=3)

        plt.xlabel("Mileage (km)")
        plt.ylabel("Price")
        plt.title("Regression Line Over Time")

        if len(self.theta_history) <= 8:
            plt.legend(fontsize=7, loc="best")
        else:
            plt.legend([f"Start (iter {self.theta_history[0][0]})", f"Mid (iter {self.theta_history[len(self.theta_history) // 2][0]})", f"Final (iter {self.theta_history[-1][0]})"], fontsize=8, loc="best")

        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()


def calculate_metrics(model, mileage, price):
    """Calculate R² and MSE manually."""
    predictions = np.array([model.predict_price(x) for x in mileage])

    mse = np.mean((price - predictions) ** 2)

    ss_total = np.sum((price - np.mean(price)) ** 2)
    ss_residual = np.sum((price - predictions) ** 2)
    r_squared = 1 - (ss_residual / ss_total) if ss_total != 0 else 0

    return r_squared, mse, len(model.cost_history)


def optimize_hyperparameters(mileage, price):
    """Find optimal learning rate through grid search."""
    learning_rates = [0.001, 0.01, 0.05, 0.1, 0.2, 0.5]
    logger.info("Optimizing hyperparameters...")

    best_lr, best_score = 0.01, -1

    for lr in learning_rates:
        try:
            model = LinearRegression(learning_rate=lr, n_iterations=1000)
            model.fit(mileage, price, verbose=False)

            r_squared, _, iterations = calculate_metrics(model, mileage, price)
            score = r_squared + max(0, (1000 - iterations) / 1000 * 0.01)

            if score > best_score:
                best_score, best_lr = score, lr
        except Exception:
            continue

    logger.info(f"Best learning rate found: {best_lr} (Score = {best_score:.4f})")
    return best_lr


def train_model(data_file):
    """Train linear regression model with automatic hyperparameter optimization."""
    mileage, price = load_data(data_file, for_training=True)

    if mileage is None or price is None:
        raise ValueError("Failed to load training data")

    if np.any(mileage < 0):
        raise ValueError("Invalid data: negative mileage values")
    if np.any(price <= 0):
        raise ValueError("Invalid data: non-positive price values")

    best_lr = optimize_hyperparameters(mileage, price)
    logger.info(f"Training model with learning rate {best_lr}...")
    model = LinearRegression(learning_rate=best_lr, n_iterations=1000)
    model.fit(mileage, price)

    model.save_model()
    model.plot_results(mileage, price)

    return model.theta0_final, model.theta1_final


def train():
    """Main function to train the model and handle errors."""
    try:
        theta0, theta1 = train_model("data.csv")
        print("\nTraining successful!")
        print(f"Model parameters: θ₀ = {theta0:.6f}, θ₁ = {theta1:.6f}")
        print("Parameters saved to model_params.json")
        print("Use 'python evaluate.py' to calculate precision metrics.")
        return 0
    except FileNotFoundError:
        logger.error("Training data file 'data.csv' not found")
        print("Error: File data.csv not found")
        return 1
    except Exception as e:
        logger.error(f"Training failed: {e}")
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(train())
