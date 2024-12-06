import argparse

from classes.ApiHandler import EdamamAPIHandler
from classes.Exceptions import EdamamAPIFieldValidationError
from src.edamampy.config.settings import ApiSettings
from src.edamampy.constants.const import INCLUDED_FIELDS

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="EdamamRecipeSearchApiHandlerCLI",
        description="This is a basic cli to try out the Edamam recipe search api. After initialization you will be prompted first for the field you want to set and then for the value you want to set. Exiting the setting loop can be done typing 'quit'. After that you can either yield the results or sets to just dump all.",
        epilog="The app id and the api key can be found in your Edamam api dashboard.: https://developer.edamam.com/admin. Enjoy cooking!",
    )
    parser.add_argument(
        "-key",
        "--api-key",
        type=str,
        required=True,
        help="The API key for the edamam API.",
    )
    parser.add_argument(
        "-id",
        "--app-id",
        type=str,
        required=True,
        help="The app id for the edamam API.",
    )
    parser.add_argument(
        "-url",
        required=True,
        type=str,
        help="The current base url specified at: https://developer.edamam.com/edamam-docs-recipe-api",
    )
    parser.add_argument("-dump", action="store_true", help="Do not interactively iterate but dump all recipes to stdout.")
    parser.add_argument("-random", action="store_true", help="set random to true")
    parser.add_argument("-beta", action="store_true", help="check for if you want to use beta features.")
    parser.add_argument("-account_tracking", action="store_true", help="Enable account tracking.")
    parser.add_argument("-db", type=str, help="db selected. By default it is 'public'.")
    parser.add_argument(
        "-fields",
        type=str,
        help="A string containing fields that should be included in the Edamam response separated by commas.",
    )
    args = parser.parse_args()

    settings = ApiSettings(
        api_key=args.api_key,
        app_id=args.app_id,
        edamam_base_url=args.url,
        included_fields=args.fields.split(",") if args.fields else INCLUDED_FIELDS,
        db_type=args.db if args.db else "public",
        random=args.random,
        enable_beta=False,
        enable_account_user_tracking=False,
    )
    handler = EdamamAPIHandler(settings)
    while True:
        action = input("What action to take?\n\nOptions: set_field, set_multiple, inspect_query, exit\n")
        match action:
            case "set_field":
                field = input("Field to set:")
                val = input(f"Value for {field} field:")
                try:
                    handler.extend_query(field, val)
                except EdamamAPIFieldValidationError as e:
                    print(e)
                    print("Field was not set.")
            case "set_multiple":
                while True:
                    field = input("Type exit to escape setting multiple fields.\n Filed to set:")
                    if field == "exit":
                        break
                    val = input(f"Value for {field} field:")
                    try:
                        handler.extend_query(field, val)
                    except EdamamAPIFieldValidationError as e:
                        print(e)
                        print("Field was not set.")
            case "inspect_query":
                print(handler.query_builder)
            case "exit":
                break
            case _:
                print("Unknown action. Please type one of the following: set_field, set_multiple, inspect_query, exit")

    if args.dump:
        for recipes in handler:
            print(recipes.model_dump())
    else:
        for recipes in handler:
            print(recipes.model_dump())
            input("Continue")



