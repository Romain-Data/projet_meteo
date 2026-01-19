"""
Data validation module for weather data.
"""

import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class DataValidator:
    """
    Validator class for weather data.
    """

    REQUIRED_COLUMNS = {
        'pressure': np.int64,
        'humidity': np.int64,
        'temperature': np.float64,
        'date': 'datetime64'
    }

    def __init__(self, rules: dict):
        """
        Initializes the validator with a set of rules.

        Args:
            rules (dict): Dictionnary of rules set in config.yaml
        """
        self.rules = rules
        logger.info("DataValidator initialized with rules: %s", rules)

    def is_format_correct(self, data: pd.DataFrame) -> bool:
        """
        Validate that DataFrame columns have the expected data types.

        Args:
            data: DataFrame containing weather data columns

        Returns:
            True if all columns have correct types, False otherwise
        """
        try:
            if data.empty:
                logger.warning("Empty DataFrame provided for format validation")
                return False

            logger.info("Validating format for %s records", len(data))

            for column, expected_dtype in self.REQUIRED_COLUMNS.items():
                if column not in data.columns:
                    logger.error("Missing required column: %s", column)
                    return False

                actual_dtype = data[column].dtype

                if expected_dtype == 'datetime64':
                    is_valid = pd.api.types.is_datetime64_any_dtype(actual_dtype)
                else:
                    is_valid = actual_dtype == expected_dtype

                if not is_valid:
                    logger.error(
                        "Invalid type for %s: expected %s, got %s",
                        column,
                        expected_dtype,
                        actual_dtype
                    )
                    return False

                logger.debug("✓ %s has correct type: %s", column, actual_dtype)

            logger.info("Format validation passed")
            return True

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Format validation failed: %s - %s", type(e).__name__, str(e))
            return False

    def are_values_valid(self, data: pd.DataFrame) -> bool:
        """
        Check if all weather measurements fall within valid ranges.

        Args:
            data: DataFrame containing weather measurements

        Returns:
            True if all values are valid, False otherwise
        """
        try:
            if data.empty:
                logger.warning("Empty DataFrame provided for value validation")
                return False

            logger.info("Validating values for %s records", len(data))

            for column, rule_details in self.rules.items():
                if column not in data.columns:
                    continue

                min_val = rule_details.get('min')
                max_val = rule_details.get('max')

                is_valid = data[column].between(min_val, max_val).all()

                if not is_valid:
                    logger.error(
                        "Valeurs invalides dans %s hors de l'intervalle [%s, %s]",
                        column,
                        min_val,
                        max_val
                    )
                    return False

                logger.debug("✓ %s values in valid range [%s, %s]", column, min_val, max_val)

            logger.info("Value validation passed")
            return True

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Value validation failed: %s - %s", type(e).__name__, str(e))
            return False
