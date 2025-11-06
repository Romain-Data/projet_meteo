import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

class DataValidator:
    REQUIRED_COLUMNS = {
        'pression': np.int64,
        'humidite': np.int64,
        'temperature_en_degre_c': np.float64,
        'heure_de_paris': 'datetime64'
    }
    
    VALUE_RANGES = {
        'temperature_en_degre_c': (-20, 50),
        'humidite': (0, 100),
        'pression': (95000, 105000)
    }
    
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
            
            for column, (min_val, max_val) in self.VALUE_RANGES.items():
                if column not in data.columns:
                    logger.error(f"Missing column for value validation: '{column}'")
                    return False
                
                is_valid = data[column].between(min_val, max_val, inclusive='both').all()
                
                if not is_valid:
                    invalid_count = (~data[column].between(min_val, max_val, inclusive='both')).sum()
                    min_found = data[column].min()
                    max_found = data[column].max()
                    
                    logger.error(
                        f"Invalid values in '{column}': {invalid_count} records out of range "
                        f"[{min_val}, {max_val}]. Found range: [{min_found}, {max_found}]"
                    )
                    return False
                
                logger.debug(f"✓ '{column}' values in valid range [{min_val}, {max_val}]")
            
            logger.info("Value validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Value validation failed: {type(e).__name__} - {str(e)}")
            return False