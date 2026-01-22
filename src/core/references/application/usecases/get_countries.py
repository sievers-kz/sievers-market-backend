from src.api.reference.dto import CountryDTO
from src.core.references.application.interfaces.abstract_country_repository import AbstractCountryRepository


class GetCountriesUseCase:
    def __init__(self, repository: AbstractCountryRepository):
        self.repository = repository

    async def execute(self):
        countries = await self.repository.get_all()
        return [CountryDTO.model_validate(country, from_attributes=True) for country in countries]
