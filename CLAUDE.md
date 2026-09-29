# Sievers Market: Backend

B2B agri marketplace for Kazakhstan (machinery and raw materials).
FastAPI, DDD + Clean Architecture, modular monolith. Python 3.11.

## Stack
- PostgreSQL (SQLAlchemy async, Alembic migrations)
- Redis, ARQ (background jobs)
- MinIO (files), Meilisearch (search), Resend (email), Sentry
- dependency-injector for DI
- API docs: Swagger at `/docs`, Scalar at `/scalar`

## Structure
- Bounded contexts live in `src/core/`: `iam`, `customer`, `vendor`, `listing`, `media`, `admin`, `catalog`, `references`, `shared`.
- Each context is split into layers, dependencies pointing inward:
  `domain` -> `app` -> `infrastructure` (models, mapper, repository, uow) -> `presentation` (router, dto, dependencies, documentation).
- `catalog` and `references` are lookup contexts (brands, cities) and have only `infrastructure` and `presentation`.
- `shared` holds the base UoW, generic repositories and security.
- DI: `ApplicationContainer` in `src/configuration/dependencies/container.py` composes one sub-container per context.

## Commands
- `make up`: start the dev environment.
- `make ci`: start isolated services and run the test suite (same as CI).
- CI (GitHub Actions): `ci.yml` runs pre-commit, then `make ci`. Also `cd.yml` and release-please.
- Seeds are YAML files in `scripts/seeds/`; Bloom filter scripts are in `scripts/bloom/`.

## Architecture rules
Architecture decisions are recorded as ADRs (see the repo's ADR directory). Read the relevant one before changing a pattern.
- **Unit of Work per context (ADR 001).** Use cases run inside `async with self.uow as uow:`. Check ADR 001 before changing who commits.
- **Roles by profile record (ADR 003).** A user's role is defined by the existence of a profile record. `get_current_vendor`, `get_current_customer` and `get_current_admin` (in `src/core/shared/presentation`) load the profile and return 403 if it is missing.
- **Contexts talk through public services (ADR 004).** Example: `CustomerService` is injected into `vendor` via DI. Never import another context's repository or models.
- The per-request DB session is held in a `ContextVar`.
- Dynamic attributes are split in two. Attribute configuration (which attributes exist and their definitions) is stored in a relational model, not JSONB. Values entered by users (for example `engine_power: 123`) are stored as JSONB in `Listing.attributes`.
- OpenAPI endpoint descriptions live in each context's `presentation/documentation`, not inline in routers.

## Conventions
- Test files must be named `test_*.py`, otherwise pytest silently skips them.
- Keep business rules in the domain layer (aggregates and entities). Use cases orchestrate; they do not hold rules.
- Keep the OpenAPI spec accurate: status codes and error schemas must match real behavior, because the frontend builds Zod schemas from it.

## How to work with me
- Plan first. Say which files you will touch and why, and wait for approval before editing.
- Do not change logic or function signatures unless asked. For tasks like docstrings, only add documentation.
- After edits, list every changed file with a one-line reason.
- If you find a bug or a suspicious spot while working, report it and ask. Do not fix it silently.
- Explain non-obvious decisions briefly. I want to understand the code, not just receive it.
