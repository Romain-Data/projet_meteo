import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class DataValidator:
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
        logger.info(f"DataValidator initialized with rules: {rules}")

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

            logger.info(f"Validating format for {len(data)} records")

            for column, expected_dtype in self.REQUIRED_COLUMNS.items():
                if column not in data.columns:
                    logger.error(f"Missing required column: '{column}'")
                    return False

                actual_dtype = data[column].dtype

                if expected_dtype == 'datetime64':
                    is_valid = pd.api.types.is_datetime64_any_dtype(actual_dtype)
                else:
                    is_valid = actual_dtype == expected_dtype

                if not is_valid:
                    logger.error(f"Invalid type for '{column}': expected {expected_dtype}, got {actual_dtype}")
                    return False

                logger.debug(f"✓ '{column}' has correct type: {actual_dtype}")

            logger.info("Format validation passed")
            return True

        except Exception as e:
            logger.error(f"Format validation failed: {type(e).__name__} - {str(e)}")
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

            logger.info(f"Validating values for {len(data)} records")

            for column, rule_details in self.rules.items():
                if column not in data.columns:
                    continue

                min_val = rule_details.get('min')
                max_val = rule_details.get('max')

                is_valid = data[column].between(min_val, max_val).all()

                if not is_valid:
                    logger.error(f"Valeurs invalides dans '{column}' hors de l'intervalle [{min_val}, {max_val}]")
                    return False

                logger.debug(f"✓ '{column}' values in valid range [{min_val}, {max_val}]")

            logger.info("Value validation passed")
            return True

        except Exception as e:
            logger.error(f"Value validation failed: {type(e).__name__} - {str(e)}")
            return False
