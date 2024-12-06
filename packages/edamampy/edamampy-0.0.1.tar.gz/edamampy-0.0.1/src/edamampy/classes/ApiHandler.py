from typing import Optional

from requests import request

from src.edamampy.classes.Exceptions import EdamamAPIException
from src.edamampy.classes.QueryBuilder import EdamamQueryBuilder
from src.edamampy.config.settings import ApiSettings

from pydantic import BaseModel, Field

class ImageInfo(BaseModel):
    url: str
    width: int
    height: int

class Link(BaseModel):
    href: str
    title: str

class Links(BaseModel):
    self: Optional[Link] | None = None
    next: Optional[Link] | None = None

class Ingredient(BaseModel):
    text: str
    quantity: float
    measure: Optional[str]
    food: str
    weight: float
    foodCategory: Optional[str] | None = None
    foodId: str
    image: Optional[str] | None = None

class Nutrient(BaseModel):
    label: str
    quantity: float
    unit: str

class SubDigest(BaseModel):
    label: str
    tag: str
    schemaOrgTag: Optional[str] | None = None
    total: float
    hasRDI: bool
    daily: float
    unit: str

class Digest(BaseModel):
    label: str
    tag: str
    sschemaOrgTag: Optional[str] | None = None
    total: float
    hasRDI: bool
    daily: float
    unit: str
    sub: list[SubDigest] | None = None

class Recipe(BaseModel):
    uri: str
    label: str
    image: str
    images: dict[str, ImageInfo]
    source: str
    url: str
    shareAs: str
    yield_field: float = Field(..., alias="yield")
    dietLabels: list[str]
    healthLabels: list[str]
    cautions: list[str]
    ingredientLines: list[str]
    ingredients: list[Ingredient]
    calories: float
    glycemicIndex: Optional[float] | None = None
    inflammatoryIndex: Optional[float] | None = None
    totalC02Emissions: Optional[float] | None = None
    co2EmissionsClass:  Optional[str] | None = None
    totalWeight: float
    totalTime: float
    cuisineType: Optional[list[str]] | None = None
    mealType:Optional[list[str]] | None = None
    dishType: Optional[list[str]] | None = None
    instructions: Optional[list[str]] | None = None
    externalId: Optional[str] | None = None
    totalNutrients: dict[str, Nutrient]
    totalDaily: dict[str, Nutrient]
    digest: list[Digest]
    tags: Optional[list[str]] | None = None


class Hit(BaseModel):
    recipe: Recipe
    links: Links = Field(..., alias="_links")


class EdamamResponse(BaseModel):
    from_field: int = Field(..., alias="from")
    to: int
    count: int
    links: Links = Field(..., alias="_links")
    hits: list[Hit]

class EdamamAPIHandler(object):
    def __init__(self, settings: ApiSettings):
        self.query_builder = EdamamQueryBuilder(**settings.model_dump())
        self.previous_return_data: None | EdamamResponse = None
        self.current_return_data: None | EdamamResponse = None

    def extend_query(self, key, value):
        """
        Main method to use.
        Provide the field which you want to set as the key and the value you want to set it as the value.
        This method will throw an exception if either the base field validator or the custom one you supplied
        raise an exception.

        Field to check has no validtor function on the validator class -> EdamamAPIFieldKeyError
        Field validation failed -> EdamamAPIFieldValidationError

        :param key:
        :param value:
        :return:
        :raises: EdamamAPIFieldKeyError | EdamamAPIFieldValidationError
        """
        self.query_builder.append_to_query(key, value)

    def _get_full_url(self):
        """
        Only call this once you are confident you have every parameter set.

        :return:
        """
        return self.query_builder.get_current_url()

    async def a_request_recipes(self):
        if self.current_return_data:
            ret = request(
                "get",
                self.current_return_data.links.next.href,
            )
        else:
            ret = request("get", self._get_full_url())
        if ret.status_code != 200:
            raise EdamamAPIException(
                ret=ret.json(), status_code=ret.status_code, additional_message=ret.text
            )
        return EdamamResponse(**ret.json())

    def request_recipes(self):
        if self.current_return_data:
            ret = request(
                "get",
                self.current_return_data.links.next.href,
            )
        else:
            ret = request("get", self._get_full_url())

        if ret.status_code != 200:
            raise EdamamAPIException(
                ret=ret.json(), status_code=ret.status_code, additional_message=ret.text
            )
        return EdamamResponse(**ret.json())

    def __iter__(self):
        return self

    def __next__(self):
        self.previous_return_data = self.current_return_data
        self.current_return_data = self.request_recipes()

        if self.current_return_data.links.next is None:
            raise StopIteration

        return self.current_return_data

    def __aiter__(self):
        return self

    async def __anext__(self):
        self.previous_return_data = self.current_return_data
        self.current_return_data = await self.a_request_recipes()

        if self.current_return_data.links.next is None:
            raise StopAsyncIteration

        return self.current_return_data