import logging
logger = logging.getLogger(__name__)

import gspread
from gspread_dataframe import get_as_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from typing import List, Dict, Any

class GoogleSheet:

    def __init__(self, json_file: str = "secret.json") -> None:
        # Required URLs
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

        try:
            # JSON Credentials
            creds = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)

            # Create client
            self.client = gspread.authorize(creds)
            self.sheet = None

            logger.info("Access to Google Sheet successful!")

        except Exception as e:
            logger.error(e)

    def open_sheet(self, name_of_sheet, name_of_worksheet="") -> bool:
        """
            Opens the indicated worksheet inside of the Google Sheet.
        """

        # Opens the first worksheet in case of not specifying
        try:
            if not name_of_worksheet:
                self.sheet = self.client.open(name_of_sheet).sheet1
                logger.info("Opened first sheet of Google Sheet.")
                return True
            else:
                self.sheet = self.client.open(name_of_sheet).worksheet(name_of_worksheet)
                logger.info(f"Opened {name_of_worksheet} worksheet.")
                return True

        except Exception as e:
            logger.error(e)
            return False

    def change_worksheet(self, name_of_worksheet) -> bool:
        """
            Changes the current working sheet.
        """
        try:
            self.worksheet = self.sheet.worksheet(name_of_worksheet)
            logger.info(f"Changed worksheet to {name_of_worksheet}.")
            return True
        except Exception as e:
            logger.error(e)
            return False

    def all_records(self, df=False) -> List[Dict[str, Any]]:
        """
            Returns all the records of the workingsheet.
        """
        try:
            if df == True:
                _df = get_as_dataframe(self.sheet)
                _df.dropna(how='all', axis=1, inplace=True)
                _df.dropna(how='all', axis=0, inplace=True)
                return _df
            else:
                return self.sheet.get_all_records(expected_headers=["nombre"])
        except Exception as e:
            logger.error(e)
            return []

    def insert(self, row):
        """
            Appends a row at the end of the worksheet.
        """
        try:
            self.sheet.append_row(row)
            logger.info("New row appended to worksheet.")
        except Exception as e:
            logger.error(e)

    def update(self, row, column, value):
        """
            Updates the indicated cell with the input value.
        """
        try:
            self.sheet.update_cell(row, column, value)
            logger.info(f"Cell {row}, {column} updated.")
        except Exception as e:
            logger.error(e)

    def append_df(self, name_of_sheet, name_of_worksheet, df):
        """
            Appends a Pandas DataFrame at the end of the worksheet.
        """
        try:
            logger.info(f"Appends a Pandas DataFrame at the end of the worksheet.")
            df_values = df.values.tolist()
            self.client.open(name_of_sheet).values_append(name_of_worksheet, {'valueInputOption': 'RAW'}, {'values': df_values})
        except Exception as e:
            logger.error(e)