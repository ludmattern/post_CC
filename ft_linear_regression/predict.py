#!/usr/bin/env python3
"""
Price prediction script for linear regression model.
Loads trained model parameters and predicts car prices based on mileage.
"""

from utils import estimate_price, load_model_params
from logging_config import get_logger

# Setup logger for prediction module
logger = get_logger(__name__)


def predict():
    """Main prediction function with interactive input."""
    logger.debug("Starting prediction function")

    params = load_model_params()
    if not params:
        print("Warning: No trained model found, using default parameters (predictions will be 0)")
        theta0 = 0
        theta1 = 0
    else:
        theta0 = params["theta0"]
        theta1 = params["theta1"]
        logger.debug(f"Model loaded: θ₀={theta0:.6f}, θ₁={theta1:.6f}")

    try:
        mileage = float(input("Enter the car's mileage (in km): "))
        logger.debug(f"User input: mileage={mileage}")

        if mileage < 0:
            logger.warning(f"User entered negative mileage: {mileage}")
            print("Error: Mileage cannot be negative.")
            return 1

        price = estimate_price(mileage, theta0, theta1)
        logger.debug(f"Prediction calculated: {mileage:.0f} km → {price:.2f} units")

        print(f"Estimated price for {mileage:.0f} km: {price:.2f} units")
        return 0
    except ValueError as e:
        if "Invalid" in str(e) or "calculation" in str(e):
            logger.error(f"Calculation error: {e}")
            print(f"Error: {e}")
        else:
            logger.info("Invalid number format from user input")
            print("Error: Please enter a valid number.")
        return 1
    except KeyboardInterrupt:
        logger.debug("Prediction interrupted by user")
        print("\nProgram interrupted by user.")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error in prediction: {e}")
        print("Error: Unexpected error occurred")
        return 1


if __name__ == "__main__":
    exit(predict())
