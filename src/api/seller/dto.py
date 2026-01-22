from typing import Literal, Annotated, Union
from uuid import UUID

from pydantic import BaseModel, Field

from src.core.seller.domain.enums import SellerType


class SellerFullnameData(BaseModel):
    last_name: str
    first_name: str
    patronymic: str | None = None


class CompanyNameData(BaseModel):
    company_name: str


class TaxIDData(BaseModel):
    tax_id: str


class BecomeSellerData(BaseModel):
    last_name: str
    first_name: str
    patronymic: str | None = None
    legal_name: str
    tax_id: str


class BecomeIndividualSeller(BecomeSellerData):
    seller_type: Literal[SellerType.IE]


class BecomeCompanySeller(BecomeSellerData):
    seller_type: Literal[SellerType.LLP]


BecomeSellerRequest = Annotated[
    Union[BecomeIndividualSeller, BecomeCompanySeller],
    Field(discriminator="seller_type")
]


class SellerResponse(BaseModel):
    last_name: str
    first_name: str
    patronymic: str | None = None
    seller_type: SellerType
    legal_name: str
    tax_id: str
    logotype_url: str
