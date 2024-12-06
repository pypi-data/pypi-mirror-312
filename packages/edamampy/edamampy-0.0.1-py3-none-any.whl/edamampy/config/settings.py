from pydantic import BaseModel
from src.edamampy.constants.const import INCLUDED_FIELDS

class ApiSettings(BaseModel):
    api_key: str
    app_id: str
    edamam_base_url: str
    included_fields: tuple = INCLUDED_FIELDS
    custom_validator_mapping: dict | None = None
    custom_validator_class: object | None = None
    db_type: str = "public"
    random: bool = False
    enable_beta: bool = False
    enable_account_user_tracking: bool = False