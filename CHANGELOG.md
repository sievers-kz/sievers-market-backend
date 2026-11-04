# Changelog

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
