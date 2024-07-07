"""Growatt Sensor definitions for the Storage type."""

from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
)

from .sensor_entity_description import GrowattSensorEntityDescription

STORAGE_SENSOR_TYPES: tuple[GrowattSensorEntityDescription, ...] = (
    GrowattSensorEntityDescription(
        key="storage_storage_production_today",
        translation_key="storage_storage_production_today",
        api_key="eBatDisChargeToday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
    ),
    GrowattSensorEntityDescription(
        key="storage_storage_production_lifetime",
        translation_key="storage_storage_production_lifetime",
        api_key="eBatDisChargeTotal",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
    ),
    GrowattSensorEntityDescription(
        key="storage_grid_discharge_today",
        translation_key="storage_grid_discharge_today",
        api_key="eacDisChargeToday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
    ),
    GrowattSensorEntityDescription(
        key="storage_load_consumption_today",
        translation_key="storage_load_consumption_today",
        api_key="eopDischrToday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
    ),
    GrowattSensorEntityDescription(
        key="storage_load_consumption_lifetime",
        translation_key="storage_load_consumption_lifetime",
        api_key="eopDischrTotal",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
    ),
    GrowattSensorEntityDescription(
        key="storage_grid_charged_today",
        translation_key="storage_grid_charged_today",
        api_key="eacChargeToday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
    ),
    GrowattSensorEntityDescription(
        key="storage_charge_storage_lifetime",
        translation_key="storage_charge_storage_lifetime",
        api_key="eChargeTotal",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
    ),
    GrowattSensorEntityDescription(
        key="storage_solar_production",
        translation_key="storage_solar_production",
        api_key="ppv",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    GrowattSensorEntityDescription(
        key="storage_solar_production_2",
        translation_key="storage_solar_production_2",
        api_key="ppv2",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    GrowattSensorEntityDescription(
        key="storage_battery_percentage",
        translation_key="storage_battery_percentage",
        api_key="capacity",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
    ),
    GrowattSensorEntityDescription(
        key="storage_power_flow",
        translation_key="storage_power_flow",
        api_key="pCharge",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    GrowattSensorEntityDescription(
        key="storage_load_consumption_solar_storage",
        translation_key="storage_load_consumption_solar_storage",
        api_key="rateVA",
        native_unit_of_measurement="VA",
    ),
    GrowattSensorEntityDescription(
        key="storage_charge_today",
        translation_key="storage_charge_today",
        api_key="eChargeToday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
    ),
    GrowattSensorEntityDescription(
        key="storage_import_from_grid",
        translation_key="storage_import_from_grid",
        api_key="pAcInPut",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    GrowattSensorEntityDescription(
        key="storage_import_from_grid_today",
        translation_key="storage_import_from_grid_today",
        api_key="eToUserToday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
    ),
    GrowattSensorEntityDescription(
        key="storage_import_from_grid_total",
        translation_key="storage_import_from_grid_total",
        api_key="eToUserTotal",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
    ),
    GrowattSensorEntityDescription(
        key="storage_load_consumption",
        translation_key="storage_load_consumption",
        api_key="outPutPower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    GrowattSensorEntityDescription(
        key="storage_grid_voltage",
        translation_key="storage_grid_voltage",
        api_key="vGrid",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        precision=2,
    ),
    GrowattSensorEntityDescription(
        key="storage_pv_charging_voltage",
        translation_key="storage_pv_charging_voltage",
        api_key="vpv",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        precision=2,
    ),
    GrowattSensorEntityDescription(
        key="storage_ac_input_frequency_out",
        translation_key="storage_ac_input_frequency_out",
        api_key="freqOutPut",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        precision=2,
    ),
    GrowattSensorEntityDescription(
        key="storage_output_voltage",
        translation_key="storage_output_voltage",
        api_key="outPutVolt",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        precision=2,
    ),
    GrowattSensorEntityDescription(
        key="storage_ac_output_frequency",
        translation_key="storage_ac_output_frequency",
        api_key="freqGrid",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        precision=2,
    ),
    GrowattSensorEntityDescription(
        key="storage_current_PV",
        translation_key="storage_current_pv",
        api_key="iAcCharge",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        precision=2,
    ),
    GrowattSensorEntityDescription(
        key="storage_current_1",
        translation_key="storage_current_1",
        api_key="iChargePV1",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        precision=2,
    ),
    GrowattSensorEntityDescription(
        key="storage_grid_amperage_input",
        translation_key="storage_grid_amperage_input",
        api_key="chgCurr",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        precision=2,
    ),
    GrowattSensorEntityDescription(
        key="storage_grid_out_current",
        translation_key="storage_grid_out_current",
        api_key="outPutCurrent",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        precision=2,
    ),
    GrowattSensorEntityDescription(
        key="storage_battery_voltage",
        translation_key="storage_battery_voltage",
        api_key="vBat",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        precision=2,
    ),
    GrowattSensorEntityDescription(
        key="storage_load_percentage",
        translation_key="storage_load_percentage",
        api_key="loadPercent",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        precision=2,
    ),
)
