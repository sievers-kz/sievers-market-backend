import uuid
from dataclasses import dataclass, field
from uuid import UUID

from src.core.admin.domain.enums import AdminRoles
from src.core.admin.domain.exceptions import InsufficientPermissionsError
from src.core.shared.domain.entities import AggregateRoot, Entity


@dataclass(frozen=False)
class Admin(AggregateRoot):
    id: UUID
    account_id: UUID
    last_name: str
    first_name: str
    patronymic: str
    role: AdminRoles
    permissions: list["Permission"] = field(default_factory=list)

    @classmethod
    def _create(
        cls,
        account_id: UUID,
        last_name: str,
        first_name: str,
        patronymic: str,
        role: AdminRoles,
    ):
        return cls(
            id=uuid.uuid4(),
            account_id=account_id,
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
            role=role,
        )

    def is_super_admin(self):
        return self.role == AdminRoles.SUPER_ADMIN

    def _ensure_can_manage_admins(self, target_role: AdminRoles):
        if self.is_super_admin():
            return
        if target_role in (AdminRoles.SUPER_ADMIN, AdminRoles.ADMIN):
            raise InsufficientPermissionsError()
        if self.role != AdminRoles.ADMIN or not self.has_permission("manage_admins"):
            raise InsufficientPermissionsError()

    def add_admin(
        self,
        account_id: UUID,
        last_name: str,
        first_name: str,
        patronymic: str,
        role: AdminRoles,
    ) -> "Admin":
        self._ensure_can_manage_admins(role)

        return Admin._create(
            account_id=account_id,
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
            role=role,
        )

    def has_permission(self, code: str) -> bool:
        return any(p.code == code for p in self.permissions)


@dataclass(frozen=False)
class Permission(Entity):
    id: UUID
    code: str
    description: str
