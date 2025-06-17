#!/usr/bin/env python3
"""
Model evaluation script for linear regression.
Calculates performance metrics (MSE, R²) on training data with visual display.
"""

import numpy as np
import matplotlib.pyplot as plt
from utils import estimate_price, load_model_params, load_data


def calculate_metrics(mileage, price, theta0, theta1):
    """Calculate all evaluation metrics for the model."""
    predictions = np.array([estimate_price(x, theta0, theta1) for x in mileage])
    errors = price - predictions
    abs_errors = np.abs(errors)

    mse = np.mean(errors**2)
    rmse = np.sqrt(mse)
    mae = np.mean(abs_errors)

    ss_total = np.sum((price - np.mean(price)) ** 2)
    ss_residual = np.sum(errors**2)
    r_squared = 1 - (ss_residual / ss_total) if ss_total != 0 else 0

    max_error = np.max(abs_errors)
    min_error = np.min(abs_errors)
    mean_price = np.mean(price)
    mape = np.mean(np.abs(errors / price)) * 100

    return {"predictions": predictions, "errors": errors, "abs_errors": abs_errors, "mse": mse, "rmse": rmse, "mae": mae, "r_squared": r_squared, "max_error": max_error, "min_error": min_error, "mean_price": mean_price, "mape": mape}


def create_visualizations(mileage, price, metrics, theta0, theta1):
    """Create comprehensive visualization dashboard."""
    predictions = metrics["predictions"]
    errors = metrics["errors"]
    mse = metrics["mse"]
    rmse = metrics["rmse"]
    mae = metrics["mae"]
    r_squared = metrics["r_squared"]
    max_error = metrics["max_error"]
    min_error = metrics["min_error"]
    mean_price = metrics["mean_price"]
    mape = metrics["mape"]

    plt.figure(figsize=(16, 12))

    plt.subplot(2, 3, 1)
    plt.scatter(price, predictions, alpha=0.7, color="blue", s=50)
    min_val = min(np.min(price), np.min(predictions))
    max_val = max(np.max(price), np.max(predictions))
    plt.plot([min_val, max_val], [min_val, max_val], "r--", linewidth=2, label="Perfect prediction")
    plt.xlabel("Actual Price")
    plt.ylabel("Predicted Price")
    plt.title("Predictions vs Actual Values")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(2, 3, 2)
    plt.scatter(predictions, errors, alpha=0.7, color="green", s=50)
    plt.axhline(y=0, color="r", linestyle="--", linewidth=2)
    plt.xlabel("Predicted Price")
    plt.ylabel("Residuals (Actual - Predicted)")
    plt.title("Residuals Analysis")
    plt.grid(True, alpha=0.3)

    plt.subplot(2, 3, 3)
    plt.hist(errors, bins=10, alpha=0.7, color="orange", edgecolor="black")
    plt.axvline(x=0, color="r", linestyle="--", linewidth=2, label="Perfect prediction")
    plt.xlabel("Prediction Errors")
    plt.ylabel("Frequency")
    plt.title("Error Distribution")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(2, 3, 4)
    metrics_names = ["R²", "MAPE (%)", "Normalized\nRMSE"]
    normalized_rmse = (rmse / mean_price) * 100
    metrics_values = [r_squared, mape, normalized_rmse]
    colors = ["green" if r_squared > 0.7 else "orange", "green" if mape < 15 else "orange", "green" if normalized_rmse < 20 else "orange"]

    bars = plt.bar(metrics_names, metrics_values, color=colors, alpha=0.7, edgecolor="black")
    plt.ylabel("Values")
    plt.title("Key Performance Metrics")
    plt.grid(True, alpha=0.3, axis="y")

    for bar, value in zip(bars, metrics_values):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height + height * 0.02, f"{value:.2f}", ha="center", va="bottom", fontweight="bold")

    plt.subplot(2, 3, 5)
    if r_squared > 0.9:
        quality = "Excellent"
        quality_color = "green"
    elif r_squared > 0.7:
        quality = "Good"
        quality_color = "orange"
    elif r_squared > 0.5:
        quality = "Fair"
        quality_color = "red"
    else:
        quality = "Poor"
        quality_color = "darkred"

    plt.pie([r_squared, 1 - r_squared], labels=["Explained Variance", "Unexplained"], colors=[quality_color, "lightgray"], startangle=90, counterclock=False)
    plt.title(f"Model Quality: {quality}\nR² = {r_squared:.3f}")

    _create_metrics_table(mileage, mse, rmse, mae, r_squared, mape, max_error, min_error)

    plt.suptitle(f"Linear Regression Model Evaluation\nFormula: price = {theta0:.2f} + ({theta1:.6f} × mileage)", fontsize=12, fontweight="bold")
    plt.tight_layout()
    plt.subplots_adjust(top=0.90, hspace=0.4, wspace=0.3)

    return quality


