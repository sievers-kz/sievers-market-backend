import uuid
from dataclasses import dataclass
from uuid import UUID

from src.core.catalog.domain.enums import CatalogStatus
from src.core.catalog.domain.exceptions import DuplicateAttributeError
from src.core.catalog.domain.value_objects import Attribute
from src.core.shared.domain.entities import AggregateRoot


@dataclass(frozen=False)
class Subcategory(AggregateRoot):
    id: UUID
    category_id: UUID
    name: str
    attributes: list[Attribute]
    status: CatalogStatus

    @classmethod
    def create(
        cls,
        category_id: UUID,
        name: str,
        attributes: list[Attribute]
    ) -> "Subcategory":
        return cls(
            id=uuid.uuid4(),
            category_id=category_id,
            name=name,
            attributes=attributes,
            status=CatalogStatus.ACTIVE
        )

    def change_parent(self, parent_id: UUID) -> None:
        if self.category_id == parent_id:
            return

        self.category_id = parent_id
        self.attributes = []

    def change_name(self, name: str) -> None:
        if self.name == name:
            return
        self.name = name

    def replace_attributes(self, new_attributes: list[Attribute]) -> None:
        keys = [attr.key for attr in new_attributes]
        if len(keys) != len(set(keys)):
            raise DuplicateAttributeError()
        self.attributes = new_attributes

    def delete(self) -> None:
        if self.status == CatalogStatus.DELETED:
            return
        self.status = CatalogStatus.DELETED

    def validate_attributes(self, attributes: dict) -> dict:
        clean_data = {}

        for attr_rule in self.attributes:
            user_value = attributes.get(attr_rule.key)

            valid_value = attr_rule.validate_value(user_value)

            if valid_value is not None:
                clean_data[attr_rule.key] = valid_value

        return clean_data


@dataclass(frozen=False)
class Category(AggregateRoot):
    id: UUID
    rubric_id: UUID
    name: str
    status: CatalogStatus

    @classmethod
    def create(
        cls,
        rubric_id: UUID,
        name: str,
    ) -> "Category":
        return cls(
            id=uuid.uuid4(),
            rubric_id=rubric_id,
            name=name,
            status=CatalogStatus.ACTIVE
        )

    def change_parent(self, parent_id: UUID) -> None:
        if self.rubric_id == parent_id:
            return
        self.rubric_id = parent_id

    def change_name(self, name: str) -> None:
        if self.name == name:
            return
        self.name = name

    def delete(self) -> None:
        if self.status == CatalogStatus.DELETED:
            return
        self.status = CatalogStatus.DELETED


@dataclass(frozen=False)
class Rubric(AggregateRoot):
    id: UUID
    name: str
    attributes: list[Attribute]
    status: CatalogStatus

    @classmethod
    def create(
        cls,
        name: str,
        attributes: list[Attribute],
    ) -> "Rubric":
        return cls(
            id=uuid.uuid4(),
            name=name,
            attributes=attributes,
            status=CatalogStatus.ACTIVE
        )

    def change_name(self, name: str) -> None:
        if self.name == name:
            return
        self.name = name

    def replace_attributes(self, new_attributes: list[Attribute]) -> None:
        keys = [attr.key for attr in new_attributes]
        if len(keys) != len(set(keys)):
            raise DuplicateAttributeError()
        self.attributes = new_attributes

    def delete(self) -> None:
        if self.status == CatalogStatus.DELETED:
            return
        self.status = CatalogStatus.DELETED
