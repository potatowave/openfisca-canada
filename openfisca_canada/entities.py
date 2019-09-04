# -*- coding: utf-8 -*-

# This file defines the entities needed by our legislation.
from openfisca_core.entities import build_entity

Person = build_entity(
    key = "person",
    plural = "persons",
    label = u'An individual. The minimal legal entity on which a legislation might be applied.',
    doc = '''

    Variables like 'salary' and 'income_tax' are usually defined for the entity 'Person'.

    Usage:
    Calculate a variable applied to a 'Person' (e.g. access the 'salary' of a specific month with person('salary', "2017-05")).
    Check the role of a 'Person' in a group entity (e.g. check if a the 'Person' is a 'first_parent' in a 'Household' entity with person.has_role(Household.FIRST_PARENT)).

    For more information, see: https://openfisca.org/doc/coding-the-legislation/50_entities.html
    ''',
    is_person = True,
    )

Vehicle = build_entity(
    key = "vehicle",
    plural = "vehicles",
    label = u'.',
    doc = '''

    Variables like 'salary' and 'income_tax' are usually defined for the entity 'Person'.

    Usage:
    Calculate a variable applied to a 'Person' (e.g. access the 'salary' of a specific month with person('salary', "2017-05")).
    Check the role of a 'Person' in a group entity (e.g. check if a the 'Person' is a 'first_parent' in a 'Household' entity with person.has_role(Household.FIRST_PARENT)).

    For more information, see: https://openfisca.org/doc/coding-the-legislation/50_entities.html
    ''',

    roles = [
        {
            'key': 'parent',
            'plural': 'parents',
            'label': u'Parents',
            'max': 2,
            'subroles': ['first_parent', 'second_parent'],
            'doc': u'The one or two adults in charge of the household.'
            },
        {
            'key': 'child',
            'plural': 'children',
            'label': u'Child',
            'doc': u'Other individuals living in the household.'
            }
        ]

    )

entities = [Person, Vehicle]