def _create_metrics_table(mileage, mse, rmse, mae, r_squared, mape, max_error, min_error):
    """Helper function to create the metrics table."""
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis("tight")
    ax6.axis("off")

    explanatory_text = "METRIC GUIDE:\n• R² = Variance explained (closer to 1.0 = better)\n• RMSE/MAE = Average prediction errors\n• MAPE = Percentage accuracy\n• MSE = Squared errors (penalizes large errors)"
    ax6.text(0.5, 0.95, explanatory_text, ha="center", va="top", transform=ax6.transAxes, fontsize=8, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))

    metrics_data = [
        ["Metric", "Value", "Interpretation"],
        ["MSE", f"{mse:.2f}", "Mean Squared Error (lower = better)"],
        ["RMSE", f"{rmse:.2f}", f"Typical error: ±{rmse:.0f} price units"],
        ["MAE", f"{mae:.2f}", f"Average error: ±{mae:.0f} price units"],
        ["R²", f"{r_squared:.4f}", f"Model explains {r_squared * 100:.1f}% of variance"],
        ["MAPE", f"{mape:.2f}%", f"{'Excellent' if mape < 10 else 'Good' if mape < 15 else 'Fair'} accuracy"],
        ["Max Error", f"{max_error:.2f}", f"Worst prediction off by {max_error:.0f}"],
        ["Min Error", f"{min_error:.2f}", f"Best prediction off by {min_error:.0f}"],
        ["Data Points", f"{len(mileage)}", "Training samples used"],
    ]

    table = ax6.table(cellText=metrics_data[1:], colLabels=metrics_data[0], cellLoc="center", loc="lower center", colWidths=[0.25, 0.25, 0.5])
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.6)

    for i in range(len(metrics_data)):
        for j in range(len(metrics_data[0])):
            cell = table[(i, j)]
            if i == 0:
                cell.set_facecolor("#4CAF50")
                cell.set_text_props(weight="bold", color="white")
            else:
                cell.set_facecolor("#f0f0f0" if i % 2 == 0 else "white")


def print_evaluation_summary(quality, metrics, theta0, theta1):
    """Print detailed evaluation summary with examples."""
    r_squared = metrics["r_squared"]
    mae = metrics["mae"]
    mape = metrics["mape"]

    print("\n" + "=" * 50)
    print("MODEL EVALUATION SUMMARY")
    print("=" * 50)
    print(f"* Model accuracy: {quality} (R² = {r_squared:.3f})")
    print(f"* Average error: ±{mae:.0f} price units")
    print(f"* Relative error: {mape:.1f}% on average")

    example_km = [50000, 100000, 150000, 200000]
    print("\nPREDICTION EXAMPLES:")
    for km in example_km:
        pred = estimate_price(km, theta0, theta1)
        print(f"   • {km:,} km → {pred:.0f} price units")

    print(f"\nFORMULA: price = {theta0:.0f} + ({theta1:.6f} × mileage)")

    if r_squared > 0.8:
        print("* This model is sufficiently accurate for reliable predictions")
    elif r_squared > 0.6:
        print("* This model provides reasonable estimates")
    else:
        print("* This model needs improvement (more data, additional variables)")

    print("=" * 50)


def evaluate_model(data_file="data.csv"):
    """Evaluate model accuracy on training data and display comprehensive visual metrics."""
    params = load_model_params()
    if not params:
        return 1

    print("MODEL PRECISION EVALUATION")
    print("Loading model and data...")

    theta0 = params["theta0"]
    theta1 = params["theta1"]

    mileage, price = load_data(data_file)
    if mileage is None or price is None:
        return 1

    print(f"Model loaded: θ₀ = {theta0:.6f}, θ₁ = {theta1:.6f}")
    print(f"Evaluating on {len(mileage)} data points...")

    try:
        metrics = calculate_metrics(mileage, price, theta0, theta1)

        quality = create_visualizations(mileage, price, metrics, theta0, theta1)

        plt.show()

        print_evaluation_summary(quality, metrics, theta0, theta1)
        print("Evaluation completed! Visual analysis displayed.")

        return 0

    except Exception as e:
        print(f"Error during evaluation: {e}")
        return 1


def main():
    """Main function to evaluate the model and handle errors."""
    try:
        print("Starting visual model evaluation...")
        result = evaluate_model("data.csv")
        if result == 0:
            print("Model evaluation completed successfully!")
        return result
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
