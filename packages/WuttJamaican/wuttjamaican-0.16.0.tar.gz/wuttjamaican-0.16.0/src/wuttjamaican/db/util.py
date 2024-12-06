# -*- coding: utf-8; -*-
################################################################################
#
#  WuttJamaican -- Base package for Wutta Framework
#  Copyright © 2023-2024 Lance Edgar
#
#  This file is part of Wutta Framework.
#
#  Wutta Framework is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Wutta Framework is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  Wutta Framework.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Database Utilities
"""

import sqlalchemy as sa

from wuttjamaican.util import make_uuid


# nb. this convention comes from upstream docs
# https://docs.sqlalchemy.org/en/14/core/constraints.html#constraint-naming-conventions
naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}


class ModelBase:
    """ """

    def __iter__(self):
        # nb. we override this to allow for `dict(self)`
        state = sa.inspect(self)
        fields = [attr.key for attr in state.attrs]
        return iter([(field, getattr(self, field))
                     for field in fields])

    def __getitem__(self, key):
        # nb. we override this to allow for `x = self['field']`
        state = sa.inspect(self)
        if hasattr(state.attrs, key):
            return getattr(self, key)


def uuid_column(*args, **kwargs):
    """
    Returns a UUID column for use as a table's primary key.
    """
    kwargs.setdefault('primary_key', True)
    kwargs.setdefault('nullable', False)
    kwargs.setdefault('default', make_uuid)
    return sa.Column(sa.String(length=32), *args, **kwargs)


def uuid_fk_column(target_column, *args, **kwargs):
    """
    Returns a UUID column for use as a foreign key to another table.

    :param target_column: Name of the table column on the remote side,
       e.g. ``'user.uuid'``.
    """
    return sa.Column(sa.String(length=32), sa.ForeignKey(target_column), *args, **kwargs)
