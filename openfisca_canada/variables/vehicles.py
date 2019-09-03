# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, a Household…
# See https://openfisca.org/doc/key-concepts/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_canada.entities import *

# Possible values for the procurement_type variable, defined further down
# See more at <https://openfisca.org/doc/coding-the-legislation/20_input_variables.html#advanced-example-enumerations-enum>
class ProcurementType(Enum):
    __order__ = "crown lease private none"
    crown = u'Crown'
    lease = u'Lease'
    private = u'Private'
    none = u'none'

class procurement_type(Variable):
    value_type = Enum
    possible_values = ProcurementType
    default_value = ProcurementType.none
    entity = Vehicle
    definition_period = MONTH
    label = u"Whether the vehicle is owned by the crown, leased or a private vehicle owned by the employee."

class vehicle_is_insured(Variable):
    value_type = bool
    entity = Vehicle
    definition_period = MONTH
    label = "vehicle would be insured"

    def formula(vehicle, period, parameters):
        procurement_type = vehicle('procurement_type', period).decode_to_str()
        return select(
            [
                procurement_type == 'crown',
                procurement_type == 'lease',
                procurement_type == 'private'
            ],
            [
                # Logic for Crown owned vehicle
                not_(vehicle('travelling_to_usa', period)) +
                (vehicle('commercial_insurance_purchased', period) * vehicle('travelling_to_usa', period)),
                # Logic for leased vehicle
                not_(vehicle('travelling_to_usa', period)) +
                (vehicle('commercial_insurance_purchased', period) * vehicle('travelling_to_usa', period)),
                # Logic for private vehicle
                vehicle('basic_insurance_coverage', period)
            ]
        )

class collision_damage_waiver(Variable):
    value_type = bool
    entity = Vehicle
    definition_period = MONTH
    label = "Collision Damage Waiver (CDW) coverage"
    def formula(vehicle, period, parameters):
        return (
            vehicle('dtec_used', period) +
            vehicle('idtc_used', period) +
            vehicle('personal_card_collision_damage_waiver', period) +
            (vehicle('procurement_type', period) == ProcurementType.crown)
        )

class public_liability_and_property_damage(Variable):
    value_type = bool
    entity = Vehicle
    definition_period = MONTH
    label = "Public Liability and Property Damage coverage"

    def formula(vehicle, period, parameters):
        return (
            vehicle('government_approved_car_rental_suppliers', period) +
            (vehicle('travelling_outside_of_canada', period) * vehicle('commercial_public_liability_purchased', period)) +
            vehicle('basic_insurance_coverage', period) +
            (vehicle('procurement_type', period) == ProcurementType.crown)
        )

class dtec_used(Variable):
    value_type = bool
    entity = Vehicle
    definition_period = MONTH
    label = "did the user use their dtec card for the purchase?"

class idtc_used(Variable):
    value_type = bool
    entity = Vehicle
    definition_period = MONTH
    label = "did the user use their idtc card for the purchase?"

class personal_card_used(Variable):
    value_type = bool
    entity = Vehicle
    definition_period = MONTH
    label = "did the user use their personal card for the purchase?"

class personal_card_collision_damage_waiver(Variable):
    value_type = bool
    entity = Vehicle
    definition_period = MONTH
    label = "did the users personal card have Collision Damage Waiver?"

class government_approved_car_rental_suppliers(Variable):
    value_type = bool
    entity = Vehicle
    definition_period = MONTH
    label = "did the user use a government approved car rental supplier?"

class public_liability_and_property_damage_purchased(Variable):
    value_type = bool
    entity = Vehicle
    definition_period = MONTH
    label = "did the user purchase public liability and property damage?"

class travelling_to_usa(Variable):
    value_type = bool
    entity = Vehicle
    definition_period = MONTH
    label = "is the vehicle going to the USA?"

class travelling_outside_of_canada(Variable):
    value_type = bool
    entity = Vehicle
    definition_period = MONTH
    label = "is the vehicle travelling outside of canada?"

class commercial_insurance_purchased(Variable):
    value_type = bool
    entity = Vehicle
    definition_period = MONTH
    label = "Has commercial insurance been purchased?"

class commercial_public_liability_purchased(Variable):
    value_type = bool
    entity = Vehicle
    definition_period = MONTH
    label = "Public Liability and Property Damage been purchased?"


# For private vehicle only
class basic_insurance_coverage(Variable):
    value_type = bool
    entity = Vehicle
    definition_period = MONTH
    label = "does the user have basic insurance coverage?"

# For private vehicle only
class commercical_insurance_purchased(Variable):
    value_type = bool
    entity = Vehicle
    definition_period = MONTH
    label = "Was commercial insurance purchased?"