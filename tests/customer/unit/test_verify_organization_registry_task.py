import asyncio
import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from arq import Retry

from src.core.customer.domain.exceptions import TaxpayerRegistryUnavailableError
from src.workers import verify_organization_registry


def make_ctx(usecase: AsyncMock, job_try: int = 1) -> dict:
    """ARQ ctx whose container hands out `usecase` the way the real provider does (as an awaitable)."""

    def provide_usecase():
        future = asyncio.get_running_loop().create_future()
        future.set_result(usecase)
        return future

    container = MagicMock()
    container.customer.verify_organization_registry_usecase.side_effect = provide_usecase
    return {"container": container, "job_try": job_try}


class TestVerifyOrganizationRegistryTask:
    @pytest.mark.unit
    async def test_runs_use_case_with_uuid(self):
        usecase = AsyncMock()
        organization_id = uuid.uuid4()

        await verify_organization_registry(make_ctx(usecase), str(organization_id))

        usecase.execute.assert_awaited_once_with(organization_id)

    @pytest.mark.unit
    async def test_builds_a_fresh_use_case_per_job(self):
        ctx = make_ctx(AsyncMock())

        await verify_organization_registry(ctx, str(uuid.uuid4()))
        await verify_organization_registry(ctx, str(uuid.uuid4()))

        assert ctx["container"].customer.verify_organization_registry_usecase.call_count == 2

    @pytest.mark.unit
    @pytest.mark.parametrize(("job_try", "delay"), [(1, 60), (2, 120), (3, 240), (4, 480), (6, 1800)])
    async def test_registry_unavailable_retries_with_backoff(self, job_try, delay):
        usecase = AsyncMock()
        usecase.execute.side_effect = TaxpayerRegistryUnavailableError()

        with pytest.raises(Retry) as exc_info:
            await verify_organization_registry(make_ctx(usecase, job_try=job_try), str(uuid.uuid4()))

        assert exc_info.value.defer_score == delay * 1000

    @pytest.mark.unit
    async def test_other_errors_are_not_retried(self):
        usecase = AsyncMock()
        usecase.execute.side_effect = RuntimeError("bug")

        with pytest.raises(RuntimeError):
            await verify_organization_registry(make_ctx(usecase), str(uuid.uuid4()))
