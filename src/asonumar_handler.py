import datetime
from typing import Dict, Tuple, Optional
from src.gsheet import GoogleSheet

class AsonumarHandler:

    def __init__(self) -> None:
        self.gsheet_client = GoogleSheet()
        self.sheet_params = {
            "sheet_name" : "asonumar",
            "worksheet_name_cuotas" : "cuotas",
            "worksheet_name_actividades" : "actividades"
        }
        self.limit_date = 5 # Primer 5 del mes
        self.today = datetime.date.today()
    
    def get_members_status(self) -> None:
        # Abrir pestaña cuotas
            if not self.gsheet_client.open_sheet(self.sheet_params["sheet_name"], self.sheet_params["worksheet_name_cuotas"]):
                return None
            
            # obtener estado de asociados
            # Cuotas
            cuota_status = self.gsheet_client.all_records()
            if not cuota_status: # Vacia?
                return None
            print(cuota_status)