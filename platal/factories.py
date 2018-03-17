# -*- coding: utf-8 -*-
#***************************************************************************
#*  Copyright (C) 2015 Polytechnique.org                                   *
#*  http://opensource.polytechnique.org/                                   *
#*                                                                         *
#*  This program is free software; you can redistribute it and/or modify   *
#*  it under the terms of the GNU General Public License as published by   *
#*  the Free Software Foundation; either version 2 of the License, or      *
#*  (at your option) any later version.                                    *
#*                                                                         *
#*  This program is distributed in the hope that it will be useful,        *
#*  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
#*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
#*  GNU General Public License for more details.                           *
#*                                                                         *
#*  You should have received a copy of the GNU General Public License      *
#*  along with this program; if not, write to the Free Software            *
#*  Foundation, Inc.,                                                      *
#*  59 Temple Place, Suite 330, Boston, MA  02111-1307  USA                *
#***************************************************************************/
"""FactoryBoy classes aimed to ease populating the database
"""
from __future__ import unicode_literals

import datetime
import django.utils.timezone
import factory
import factory.django
import re
import unicodedata

from . import models


def emailify(string):
    """Transform a UTF-8 string to an ASCII representation suitable for an
    email address

    >>> emailify('ABC def')
    'abc-def'
    >>> emailify('gégé à l\'accent')
    'gege-a-l-accent'
    """
    normstr = unicodedata.normalize('NFKD', string)
    asciitext = normstr.encode('ascii', 'ignore').decode('ascii').lower()
    return re.sub(r'[^-._a-zA-Z0-9]', '-', asciitext)


# Define a list of names so that they are always the same accross builds
FIRSTNAMES_F = (
    'Elisabeth',
    'Emmanuelle',
    'Marie',
    'Marie-Hélène',
    'Marthe',
)
FIRSTNAMES_M = (
    'Jean',
    'Jean-Baptiste',
    'Jacques',
    'Joseph',
    'Luc',
    'Marc',
    'Matthieu',
    'Paul',
    'Pierre',
    'Simon',
    'Thomas',
)
FIRSTNAMES = FIRSTNAMES_F + FIRSTNAMES_M
LASTNAMES = (
    'Bibi',
    'Exemple',
    'De La Machine',
    'Le Testeur',
)

class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Account

    firstname = factory.Sequence(lambda n: FIRSTNAMES[n % len(FIRSTNAMES)])
    lastname = factory.Sequence(lambda n: LASTNAMES[n % len(LASTNAMES)])
    full_name = factory.LazyAttribute(lambda o: '%s %s' % (o.firstname, o.lastname))
    directory_name = factory.LazyAttribute(lambda o: '%s %s' % (o.firstname, o.lastname))
    sort_name = factory.LazyAttribute(lambda o: '%s %s' % (o.lastname, o.firstname))
    display_name = factory.LazyAttribute(lambda o: '%s %s' % (o.firstname, o.lastname))
    sex = factory.Sequence(lambda n: 'female' if n % len(FIRSTNAMES) < len(FIRSTNAMES_F) else 'male')
    hruid = factory.LazyAttributeSequence(
        lambda o, n: emailify('%s.%s.%d' % (o.firstname, o.lastname, n)))
    registration_date = factory.Sequence(
        lambda n: datetime.date(2000, 1, 1) + datetime.timedelta(days=n))
