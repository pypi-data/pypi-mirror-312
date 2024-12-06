from src.edamampy.classes.Exceptions import EdamamAPIFieldValidationError
from src.edamampy.constants.const import (
    INCLUDED_FIELDS,
    RANDOM_FIELD,
    IMAGE_SIZE,
    DISH_TYPE,
    MEAL_TYPE,
    HEALTH_TYPE,
    CUISINE_TYPE,
    DIET_TYPE,
)
class EdamamFieldValidator(object):

    @staticmethod
    def _validate_diet(value: str) -> None:
        if value not in DIET_TYPE:
            raise EdamamAPIFieldValidationError("diet", value)

    @staticmethod
    def _validate_floating_point_range(value: str) -> None:
        try:
            if "-" in value:
                first, second = value.split("-")
                float(first)
                float(second)
            else:
                float(value)
        except ValueError:
            raise EdamamAPIFieldValidationError("nutrients", value)

    @staticmethod
    def _validate_q(value: str) -> None:
        """
        Validate the query item.

        :param value:
        :return:
        """
        if any(map(lambda x: x.isdigit(), value)):
            raise EdamamAPIFieldValidationError("q", value)

    @staticmethod
    def _validate_ingr(value: str) -> None:
        """
        On the edamam api this field filters for min to max ingredients.
        Allowed formats: MIN+, MIN-MAX, MAX OR empty

        :return:
        """
        if "-" in value:
            value1, value2 = value.split("-")
            try:
                int(value1)
                int(value2)
            except ValueError:
                raise EdamamAPIFieldValidationError("ingr", value)

            return

        if "+" in value:
            try:
                assert value[len(value) - 1] == "+"
                int(value[: len(value) - 1])
            except AssertionError:
                raise EdamamAPIFieldValidationError("ingr", value)
            except ValueError:
                raise EdamamAPIFieldValidationError("ingr", value)

            return

        try:
            int(value)
        except ValueError:
            raise EdamamAPIFieldValidationError("ingr", value)

    @staticmethod
    def _validate_cuisine_type(value: str) -> None:
        if value not in CUISINE_TYPE:
            raise EdamamAPIFieldValidationError("cuisineType", value)

    @staticmethod
    def _validate_health(value: str) -> None:
        if value not in HEALTH_TYPE:
            raise EdamamAPIFieldValidationError("health", value)

    @staticmethod
    def _validate_meal_type(value: str) -> None:
        if value not in MEAL_TYPE:
            raise EdamamAPIFieldValidationError("mealType", value)

    @staticmethod
    def _validate_dish_type(value: str) -> None:
        if value not in DISH_TYPE:
            raise EdamamAPIFieldValidationError("dishType", value)

    @staticmethod
    def _validate_time(value: str) -> None:
        """
        Validates the time format to be in the format of MIN+, MIN-MAX, MAX
        :param value:
        :return:
        """
        if "-" in value:
            value1, value2 = value.split("-")
            try:
                int(value1)
                int(value2)
            except ValueError:
                raise EdamamAPIFieldValidationError("time", value)

            return

        if "+" in value:
            try:
                assert value[len(value) - 1] == "+"
                int(value[: len(value) - 1])
            except AssertionError:
                raise EdamamAPIFieldValidationError("time", value)
            except ValueError:
                raise EdamamAPIFieldValidationError("time", value)

            return

        try:
            int(value)
        except ValueError:
            raise EdamamAPIFieldValidationError("time", value)

    @staticmethod
    def _validate_image_size(value: str) -> None:
        if value not in IMAGE_SIZE:
            raise EdamamAPIFieldValidationError("imageSize", value)

    @staticmethod
    def _validate_nutrients(value: str) -> None:
        if "-" in value:
            value1, value2 = value.split("-")
            try:
                float(value1)
                float(value2)
            except ValueError:
                raise EdamamAPIFieldValidationError("nutrients", value)

            return

        if "+" in value:
            try:
                if not value[len(value) - 1] == "+":
                    raise EdamamAPIFieldValidationError("nutrients", value)
                float(value[: len(value) - 1])
            except ValueError:
                raise EdamamAPIFieldValidationError("nutrients", value)

            return

        try:
            float(value)
        except ValueError:
            raise EdamamAPIFieldValidationError("nutrients", value)

    @staticmethod
    def _validate_excluded(value: str) -> None:
        try:
            assert value.islower()
        except AssertionError:
            raise EdamamAPIFieldValidationError("excluded", value)

    @staticmethod
    def _validate_random(value: str) -> None:
        if value not in RANDOM_FIELD:
            raise EdamamAPIFieldValidationError("random", value)

    @staticmethod
    def _validate_field(value: str) -> None:
        if value not in INCLUDED_FIELDS:
            raise EdamamAPIFieldValidationError("field", value)

    @staticmethod
    def _validate_co2_emissions_class(value: str) -> None:
        if value.casefold() not in ["A+", "A", "B", "C", "D", "E", "F", "G"]:
            raise EdamamAPIFieldValidationError("c02_emissions_class", value)

    @staticmethod
    def _validate_tag(value: str) -> None:
        pass

    @staticmethod
    def _validate_sys_tag(value: str) -> None:
        if value.casefold() != "live":
            raise EdamamAPIFieldValidationError("sys_tag", value)

    @staticmethod
    def _validate_accept_language(value: str) -> None:
        pass