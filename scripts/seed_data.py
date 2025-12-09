# from src.configuration.dependencies.depends import DependencyContainer
# from src.core.listings.domain.enums import MachinerySpecsValueTypeEnum
#
# from src.core.users.infrastructure.models import User, UserProfile, BusinessDetails
# from src.core.listings.infrastructure.models.listing import Listing, ListingMedia
# from src.core.listings.infrastructure.models.machinery import MachinerySpecification, MachinerySubcategorySpecification
#
# from src.core.listings.infrastructure.models.references import (
#     Roubric,
#     MachineryCategory,
#     MachinerySubcategory,
#     UnitOfMeasure,
#     MachineryManufacturer,
#     MachineryManufacturerCountry
# )
#
# from src.core.shared.infrastructure.shared_models import Region, Color
#
#
# async def seed_data(container: DependencyContainer):
#     async_session_maker = container.async_session_maker()
#     async with async_session_maker() as session:
#         roubric = Roubric(name="Техника")
#         session.add(roubric)
#         await session.flush()
#
#         tractors = MachineryCategory(roubric_id=roubric.id, name="Тракторы")
#         harvesters = MachineryCategory(roubric_id=roubric.id, name="Комбайны")
#         tillage = MachineryCategory(roubric_id=roubric.id, name="Почвообрабатывающая техника")
#         seeding = MachineryCategory(roubric_id=roubric.id, name="Посевная и посадочная техника")
#         protection = MachineryCategory(roubric_id=roubric.id, name="Техника для защиты растений")
#         irrigation = MachineryCategory(roubric_id=roubric.id, name="Техника для полива и орошения")
#         vehicles = MachineryCategory(roubric_id=roubric.id, name="Автотранспорт")
#         loaders = MachineryCategory(roubric_id=roubric.id, name="Погрузочная техника")
#         innovation = MachineryCategory(roubric_id=roubric.id, name="Инновационная техника")
#
#         session.add_all([
#             tractors,
#             harvesters,
#             tillage,
#             seeding,
#             protection,
#             irrigation,
#             vehicles,
#             loaders,
#             innovation
#         ])
#         await session.flush()
#
#         wheeled_tractors = MachinerySubcategory(category_id=tractors.id, name="Колесные тракторы")
#         tracked_tractors = MachinerySubcategory(category_id=tractors.id, name="Гусеничные тракторы")
#         mini_tractors = MachinerySubcategory(category_id=tractors.id, name="Мини-тракторы")
#
#         grain_combines = MachinerySubcategory(category_id=harvesters.id, name="Зерноуборочные комбайны")
#         forage_combines = MachinerySubcategory(category_id=harvesters.id, name="Кормоуборочные комбайны")
#         potato_combines = MachinerySubcategory(category_id=harvesters.id, name="Картофелеуборочные комбайны")
#         beet_combines = MachinerySubcategory(category_id=harvesters.id, name="Свеклоуборочные комбайны")
#
#         harrows = MachinerySubcategory(category_id=tillage.id, name="Бороны")
#         ploughs = MachinerySubcategory(category_id=tillage.id, name="Плуги")
#         subsoiler = MachinerySubcategory(category_id=tillage.id, name="Глубокорыхлители")
#         cultivators = MachinerySubcategory(category_id=tillage.id, name="Культиваторы")
#         stone_removers = MachinerySubcategory(category_id=tillage.id, name="Камнеуборочные машины")
#         rollers = MachinerySubcategory(category_id=tillage.id, name="Катки")
#
#         seeders = MachinerySubcategory(category_id=seeding.id, name="Сеялки")
#         planters = MachinerySubcategory(category_id=seeding.id, name="Сажалки")
#
#         self_propelled_sprayers = MachinerySubcategory(category_id=protection.id, name="Опрыскиватели самоходные")
#         trailer_sprayers = MachinerySubcategory(category_id=protection.id, name="Опрыскиватели прицепные")
#         mounted_sprayers = MachinerySubcategory(category_id=protection.id, name="Опрыскиватели навесные")
#         fertilizer_spreaders = MachinerySubcategory(category_id=protection.id, name="Разбрасыватели удобрений")
#
#         irrigation_machines = MachinerySubcategory(category_id=irrigation.id, name="Дождевальные машины")
#         drip_irrigations = MachinerySubcategory(category_id=irrigation.id, name="Системы капельного орошения")
#         pump_stations = MachinerySubcategory(category_id=irrigation.id, name="Насосные станции")
#
#         trucks = MachinerySubcategory(category_id=vehicles.id, name="Грузовой транспорт")
#         cars = MachinerySubcategory(category_id=vehicles.id, name="Легковой транспорт")
#         bus = MachinerySubcategory(category_id=vehicles.id, name="Автобусы")
#         tankers = MachinerySubcategory(category_id=vehicles.id, name="Автоцистерны")
#
#         front_loaders = MachinerySubcategory(category_id=loaders.id, name="Фронтальные погрузчики")
#         telehandlers = MachinerySubcategory(category_id=loaders.id, name="Телескопические погрузчики")
#         mini_loaders = MachinerySubcategory(category_id=loaders.id, name="Мини-погрузчики")
#
#         drones = MachinerySubcategory(category_id=innovation.id, name="Дроны")
#         robotics = MachinerySubcategory(category_id=innovation.id, name="Робототехника")
#         agroaviation = MachinerySubcategory(category_id=innovation.id, name="Агроавиация")
#
#         session.add_all([
#             wheeled_tractors,
#             tracked_tractors,
#             mini_tractors,
#
#             grain_combines,
#             forage_combines,
#             potato_combines,
#             beet_combines,
#
#             harrows,
#             ploughs,
#             subsoiler,
#             cultivators,
#             stone_removers,
#             rollers,
#
#             seeders,
#             planters,
#
#             self_propelled_sprayers,
#             trailer_sprayers,
#             mounted_sprayers,
#             fertilizer_spreaders,
#
#             irrigation_machines,
#             drip_irrigations,
#             pump_stations,
#
#             trucks,
#             cars,
#             bus,
#             tankers,
#
#             front_loaders,
#             telehandlers,
#             mini_loaders,
#
#             drones,
#             robotics,
#             agroaviation
#         ])
#         await session.flush()
#
#         horsepower = UnitOfMeasure(name="h.p", label="л.с.")
#         kilowatt = UnitOfMeasure(name="kW", label="кВт")
#         meter = UnitOfMeasure(name="m", label="м")
#         millimeter = UnitOfMeasure(name="mm", label="мм")
#         centimeter = UnitOfMeasure(name="cm", label="см")
#         cubic_meter = UnitOfMeasure(name="m³", label="м³")
#         liter = UnitOfMeasure(name="l", label="л")
#         kilogram = UnitOfMeasure(name="kg", label="кг")
#         ton = UnitOfMeasure(name="t", label="т")
#         rpm = UnitOfMeasure(name="rpm", label="об/мин")
#         unit = UnitOfMeasure(name="unit", label="шт")
#         newton_meter = UnitOfMeasure(name="Nm", label="Нм")
#         kilometer_per_hour = UnitOfMeasure(name="km/h", label="км/ч")
#         percent = UnitOfMeasure(name="%", label="%")
#         liter_per_hour = UnitOfMeasure(name="l/h", label="л/ч")
#         kpa = UnitOfMeasure(name="KPa", label="КПа")
#         hour = UnitOfMeasure(name="h", label="ч")
#
#         session.add_all([
#             horsepower,
#             kilowatt,
#             meter,
#             millimeter,
#             centimeter,
#             cubic_meter,
#             liter,
#             kilogram,
#             ton,
#             rpm,
#             unit,
#             newton_meter,
#             kilometer_per_hour,
#             percent,
#             liter_per_hour,
#             kpa
#         ])
#         await session.flush()
#
#         manufacturers = [
#             MachineryManufacturer(name="John Deere"),
#             MachineryManufacturer(name="Claas"),
#             MachineryManufacturer(name="Case IH"),
#             MachineryManufacturer(name="New Holland"),
#             MachineryManufacturer(name="Rostselmash"),
#             MachineryManufacturer(name="Belarus"),
#             MachineryManufacturer(name="Yamato"),
#             MachineryManufacturer(name="Deutz-Fahr"),
#         ]
#
#         session.add_all(manufacturers)
#         await session.flush()
#
#         manufacturer_countries = [
#             MachineryManufacturerCountry(name="США"),
#             MachineryManufacturerCountry(name="Казахстан"),
#             MachineryManufacturerCountry(name="Япония"),
#             MachineryManufacturerCountry(name="Россия"),
#             MachineryManufacturerCountry(name="Польша"),
#             MachineryManufacturerCountry(name="Великобритания"),
#         ]
#
#         session.add_all(manufacturer_countries)
#         await session.flush()
#
#         regions = [
#             Region(name="Астана"),
#             Region(name="Алматы"),
#             Region(name="Шымкент"),
#             Region(name="Павлодар"),
#             Region(name="Актау"),
#             Region(name="Кокшетау"),
#             Region(name="Семей"),
#         ]
#
#         session.add_all(regions)
#         await session.flush()
#
#         colors = [
#             Color(name="Черный", hex="#000000"),
#             Color(name="Белый", hex="#FFFFFF"),
#             Color(name="Красный", hex="#FF0000"),
#             Color(name="Синий", hex="#0000FF"),
#             Color(name="Желтый", hex="#FFFF00"),
#             Color(name="Зеленый", hex="#008000"),
#         ]
#
#         session.add_all(colors)
#         await session.flush()
#
#         rpm_pto = MachinerySpecification(
#             key="rpm_pto",
#             label="Частота вращения ВОМ",
#             value_type=MachinerySpecsValueTypeEnum.ENUM,
#             options=["540/1000", "540", "1000"]
#         )
#         counterweight_mass = MachinerySpecification(
#             key="counterweight_mass",
#             label="Противовес",
#             value_type=MachinerySpecsValueTypeEnum.INTEGER
#         )
#         min_turn_radius = MachinerySpecification(
#             key="min_turn_radius",
#             label="Наименьший радиус поворота",
#             value_type=MachinerySpecsValueTypeEnum.INTEGER
#         )
#         length = MachinerySpecification(
#             key="length",
#             label="Длина",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         width = MachinerySpecification(
#             key="width",
#             label="Ширина",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         height = MachinerySpecification(
#             key="height",
#             label="Высота",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         weight = MachinerySpecification(
#             key="weight",
#             label="Вес",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         fuel_system = MachinerySpecification(
#             key="fuel_system",
#             label="Топливная система",
#             value_type=MachinerySpecsValueTypeEnum.ENUM,
#             options=["Бензин", "Дизель", "Газ", "Электро", "Гибрид", "Газодизель"]
#         )
#         engine_power = MachinerySpecification(
#             key="engine_power",
#             label="Мощность двигателя",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         torque = MachinerySpecification(
#             key="torque",
#             label="Крутящий момент",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         engine_volume = MachinerySpecification(
#             key="engine_volume",
#             label="Объём двигателя",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         cylinder_count = MachinerySpecification(
#             key="cylinder_count",
#             label="Количество цилиндров",
#             value_type=MachinerySpecsValueTypeEnum.INTEGER
#         )
#         fuel_consumption = MachinerySpecification(
#             key="fuel_consumption",
#             label="Расход топлива",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         tank_volume = MachinerySpecification(
#             key="tank_volume",
#             label="Объём бака",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         transmission_type = MachinerySpecification(
#             key="transmission_type",
#             label="Коробка передач",
#             value_type=MachinerySpecsValueTypeEnum.ENUM,
#             options=["Механика", "Автомат", "Робот"]
#         )
#         reverser = MachinerySpecification(
#             key="reverser",
#             label="Реверсивный ход",
#             value_type=MachinerySpecsValueTypeEnum.ENUM,
#             options=["Есть", "Нет"]
#         )
#         suspension = MachinerySpecification(
#             key="suspension",
#             label="Подвеска",
#             value_type=MachinerySpecsValueTypeEnum.ENUM,
#             options=["Жесткая", "Пружинная", "Гидравлическая", "Пневматическая"]
#         )
#         drive_type = MachinerySpecification(
#             key="drive_type",
#             label="Тип привода",
#             value_type=MachinerySpecsValueTypeEnum.ENUM,
#             options=["Полный", "Задний", "Передний"]
#         )
#         wheel_formula = MachinerySpecification(
#             key="wheel_formula",
#             label="Колесная формула",
#             value_type=MachinerySpecsValueTypeEnum.ENUM,
#             options=["4х4", "6х6", "4х2"]
#         )
#         front_tire_size = MachinerySpecification(
#             key="front_tire_size",
#             label="Размер шин спереди",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         rear_tire_size = MachinerySpecification(
#             key="rear_tire_size",
#             label="Размер шин сзади",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         front_tread_depth = MachinerySpecification(
#             key="front_tread_depth",
#             label="Остаток протектора спереди",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         rear_tread_depth = MachinerySpecification(
#             key="rear_tread_depth",
#             label="Остаток протектора сзади",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         wheel_track_width = MachinerySpecification(
#             key="wheel_track_width",
#             label="Колея",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         ground_clearance = MachinerySpecification(
#             key="ground_clearance",
#             label="Дорожный просвет",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         reverse_gears_count = MachinerySpecification(
#             key="reverse_gears_count",
#             label="Количество передач заднего хода",
#             value_type=MachinerySpecsValueTypeEnum.INTEGER
#         )
#         front_gears_count = MachinerySpecification(
#             key="front_gears_count",
#             label="Количество передач переднего хода",
#             value_type=MachinerySpecsValueTypeEnum.INTEGER
#         )
#         track_type = MachinerySpecification(
#             key="track_type",
#             label="Тип гусениц",
#             value_type=MachinerySpecsValueTypeEnum.ENUM,
#             options=["Резиновые", "Металлические"]
#         )
#         track_belt_width = MachinerySpecification(
#             key="track_belt_width",
#             label="Ширина гусениц",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         ground_pressure = MachinerySpecification(
#             key="ground_pressure",
#             label="Давление на грунт",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         engine_hours = MachinerySpecification(
#             key="engine_hours",
#             label="Моточасы",
#             value_type=MachinerySpecsValueTypeEnum.INTEGER
#         )
#         mileage = MachinerySpecification(
#             key="mileage",
#             label="Пробег",
#             value_type=MachinerySpecsValueTypeEnum.INTEGER
#         )
#         swath_width = MachinerySpecification(
#             key="swath_width",
#             label="Ширина захвата",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         row_spacing = MachinerySpecification(
#             key="row_spacing",
#             label="Ширина междурядий",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         rows_count = MachinerySpecification(
#             key="rows_count",
#             label="Количество рядов",
#             value_type=MachinerySpecsValueTypeEnum.INTEGER
#         )
#         hopper_volume = MachinerySpecification(
#             key="hopper_volume",
#             label="Объем бункера",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         drum_width = MachinerySpecification(
#             key="drum_width",
#             label="Ширина барабана",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         drum_diameter = MachinerySpecification(
#             key="drum_diameter",
#             label="Диаметр барабана",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         header_type = MachinerySpecification(
#             key="header_type",
#             label="Тип жатки",
#             value_type=MachinerySpecsValueTypeEnum.ENUM,
#             options=["Зерновая", "Рапсовая", "Кукурузная", "Подсолнечная"]
#         )
#         performance = MachinerySpecification(
#             key="performance",
#             label="Производительность",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         drum_hours = MachinerySpecification(
#             key="drum_hours",
#             label="Моточасы барабана",
#             value_type=MachinerySpecsValueTypeEnum.INTEGER
#         )
#         knife_count = MachinerySpecification(
#             key="knife_count",
#             label="Количество ножей",
#             value_type=MachinerySpecsValueTypeEnum.INTEGER
#         )
#         chopper_type = MachinerySpecification(
#             key="chopper_type",
#             label="Тип измельчителя",
#             value_type=MachinerySpecsValueTypeEnum.ENUM,
#             options=["Роторный", "Барабанный", "Дисковый", "Ножевой"]
#         )
#         chopper_drum_width = MachinerySpecification(
#             key="chopper_drum_width",
#             label="Ширина измельчающего барабана",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#         chopper_drum_diameter = MachinerySpecification(
#             key="chopper_drum_diameter",
#             label="Диаметр измельчающего барабана",
#             value_type=MachinerySpecsValueTypeEnum.FLOAT
#         )
#
#         session.add_all([
#             rpm_pto,
#             counterweight_mass,
#             min_turn_radius,
#             length,
#             width,
#             height,
#             weight,
#             fuel_system,
#             engine_power,
#             torque,
#             engine_volume,
#             cylinder_count,
#             fuel_consumption,
#             tank_volume,
#             transmission_type,
#             reverser,
#             suspension,
#             drive_type,
#             wheel_formula,
#             front_tire_size,
#             rear_tire_size,
#             front_tread_depth,
#             rear_tread_depth,
#             wheel_track_width,
#             ground_clearance,
#             reverse_gears_count,
#             front_gears_count,
#             track_type,
#             track_belt_width,
#             ground_pressure,
#             engine_hours,
#             mileage,
#             swath_width,
#             row_spacing,
#             rows_count,
#             hopper_volume,
#             drum_width,
#             drum_diameter,
#             header_type,
#             performance,
#             drum_hours,
#             knife_count,
#             chopper_type,
#             chopper_drum_width,
#             chopper_drum_diameter
#         ])
#         await session.flush()
#
#         subcategory_specifications = [
#             # Колесные Тракторы
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=rpm_pto.id,
#                 unit_id=rpm.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=counterweight_mass.id,
#                 unit_id=kilogram.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=min_turn_radius.id,
#                 unit_id=meter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=length.id,
#                 unit_id=millimeter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=width.id,
#                 unit_id=millimeter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=height.id,
#                 unit_id=millimeter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=weight.id,
#                 unit_id=kilogram.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=fuel_system.id,
#                 unit_id=None,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=engine_power.id,
#                 unit_id=horsepower.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=engine_power.id,
#                 unit_id=kilowatt.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=torque.id,
#                 unit_id=newton_meter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=engine_volume.id,
#                 unit_id=liter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=cylinder_count.id,
#                 unit_id=unit.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=fuel_consumption.id,
#                 unit_id=liter_per_hour.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=tank_volume.id,
#                 unit_id=liter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=transmission_type.id,
#                 unit_id=None,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=reverser.id,
#                 unit_id=None,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=front_tire_size.id,
#                 unit_id=millimeter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=suspension.id,
#                 unit_id=None,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=drive_type.id,
#                 unit_id=None,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=wheel_formula.id,
#                 unit_id=None,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=rear_tire_size.id,
#                 unit_id=millimeter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=front_tread_depth.id,
#                 unit_id=percent.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=rear_tread_depth.id,
#                 unit_id=percent.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=wheel_track_width.id,
#                 unit_id=millimeter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=ground_clearance.id,
#                 unit_id=centimeter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=reverse_gears_count.id,
#                 unit_id=unit.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=wheeled_tractors.id,
#                 specification_id=front_gears_count.id,
#                 unit_id=unit.id,
#                 is_required=False
#             ),
#
#             # ГУСЕНИЧНЫЕ ТРАКТОРЫ
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=track_type.id,
#                 unit_id=None,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=track_belt_width.id,
#                 unit_id=millimeter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=ground_pressure.id,
#                 unit_id=kpa.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=engine_hours.id,
#                 unit_id=hour.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=rpm_pto.id,
#                 unit_id=rpm.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=counterweight_mass.id,
#                 unit_id=kilogram.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=min_turn_radius.id,
#                 unit_id=meter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=length.id,
#                 unit_id=millimeter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=width.id,
#                 unit_id=millimeter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=height.id,
#                 unit_id=millimeter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=weight.id,
#                 unit_id=kilogram.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=fuel_system.id,
#                 unit_id=None,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=engine_power.id,
#                 unit_id=horsepower.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=engine_power.id,
#                 unit_id=kilowatt.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=torque.id,
#                 unit_id=newton_meter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=engine_volume.id,
#                 unit_id=liter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=cylinder_count.id,
#                 unit_id=unit.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=fuel_consumption.id,
#                 unit_id=liter_per_hour.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=tank_volume.id,
#                 unit_id=liter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=transmission_type.id,
#                 unit_id=None,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=reverser.id,
#                 unit_id=None,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=ground_clearance.id,
#                 unit_id=centimeter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=reverse_gears_count.id,
#                 unit_id=unit.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=tracked_tractors.id,
#                 specification_id=front_gears_count.id,
#                 unit_id=unit.id,
#                 is_required=False
#             ),
#
#             # ЗЕРНОУБОРОЧНЫЕ КОМБАЙНЫ
#             MachinerySubcategorySpecification(
#                 subcategory_id=grain_combines.id,
#                 specification_id=engine_hours.id,
#                 unit_id=hour.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=grain_combines.id,
#                 specification_id=swath_width.id,
#                 unit_id=meter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=grain_combines.id,
#                 specification_id=hopper_volume.id,
#                 unit_id=cubic_meter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=grain_combines.id,
#                 specification_id=drum_width.id,
#                 unit_id=meter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=grain_combines.id,
#                 specification_id=drum_diameter.id,
#                 unit_id=meter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=grain_combines.id,
#                 specification_id=drum_hours.id,
#                 unit_id=hour.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=grain_combines.id,
#                 specification_id=width.id,
#                 unit_id=millimeter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=grain_combines.id,
#                 specification_id=height.id,
#                 unit_id=millimeter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=grain_combines.id,
#                 specification_id=length.id,
#                 unit_id=millimeter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=grain_combines.id,
#                 specification_id=weight.id,
#                 unit_id=kilogram.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=grain_combines.id,
#                 specification_id=engine_power.id,
#                 unit_id=horsepower.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=grain_combines.id,
#                 specification_id=engine_power.id,
#                 unit_id=kilowatt.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=grain_combines.id,
#                 specification_id=fuel_system.id,
#                 unit_id=None,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=grain_combines.id,
#                 specification_id=torque.id,
#                 unit_id=newton_meter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=grain_combines.id,
#                 specification_id=engine_volume.id,
#                 unit_id=liter.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=grain_combines.id,
#                 specification_id=fuel_consumption.id,
#                 unit_id=liter_per_hour.id,
#                 is_required=False
#             ),
#             MachinerySubcategorySpecification(
#                 subcategory_id=grain_combines.id,
#                 specification_id=cylinder_count.id,
#                 unit_id=unit.id,
#                 is_required=False
#             ),
#         ]
#
#         session.add_all(subcategory_specifications)
#         await session.commit()
#
#
