# Changelog

## [4.4.0](https://github.com/sievers-kz/sievers-market-backend/compare/v4.3.0...v4.4.0) (2026-11-22)


### Features

* add Kind & OrganizationStatus enums ([7115f96](https://github.com/sievers-kz/sievers-market-backend/commit/7115f96d909b36543a9a940c5ad7d90b739e1347))
* **catalog:** full equipment tree with attributes per subcategory ([d8f2848](https://github.com/sievers-kz/sievers-market-backend/commit/d8f2848835bbbeec17b783c4c793966008265c43))
* **catalog:** full equipment tree with attributes per subcategory ([a2c513c](https://github.com/sievers-kz/sievers-market-backend/commit/a2c513cd2003cde8445ea1904b96d47040c61385))
* **customer:** add Organization aggregate ([cac56ca](https://github.com/sievers-kz/sievers-market-backend/commit/cac56cafbf198a861919904876413264a3731765))
* **customer:** add Organization mapper ([41cb70b](https://github.com/sievers-kz/sievers-market-backend/commit/41cb70be20e302aea22f6e9d898c0c4876529436))
* **customer:** add Organization model & remove avatar_url from Customer ([8639174](https://github.com/sievers-kz/sievers-market-backend/commit/86391744a33ade5c91aa8f93bdaae409f5c2f28f))
* **customer:** add organization repository ([d29be8f](https://github.com/sievers-kz/sievers-market-backend/commit/d29be8f45ec62a041131540b049e1c2962ade2ff))
* **customer:** admin confirmation of organization ownership ([33a7495](https://github.com/sievers-kz/sievers-market-backend/commit/33a749532117fd877861ed7d11873ba5f6a1a420))
* **customer:** admin confirmation of organization ownership ([07456a9](https://github.com/sievers-kz/sievers-market-backend/commit/07456a9ec4eca09313244d0964ebea55dce620eb))
* **customer:** fill organization legal_address from DaData registry ([28756ab](https://github.com/sievers-kz/sievers-market-backend/commit/28756abb8724795da4985904c97eaee1214e108b))
* **customer:** PATCH endpoints for organization shop name, contact phone and email ([b2d0b33](https://github.com/sievers-kz/sievers-market-backend/commit/b2d0b33de95e2cdb529afa8d64466b7af4af8ef1))
* **customer:** PATCH-эндпоинты названия магазина, телефона и email организации ([c6a6b97](https://github.com/sievers-kz/sievers-market-backend/commit/c6a6b9738905651ebb40220cb6499795ad92fcd8))
* **customer:** public sellers catalog ([58cdf65](https://github.com/sievers-kz/sievers-market-backend/commit/58cdf650a09c2ded8e8ffcc8e723bf33e0d5edb4))
* **customer:** public sellers catalog ([433c7e2](https://github.com/sievers-kz/sievers-market-backend/commit/433c7e2684cc8d4e50844446a2e6eb86e9d60bde))
* **customer:** replace vendor with organization and async registry verification ([4678f73](https://github.com/sievers-kz/sievers-market-backend/commit/4678f73d8b9bba30c828d38edb7afc455ab0bcbf))
* **customer:** require filled profile to publish, expose missing_fields ([483ccfd](https://github.com/sievers-kz/sievers-market-backend/commit/483ccfdaece2b2a986a840ce608d00f43abafbd3))
* **customer:** заполненный профиль обязателен для публикации, missing_fields в ответе ([7bd0770](https://github.com/sievers-kz/sievers-market-backend/commit/7bd0770ea2ea8de5a3ad4a5688e485321c9c7032))
* **customer:** заполнять legal_address организации из DaData ([902c5e7](https://github.com/sievers-kz/sievers-market-backend/commit/902c5e79d39535aa6236e0116f43e0b8f992173d))
* **customer:** каталог организаций с поиском ([bca7b24](https://github.com/sievers-kz/sievers-market-backend/commit/bca7b24f3abc31d4b4dd12652c3ab22957031ff6))
* **customer:** каталог организаций с поиском по названию ([b07108b](https://github.com/sievers-kz/sievers-market-backend/commit/b07108bbf621ab43d29a8efc3658d04b8bb3a9d7))
* **listing:** add GET /listing/my for the account listings page ([1a5f668](https://github.com/sievers-kz/sievers-market-backend/commit/1a5f6686a53fde51fc7f0ed7ef3034215f7784d7))
* **listing:** add GET /listing/my for the account listings page ([31e4c14](https://github.com/sievers-kz/sievers-market-backend/commit/31e4c14a237e85bf2613dd31db1456343fad7bd1))
* **listing:** create listings from an explicitly chosen organization ([b5c4b1a](https://github.com/sievers-kz/sievers-market-backend/commit/b5c4b1ad11c5c97eee2cb7de7ddb33da6c5c3d44))
* **listing:** create listings from an explicitly chosen organization ([3a3a732](https://github.com/sievers-kz/sievers-market-backend/commit/3a3a732f4c3e21089bc4336ca099710b36685079))
* **listing:** keep search index in sync with listing state ([20131f0](https://github.com/sievers-kz/sievers-market-backend/commit/20131f05241b2b8274b4eb774440530cc06119be))
* **listing:** keep search index in sync with listing state ([dade5b2](https://github.com/sievers-kz/sievers-market-backend/commit/dade5b2b4fa2eff2b51cc708884504a12a8e8c3f))
* **listing:** organization, condition and created_at in catalog card ([0d1d18d](https://github.com/sievers-kz/sievers-market-backend/commit/0d1d18d9d4b90e475ffa615f11eda769ac9d4a34))
* **listing:** search returns catalog cards ([48cf954](https://github.com/sievers-kz/sievers-market-backend/commit/48cf9543f013f4329ccb8c0e0ee877507aafdfa1))
* **listing:** search returns catalog cards ([db06450](https://github.com/sievers-kz/sievers-market-backend/commit/db06450dbde8f8f4431ddd0e8c06ccbaa9f851d8))
* **listing:** seller and display-ready specs in listing details ([c11cc39](https://github.com/sievers-kz/sievers-market-backend/commit/c11cc394ba091c9276b945f4530904fca4592897))
* **listing:** seller legal data, masked contacts and contacts endpoint ([590841f](https://github.com/sievers-kz/sievers-market-backend/commit/590841fa82e99f6e905966e9b455047bf6d627d2))
* **listing:** организация, состояние и дата в карточке каталога ([138d1ca](https://github.com/sievers-kz/sievers-market-backend/commit/138d1ca1d6ce1909099058116410945d859d1879))
* **listing:** продавец и характеристики в деталке объявления ([9194f45](https://github.com/sievers-kz/sievers-market-backend/commit/9194f45064a2cf884ef14d7fea667b3e6c672d8d))
* **listing:** юрданные продавца, маска контактов и /contacts ([84eb4be](https://github.com/sievers-kz/sievers-market-backend/commit/84eb4beac78c18e6030ca390a2faed8a0aa5e68e))
* **search:** full reindex script and text search on string attributes ([6dcf9ea](https://github.com/sievers-kz/sievers-market-backend/commit/6dcf9eaae9acc3f24d4478fbce14fa4971a1421d))
* **search:** full reindex script and text search on string attributes ([fe371fb](https://github.com/sievers-kz/sievers-market-backend/commit/fe371fbc56b9ee67d85bc9c4ea92c26267a2b046))
* **search:** numeric attribute ranges and KZT-only price comparison ([696238b](https://github.com/sievers-kz/sievers-market-backend/commit/696238bcfd4425f1b449844ff6c9fff86cfab674))
* **search:** numeric attribute ranges and KZT-only price comparison ([ba1fa64](https://github.com/sievers-kz/sievers-market-backend/commit/ba1fa64a562fc6077b4a507dda68d094099b5bed))


### Bug Fixes

* **api:** accept Kazakh letters in names and return error metadata ([a75feb8](https://github.com/sievers-kz/sievers-market-backend/commit/a75feb80dbaa5f1d74f1877dd7f5dee695b59a06))
* **api:** accept Kazakh letters in names and return error metadata ([8ede95b](https://github.com/sievers-kz/sievers-market-backend/commit/8ede95be31f5e3f93bf06f21283fd45e6bd31ceb))
* **api:** return error_code in domain exception responses ([b2186b8](https://github.com/sievers-kz/sievers-market-backend/commit/b2186b8cbc07a9795a808dbd4e1f54644308469c))
* **api:** return error_code in domain exception responses ([e32554d](https://github.com/sievers-kz/sievers-market-backend/commit/e32554d5c198d9a0963f416dfb8820e1a875871a)), closes [#201](https://github.com/sievers-kz/sievers-market-backend/issues/201)
* **catalog,listing:** объявления в подкатегориях без атрибутов и проверка ссылок на каталог ([e3b95be](https://github.com/sievers-kz/sievers-market-backend/commit/e3b95be5c10f84d300b1b96229e33c3b4b9e7b5b))
* **catalog:** allow listings for subcategories without attributes ([45c90e9](https://github.com/sievers-kz/sievers-market-backend/commit/45c90e9ae88a6a24ee3c83ec3c6a86994445a294))
* **listing:** select contacts from listings joined to organization ([e7019b4](https://github.com/sievers-kz/sievers-market-backend/commit/e7019b43f7be4ee17bd2214bca4e4f024d67bba1))
* **listing:** select organization_id in listing details query ([5f3e18f](https://github.com/sievers-kz/sievers-market-backend/commit/5f3e18f59e6037bd7911d6811b643a936c2b9fcf))
* **listing:** select organization_id in listing details query ([e21f8a6](https://github.com/sievers-kz/sievers-market-backend/commit/e21f8a6db449dcdbf1d4bd6afc03e19a367686da))
* **listing:** validate catalog references on create and change attributes ([cc779c9](https://github.com/sievers-kz/sievers-market-backend/commit/cc779c93a68ca5a8416ecfaad39a64a3d8eee977))
* **media:** sign presigned URLs with a public MinIO client and run blocking calls in threads ([3a81e9e](https://github.com/sievers-kz/sievers-market-backend/commit/3a81e9eb35e8ae56f368aa0e46f89dc23382ba2b))
* **media:** sign presigned URLs with a public MinIO client and run blocking calls in threads ([dc954f5](https://github.com/sievers-kz/sievers-market-backend/commit/dc954f51b78ddc99a2ce2d7c3f8463cd992170c0))
* **search:** escape and validate Meilisearch filter inputs ([d74caf3](https://github.com/sievers-kz/sievers-market-backend/commit/d74caf38879e0a862cbed8b7c6a17e92f3bda015))
* **search:** escape and validate Meilisearch filter inputs ([0455b56](https://github.com/sievers-kz/sievers-market-backend/commit/0455b5646e1c9d7008405399796b1380582f3b7b))
* **search:** pass catalog_service in schema sync script ([cad6942](https://github.com/sievers-kz/sievers-market-backend/commit/cad6942f78d0e1be57297aaaa0cc0a19f7091cf6))
* **search:** pass catalog_service in schema sync script ([882c0ac](https://github.com/sievers-kz/sievers-market-backend/commit/882c0ac355130ba1018f4b65c416229327c944e8))


### Documentation

* **customer:** document organization and profile endpoints ([63a1ca0](https://github.com/sievers-kz/sievers-market-backend/commit/63a1ca09a0f7185ec3ad06ccee9c36b176677d51))

## [4.3.0](https://github.com/sievers-kz/sievers-market-backend/compare/v4.2.0...v4.3.0) (2026-11-04)


### Features

* add healthcheck endpoint ([ab56de8](https://github.com/sievers-kz/sievers-market-backend/commit/ab56de82e9fc6bb997293f2860634cbe5117fdcf))
* add healthcheck endpoint ([faeebd6](https://github.com/sievers-kz/sievers-market-backend/commit/faeebd6db9221821d24dc301a22a08206cbb816a))
* add healthcheck endpoint ([ba4f87a](https://github.com/sievers-kz/sievers-market-backend/commit/ba4f87a0ba3307d35018bdda1018e184b3003f37))

## [4.2.0](https://github.com/sievers-kz/sievers-market-backend/compare/v4.1.0...v4.2.0) (2026-11-04)


### Features

* remove legacy deploy ([e974225](https://github.com/sievers-kz/sievers-market-backend/commit/e974225b7a5091d82e2053cc9a3d5d67193567f9))

## [4.1.0](https://github.com/sievers-kz/sievers-market-backend/compare/v4.0.0...v4.1.0) (2026-11-03)


### Features

* add trigger-deploy job to cd.yml to trigger CD workflow in siev… ([be33400](https://github.com/sievers-kz/sievers-market-backend/commit/be33400160bfe6e2327c393b18db8cd6050c9430))
* add trigger-deploy job to cd.yml to trigger CD workflow in sievers-infra repo ([fd8d887](https://github.com/sievers-kz/sievers-market-backend/commit/fd8d8879321fa135b4c58737a84cb406c94811c9))
* **cd:** remove deploy job from cd.yml and migrate to trigger deploy ([9a2565f](https://github.com/sievers-kz/sievers-market-backend/commit/9a2565f07116144ad702518f97ddff876b5d4b4c))
* **cd:** remove deploy job from cd.yml and migrate to trigger deploy ([9d7827c](https://github.com/sievers-kz/sievers-market-backend/commit/9d7827cb7d2c2fbcb699ae2e519f2369667de1b9))
* migrate to trigger deploy ([4ede029](https://github.com/sievers-kz/sievers-market-backend/commit/4ede029b01fc7ced2d6ebd45d51a3d3d1ce7b700))

## [4.0.0](https://github.com/sievers-kz/sievers-market-backend/compare/v3.0.0...v4.0.0) (2026-09-29)


### ⚠ BREAKING CHANGES

* **iam:** split change password into request and confirm endpoints. Closes #174

### Features

* **iam:** split change password into request and confirm endpoints. Closes [#174](https://github.com/sievers-kz/sievers-market-backend/issues/174) ([11debcf](https://github.com/sievers-kz/sievers-market-backend/commit/11debcf307c9e52c0092b6f0366bd417b9250e43))
* **versioning:** implement semantic versioning via release-please ([f819423](https://github.com/sievers-kz/sievers-market-backend/commit/f81942304184d370ae38a2b459020e9349523b95))
* **versioning:** implement semantic versioning via release-please ([5b0b2dc](https://github.com/sievers-kz/sievers-market-backend/commit/5b0b2dc54a2aed5f11114c939fe0818fc5e4c3b9))


### Bug Fixes

* **database:** switch session provider to callable & resolve race con… ([44c25af](https://github.com/sievers-kz/sievers-market-backend/commit/44c25af12f719ccd86860c6d014889e229647253))
* **database:** switch session provider to callable & resolve race conditions. Closes [#172](https://github.com/sievers-kz/sievers-market-backend/issues/172) ([0e7fb52](https://github.com/sievers-kz/sievers-market-backend/commit/0e7fb523854e0c245acb4b2ffbcd02ff482d387d))
* fix target-branch input name ([52c8428](https://github.com/sievers-kz/sievers-market-backend/commit/52c84288c9a4ec048dc5969a6fe5280de6e2d7ca))
* fix target-branch input name ([35a5309](https://github.com/sievers-kz/sievers-market-backend/commit/35a5309d56e4d263c650299e7680a75bccc4b194))
