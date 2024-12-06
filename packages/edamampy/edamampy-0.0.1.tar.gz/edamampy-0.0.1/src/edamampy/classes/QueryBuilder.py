from requests import PreparedRequest

from src.edamampy.classes.Exceptions import EdamamURLValidationError, EdamamAPIFieldKeyError
from src.edamampy.classes.Validator import EdamamFieldValidator

API_FIELD_VALIDATOR_MAPPING = {
    "q": "_validate_q",
    "ingr": "_validate_ingr",
    "diet": "_validate_diet",
    "health": "_validate_health",
    "cuisineType": "_validate_cuisineType",
    "mealType": "_validate_mealType",
    "dishType": "_validate_dishType",
    "calories": "_validate_floating_point_range",
    "time": "_validate_time",
    "imageSize": "_validate_imageSize",
    "glycemicIndex": "_validate_floating_point_range",
    "inflammatoryIndex": "_validate_floating_point_range",
    "nutrients[CA]": "_validate_nutrients",
    "nutrients[CHOCDF]": "_validate_nutrients",
    "nutrients[CHOCDF.net]": "_validate_nutrients",
    "nutrients[CHOLE]": "_validate_nutrients",
    "nutrients[ENERC_KCAL]": "_validate_nutrients",
    "nutrients[FAMS]": "_validate_nutrients",
    "nutrients[FAPU]": "_validate_nutrients",
    "nutrients[FASAT]": "_validate_nutrients",
    "nutrients[FAT]": "_validate_nutrients",
    "nutrients[FATRN]": "_validate_nutrients",
    "nutrients[FE]": "_validate_nutrients",
    "nutrients[FIBTG]": "_validate_nutrients",
    "nutrients[FOLAC]": "_validate_nutrients",
    "nutrients[FOLDFE]": "_validate_nutrients",
    "nutrients[FOLFD]": "_validate_nutrients",
    "nutrients[K]": "_validate_nutrients",
    "nutrients[MG]": "_validate_nutrients",
    "nutrients[NA]": "_validate_nutrients",
    "nutrients[NIA]": "_validate_nutrients",
    "nutrients[P]": "_validate_nutrients",
    "nutrients[PROCNT]": "_validate_nutrients",
    "nutrients[RIBF]": "_validate_nutrients",
    "nutrients[SUGAR]": "_validate_nutrients",
    "nutrients[SUGAR.added]": "_validate_nutrients",
    "nutrients[Sugar.alcohol]": "_validate_nutrients",
    "nutrients[THIA]": "_validate_nutrients",
    "nutrients[TOCPHA]": "_validate_nutrients",
    "nutrients[VITA_RAE]": "_validate_nutrients",
    "nutrients[VITB12]": "_validate_nutrients",
    "nutrients[VITB6A]": "_validate_nutrients",
    "nutrients[VITC]": "_validate_nutrients",
    "nutrients[VITD]": "_validate_nutrients",
    "nutrients[VITK1]": "_validate_nutrients",
    "nutrients[WATER]": "_validate_nutrients",
    "nutrients[ZN]": "_validate_nutrients",
    "co2EmissionsClass": "_validate_co2_emissions_class",
    "tag": "_validate_tag",
    "sysTag": "_validate_sys_tag",
    "Edamam-Account-User": "_validate_edamam_account_user",
    "Accept-Language": "_validate_accept_language",
    "excluded": "_validate_excluded",
    "random": "_validate_random",
    "field": "_validate_field",
}

class EdamamQueryBuilder(object):

    def __init__(
        self,
        api_key: str,
        app_id: str,
        edamam_base_url: str,
        included_fields: tuple,
        custom_validator_mapping: dict | None,
        custom_validator_class: object | None,
        db_type: str = "public",
        random: bool = False,
        enable_beta: bool = False,
        enable_account_user_tracking: bool = False,
    ):
        self._prepped_request = PreparedRequest()
        self.enable_beta = enable_beta
        self.enable_account_user_tracking = enable_account_user_tracking
        self.api_key = api_key
        self.edamam_base_url = edamam_base_url
        self.app_id = app_id
        self.db_type = db_type
        self.included_fields = included_fields
        self._current_url = ""
        self.random = random
        self.custom_validator_mapping = custom_validator_mapping
        self.custom_validator_class = custom_validator_class
        self._gen_initial_url()

    def __str__(self):
        return f"Current state of the generated URL: {self._current_url}"

    def _gen_initial_url(self) -> None:
        """

        :return:
        """
        self._prepped_request.prepare_url(
            self.edamam_base_url,
            {"app_id": self.app_id, "app_key": self.api_key, "random": self.random, "type": self.db_type},
        )
        self._current_url = self._prepped_request.url

        if not self.included_fields:
            return
        for key in self.included_fields:
            self._prepped_request.prepare_url(self._current_url, {"field": key})
            self._current_url = self._prepped_request.url

    def get_current_url(self) -> str:
        """
        Gets the current built up url, but before runs a validation to the edamam api spec.

        :return:
        """
        self._validate_current_url()
        return self._current_url

    def _validate_current_url(self) -> None:
        """
        Validates the current url.

        :return:
        """
        errs = [
            "app_id" not in self._current_url,
            "app_key" not in self._current_url,
            "type" not in self._current_url,
            ("q" not in self._current_url)
            and all([key not in self._current_url for key in API_FIELD_VALIDATOR_MAPPING.keys()]),
        ]

        if any(errs):
            raise EdamamURLValidationError(
                f"Edamam API URL is invalid. Given URL: {self._current_url}"
            )

    def append_to_query(self, key: str, value: str):
        """
        Based on the key validation for the value will run and throw an exception if the validation fails.

        :param key:
        :param value:
        :return:
        """
        validate_function = API_FIELD_VALIDATOR_MAPPING.get(key)
        if not hasattr(EdamamFieldValidator, validate_function):
            raise EdamamAPIFieldKeyError(key)
        method = getattr(EdamamFieldValidator, validate_function)
        method(value)

        if self.custom_validator_class is not None and self.custom_validator_mapping is not None:
            validate_function = self.custom_validator_mapping.get(key)
            if not hasattr(self.custom_validator_class, validate_function):
                raise EdamamAPIFieldKeyError(key)
            method = getattr(self.custom_validator_class, validate_function)
            method(value)

        self._prepped_request.prepare_url(self._current_url, {key: value})
        self._current_url = self._prepped_request.url
