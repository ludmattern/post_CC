#!/usr/bin/env python3
"""
Price prediction script for linear regression model.
Loads trained model parameters and predicts car prices based on mileage.
"""

from utils import estimate_price, load_model_params


def predict():
    """Main prediction function with interactive input."""
    params = load_model_params()
    if not params:
        theta0 = 0
        theta1 = 0
    else:
        theta0 = params["theta0"]
        theta1 = params["theta1"]
        print(f"Model loaded: θ₀={theta0:.6f}, θ₁={theta1:.6f}")

    try:
        mileage = float(input("Enter the car's mileage (0-1,000,000 km): "))

        if mileage < 0:
            print("Error: Mileage cannot be negative.")
            return 1

        price = estimate_price(mileage, theta0, theta1)

        print(f"Estimated price for {mileage:.0f} km: {price:.2f} units")
        return 0
    except ValueError as e:
        if "Invalid" in str(e) or "calculation" in str(e):
            print(f"Error: {e}")
        else:
            print("Error: Please enter a valid number.")
        return 1
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit(predict())
