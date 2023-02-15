import logging
logger = logging.getLogger(__name__)

from datetime import datetime
from typing import Dict, Tuple, Optional, List, Any
from src.gsheet import GoogleSheet
from src.constants import months

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
        self.today_day = datetime.now().day
        self.today_month = datetime.now().month
        self.today_month = 0 if self.today_month == 12 else self.today_month
        self.members = self.get_members_info()
        self.status_cuotas, self.status_actividades = self.get_members_status()
    
    def handle(self):
        if None in [self.members, self.status_cuotas, self.status_actividades]:
            logger.error("Could not handle.")
            return
        logger.info("Hanlder started.")
        self.update_debtors(self.status_cuotas, self.sheet_params["worksheet_name_cuotas"])
        self.update_debtors(self.status_actividades, self.sheet_params["worksheet_name_actividades"])


    def get_members_info(self) -> List[Dict[str, Any]]:
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

    def update_debtors(self, status, worksheet_name):
        if not self.gsheet_client.open_sheet(self.sheet_params["sheet_name"], worksheet_name):
            return None
        for i, cuotas_member in enumerate(status):
            paid_months_counter = 0
            for month, value in cuotas_member.items():
                if "nombre" in month:
                    name = value
                    continue
                if "deudor" in month :
                    continue
                if "dic" in month and not value:
                    logger.info(f"{name} ha pagado hasta {month} - Es deudor")
                    self.gsheet_client.update_cell(f"N{i+2}", "Si")
                    break
                if not value:
                    if self.today_month == months[month] and self.today_day <= 5:
                        logger.info(f"{name} ha pagado hasta {month} - Pronto a vencer fecha")
                        self.gsheet_client.update_cell(f"N{i+2}", "Casi")
                    elif self.today_month > months[month]:
                        logger.info(f"{name} ha pagado hasta {month} - Es deudor")
                        self.gsheet_client.update_cell(f"N{i+2}", "Si")
                    else:
                        logger.info(f"{name} ha pagado hasta {month} - No es deudor")
                        self.gsheet_client.update_cell(f"N{i+2}", "No")
                    break
                else:
                    paid_months_counter += 1
                if paid_months_counter == 12:
                    status[i]["deudor"] = "Todo pago"
                    self.gsheet_client.update_cell(f"N{i+2}", "Todo pago")
    

    def send_mail():
        pass