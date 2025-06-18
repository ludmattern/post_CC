#!/usr/bin/env python3
"""
Common utilities for linear regression project.
Shared functions used across train.py, predict.py, and evaluate.py.
"""

import json
import numpy as np
from logging_config import get_logger

# Setup logger for utils module
logger = get_logger(__name__)


def estimate_price(mileage, theta0, theta1):
    """Calculate estimated price using linear model: price = θ₀ + (θ₁ * mileage)."""
    if not isinstance(mileage, (int, float)) or not np.isfinite(mileage):
        raise ValueError("Invalid mileage value")
    if not isinstance(theta0, (int, float)) or not np.isfinite(theta0):
        raise ValueError("Invalid theta0 parameter")
    if not isinstance(theta1, (int, float)) or not np.isfinite(theta1):
        raise ValueError("Invalid theta1 parameter")

    price = theta0 + (theta1 * mileage)

    if not np.isfinite(price):
        raise ValueError("Price calculation resulted in invalid value")

    return price


def load_model_params(filename="model_params.json"):
    """Load trained model parameters from JSON file."""
    try:
        with open(filename, "r") as f:
            params = json.load(f)

        if "theta0" not in params or "theta1" not in params:
            logger.error("Invalid model file - missing required parameters")
            return None

        logger.debug(f"Model parameters loaded from {filename}")
        return params
    except FileNotFoundError:
        logger.debug(f"Model parameters file '{filename}' not found")
        return None
    except json.JSONDecodeError:
        logger.error("Invalid JSON format in model file")
        return None
    except Exception as e:
        logger.error(f"Error loading model parameters: {e}")
        return None


def load_data(data_file="data.csv", for_training=False):
    """Load training data from CSV file with 'km' and 'price' columns."""
    try:
        data = np.loadtxt(data_file, delimiter=",", skiprows=1, usecols=(0, 1))
        mileage, price = data[:, 0], data[:, 1]

        min_samples = 2 if not for_training else 2
        error_msg = "Insufficient data for training" if for_training else "Insufficient valid data"

        if len(mileage) < min_samples:
            raise ValueError(error_msg)

        if for_training:
            logger.info(f"Training data loaded: {len(mileage)} samples")
        else:
            logger.debug(f"Data loaded: {len(mileage)} samples")

        return mileage, price
    except FileNotFoundError:
        logger.error(f"Data file '{data_file}' not found")
        return None, None
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return None, None
