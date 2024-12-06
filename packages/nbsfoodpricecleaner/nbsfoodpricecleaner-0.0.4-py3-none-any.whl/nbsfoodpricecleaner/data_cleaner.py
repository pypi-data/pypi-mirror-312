import pandas as pd
from typing import Optional, Dict, List


class NBSFoodPriceCleaner:
    """
    A class for cleaning and processing NBS food price data.
    """

    def __init__(self, input_filepath: Optional[str] = None, output_filepath: str = "cleaned_nbs_data.csv") -> None:
        """
        Initialize the cleaner with file paths.

        Args:
            input_filepath (Optional[str]): Path to the raw CSV file.
            output_filepath (str): Path to save the cleaned CSV file.
        """
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath
        self.data: Optional[pd.DataFrame] = None

    def load_data(self) -> None:
        """
        Load the raw data from the input CSV file.
        """
        if not self.input_filepath:
            raise ValueError("Input file path is not specified.")

        try:
            self.data = pd.read_csv(self.input_filepath)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: The file '{self.input_filepath}' was not found.")
        except pd.errors.EmptyDataError:
            raise ValueError("Error: The file is empty.")
        except Exception as e:
            raise Exception(f"An error occurred while loading data: {e}")

    def clean_data(self) -> None:
        """
        Clean and process the loaded data.
        """
        if self.data is None:
            raise ValueError("Data is not loaded. Use `load_data()` to load the data first.")

        # Drop irrelevant columns
        columns_to_drop: List[str] = [
            "_tags",
            "_notes",
            "_duration",
            "_id",
            "_uuid",
            "meta/instanceID",
            "_submission_time",
            "_date_modified",
            "_version",
            "_submitted_by",
            "_total_media",
            "_media_count",
            "_media_all_received",
            "_xform_id",
        ]
        self.data.drop(columns=columns_to_drop, errors="ignore", inplace=True)

        # Rename columns for consistency
        self.data.rename(
            columns={
                "today": "Date",
                "STATELABEL": "State",
                "lgalabel": "LGA",
                "g_consent/Section_A/market_type": "Outlet Type",
                "_gps_latitude": "Latitude",
                "_gps_longitude": "Longitude",
                "sector": "Sector",
                "VC_ID": "CONTRIBUTOR ID",
            },
            inplace=True,
        )

        # Add default country
        self.data["Country"] = "Nigeria"

        # Map food items to their respective columns
        food_mapping: Dict[str, Dict[str, str]] = {
            "g_consent/Section_B1/maize_yellow": {
                "uom": "g_consent/Section_B1/uom_Ymaize",
                "quantity": "g_consent/Section_B1/Q_Ymaize",
                "price": "g_consent/Section_B1/price_Ymaize",
            },
            "g_consent/Section_B2/maize_white": {
                "uom": "g_consent/Section_B2/uom_Wmaize",
                "quantity": "g_consent/Section_B2/Q_Wmaize",
                "price": "g_consent/Section_B2/price_Wmaize",
            },
            "g_consent/Section_B3/sorghum": {
                "uom": "g_consent/Section_B3/uom_sorghum",
                "quantity": "g_consent/Section_B3/Q_sorghum",
                "price": "g_consent/Section_B3/price_sorghum",
            },
            "g_consent/Section_B4/imported_rice": {
                "uom": "g_consent/Section_B4/uom_imported_rice",
                "quantity": "g_consent/Section_B4/Q_rice",
                "price": "g_consent/Section_B4/price_imported_rice",
            },
            "g_consent/Section_B5/local_rice": {
                "uom": "g_consent/Section_B5/uom_local_rice",
                "quantity": "g_consent/Section_B5/Q_local_rice",
                "price": "g_consent/Section_B5/price_local_rice",
            },
            "g_consent/Section_B6/brown_beans": {
                "uom": "g_consent/Section_B6/uom_brownbeans",
                "quantity": "g_consent/Section_B6/Q_brownbeans",
                "price": "g_consent/Section_B6/price_brown_beans",
            },
            "g_consent/Section_B7/White_beans": {
                "uom": "g_consent/Section_B7/uom_whitebeans",
                "quantity": "g_consent/Section_B7/Q_whitebeans",
                "price": "g_consent/Section_B7/price_White_beans",
            },
            "g_consent/Section_B8/garri_confirm": {
                "uom": "g_consent/Section_B8/uom_garri",
                "quantity": "g_consent/Section_B8/Q_garri",
                "price": "g_consent/Section_B8/price_garri",
            },
            "g_consent/Section_B9/yam_confirm": {
                "uom": "g_consent/Section_B9/uom_yam",
                "quantity": "g_consent/Section_B9/Q_yam",
                "price": "g_consent/Section_B9/price_yam",
            },
            "g_consent/Section_B10/Soyabeans": {
                "uom": "g_consent/Section_B10/uom_soyabeans",
                "quantity": "g_consent/Section_B10/Q_soyabeans",
                "price": "g_consent/Section_B10/price_soyabeans",
            },
        }

        # Prepare long-format data
        long_format_data: List[pd.DataFrame] = []
        for food_col, mapping in food_mapping.items():
            uom_col = mapping["uom"]
            quantity_col = mapping["quantity"]
            price_col = mapping["price"]

            if all(col in self.data.columns for col in [uom_col, quantity_col, price_col]):
                temp_df = self.data[
                    [
                        "Date",
                        "State",
                        "CONTRIBUTOR ID",
                        "LGA",
                        "Outlet Type",
                        "Latitude",
                        "Longitude",
                        "Country",
                        "Sector",
                    ]
                ].copy()
                temp_df["Food Item"] = food_col.split("/")[-1].replace("_", " ").capitalize()
                temp_df["UOM"] = self.data[uom_col].astype(str)
                temp_df["Quantity"] = pd.to_numeric(self.data[quantity_col], errors="coerce")
                temp_df["Price"] = pd.to_numeric(self.data[price_col], errors="coerce")

                # Calculate weight as Quantity * UOM (numeric part)
                temp_df["Weight"] = temp_df["Quantity"] * temp_df["UOM"].str.extract(r"(\d+\.?\d*)")[0].astype(float)

                # Calculate unit price
                temp_df["UPRICE"] = (temp_df["Price"] / temp_df["Weight"]).round(2)
                temp_df["Price Category"] = self.data.get("g_consent/Section_A/price_category", None)

                # Clean outlet type
                temp_df["Outlet Type"] = temp_df["Outlet Type"].str.replace("_", " ", regex=False)
                long_format_data.append(temp_df)

        # Combine the cleaned data
        if long_format_data:
            self.data = pd.concat(long_format_data, ignore_index=True)
        else:
            raise ValueError("No valid data found to clean.")

        # Reorder columns
        column_order = [
            "Date",
            "State",
            "CONTRIBUTOR ID",
            "LGA",
            "Outlet Type",
            "Latitude",
            "Longitude",
            "Country",
            "Sector",
            "Food Item",
            "UOM",
            "Quantity",
            "Price Category",
            "Price",
            "Weight",
            "UPRICE",
        ]
        self.data = self.data[column_order]

        # Convert 'Date' to datetime
        self.data["Date"] = pd.to_datetime(self.data["Date"], errors="coerce")

        # Drop rows with missing essential values
        essential_cols = [
            "State",
            "LGA",
            "Date",
            "Food Item",
            "UPRICE",
            "UOM",
            "Quantity",
            "Price",
            "Weight",
            "Latitude",
            "Longitude",
        ]
        self.data.dropna(subset=essential_cols, inplace=True)

    def save_cleaned_data(self) -> None:
        """
        Save the cleaned data to the specified output file.
        """
        if self.data is None:
            raise ValueError("No cleaned data available to save. Run `clean_data()` first.")

        self.data.to_csv(self.output_filepath, index=False)
        print(f"Cleaned data saved to {self.output_filepath}")

    def setup_ano_ai_connection(self) -> None:
        """
        Placeholder for setting up a connection with the ano.ai platform.
        """
        pass  # Future implementation goes here
