import logging
logger = logging.getLogger(__name__)

from datetime import datetime
from typing import Dict, Tuple, Optional, List, Any
from src.gsheet import GoogleSheet

class AsonumarHandler:

    def __init__(self) -> None:
        self.gsheet_client = GoogleSheet()
        self.sheet_params = {
            "sheet_name" : "asonumar",
            "worksheet_name_cuotas" : "cuotas",
            "worksheet_name_actividades" : "actividades",
            "worksheet_name_asociados" : "info"
        }
        self.limit_date = 5 # Primer 5 del mes
        self.today_date = datetime.now()
        self.today_day = datetime.now().day
        self.members = self.get_members()
        self.status_cuotas, self.status_actividades = self.get_members_status()
    
    def handle(self):
        if None in [self.members, self.status_cuotas, self.status_actividades]:
            logger.error("Could not handle.")
            return
        logger.info("Hanlder started.")


    def get_members(self) -> List[Dict[str, Any]]:
        # Obtener estado actividades
        if not self.gsheet_client.open_sheet(self.sheet_params["sheet_name"], self.sheet_params["worksheet_name_asociados"]):
            return None
        
        asociados_info = self.gsheet_client.all_records()
        if not asociados_info: # Vacia?
            logger.error("Could not get asociados info.")
            return None
        logger.info("Asociados info downloaded successfully.")

        return asociados_info


    def get_members_status(self) -> Optional[Tuple[List[Dict[str, Any]]]]:
    # Obtener estado cuotas
        if not self.gsheet_client.open_sheet(self.sheet_params["sheet_name"], self.sheet_params["worksheet_name_cuotas"]):
            return None
        
        cuota_status = self.gsheet_client.all_records()
        if not cuota_status: # Vacia?
            logger.error("Could not get cuotas status info.")
            return None
        logger.info("Cuotas status downloaded successfully.")
    
    # Obtener estado actividades
        if not self.gsheet_client.open_sheet(self.sheet_params["sheet_name"], self.sheet_params["worksheet_name_actividades"]):
            return None
        
        actividades_status = self.gsheet_client.all_records()
        if not actividades_status: # Vacia?
            logger.error("Could not get actividades status info.")
            return None
        logger.info("Actividades status downloaded successfully.")

        return cuota_status, actividades_status

