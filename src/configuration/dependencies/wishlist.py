from dependency_injector import containers, providers

from src.core.wishlist.application.services.wishlist import WishlistService
from src.core.wishlist.application.usecases import AddToWishlistUseCase, DeleteFromWishlistUseCase, GetWishlistUseCase
from src.core.wishlist.infrastructure.repository import WishlistRepository
from src.core.wishlist.infrastructure.wishlist_unit_of_work import WishlistUnitOfWork


class WishlistContainer(containers.DeclarativeContainer):
    database_session = providers.Dependency()

    wishlist_repository = providers.Factory(
        WishlistRepository,
        session=database_session
    )

    wishlist_service = providers.Factory(
        WishlistService,
        repository=wishlist_repository
    )

    wishlist_unit_of_work = providers.Factory(
        WishlistUnitOfWork,
        session=database_session
    )

    add_to_wishlist_usecase = providers.Factory(
        AddToWishlistUseCase,
        unit_of_work=wishlist_unit_of_work
    )

    delete_from_wishlist_usecase = providers.Factory(
        DeleteFromWishlistUseCase,
        unit_of_work=wishlist_unit_of_work
    )

    get_wishlist_usecase = providers.Factory(
        GetWishlistUseCase,
        unit_of_work=wishlist_unit_of_work
    )
