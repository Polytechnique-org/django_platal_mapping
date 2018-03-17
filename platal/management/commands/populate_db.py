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
"""Populate the database with initial data"""
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from ... import models


class Command(BaseCommand):
    help = "Populate the database with initial data"

    def populate_account_types(self):
        account_types = (
            ('ax', 'groups,directory_ax,directory_hidden,edit_directory,user', "Personnel de l'AX"),
            ('fx', 'groups,directory_ax,user', "Personnel de la FX"),
            ('master', 'groups,mail,directory_private,forums,lists,payment,user', "Master de l'X"),
            ('phd', 'groups,mail,directory_private,forums,lists,payment,user', "Docteur de l'X"),
            ('pi', 'groups,forums,lists,user', "Elève du programme international"),
            ('school', 'groups,directory_ax,user', "Personnel de l'X"),
            ('virtual', '', None),
            ('x', 'groups,mail,directory_private,forums,lists,payment,gapps,user', "Polytechnicien"),
            ('xnet', 'groups', None),
        )
        for t, perms, desc in account_types:
            models.AccountType(type=t, perms=perms, description=desc).save()

    def handle(self, *args, **options):
        self.populate_account_types()
