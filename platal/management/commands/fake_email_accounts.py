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
"""Create fake email accounts in the database for testing purpose"""
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from ... import factories, models


class Command(BaseCommand):
    help = "Create fake email accounts in the database"

    def handle(self, *args, **options):
        # Remove every account from the database
        models.Account.objects.all().delete()

        # Create several accounts
        for i in range(20):
            account = factories.AccountFactory.create()
