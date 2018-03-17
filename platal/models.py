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
"""Django models which fit the latest version of Plat/al database

Latest version synced: Plat/al 1.1.15
https://github.com/Polytechnique-org/platal/tree/xorg/maint/upgrade

cf. https://docs.djangoproject.com/en/dev/howto/legacy-databases/

This requires Django to work.
"""
from __future__ import unicode_literals

import collections
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


def is_ax_visible(field):
    return field in ('public', 'ax')


# Misc for Account/Profile
# ========================


@python_2_unicode_compatible
class Skin(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=96)
    date = models.DateField()
    comment = models.CharField(max_length=765)
    auteur = models.CharField(max_length=90)
    skin_tpl = models.CharField(max_length=96)
    ext = models.CharField(max_length=9)

    class Meta:
        db_table = 'skins'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class EmailVirtualDomain(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=765)
    aliasing = models.ForeignKey('self', db_column='aliasing')

    class Meta:
        db_table = 'email_virtual_domains'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ProfileSectionEnum(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=150, unique=True)

    class Meta:
        db_table = 'profile_section_enum'

    def __str__(self):
        return self.text


@python_2_unicode_compatible
class GeolocCountry(models.Model):
    iso_3166_1_a2 = models.CharField(max_length=6, primary_key=True)
    iso_3166_1_a3 = models.CharField(max_length=9, unique=True)
    iso_3166_1_num = models.IntegerField(unique=True)
    worldregion = models.CharField(max_length=6, db_column='worldRegion', blank=True) # Field name made lowercase.
    country = models.CharField(max_length=765, blank=True)
    countryen = models.CharField(max_length=765, db_column='countryEn', blank=True) # Field name made lowercase.
    capital = models.CharField(max_length=765)
    nationality = models.CharField(max_length=765, blank=True)
    nationalityen = models.CharField(max_length=765, db_column='nationalityEn', blank=True) # Field name made lowercase.
    phoneprefix = models.IntegerField(null=True, db_column='phonePrefix', blank=True) # Field name made lowercase.
    phoneformat = models.CharField(max_length=765, db_column='phoneFormat') # Field name made lowercase.
    licenseplate = models.CharField(max_length=12, db_column='licensePlate', blank=True) # Field name made lowercase.
    belongsto = models.ForeignKey('self', null=True, db_column='belongsTo', blank=True) # Field name made lowercase.
    countryplain = models.CharField(max_length=765, db_column='countryPlain', blank=True) # Field name made lowercase.

    class Meta:
        db_table = 'geoloc_countries'

    def __str__(self):
        return self.iso_3166_1_a2


# Account/Profile
# ===============


@python_2_unicode_compatible
class AccountType(models.Model):
    type = models.CharField(max_length=48, primary_key=True)
    perms = models.CharField(max_length=321)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'account_types'

    def __str__(self):
        return self.type


@python_2_unicode_compatible
class Account(models.Model):
    uid = models.AutoField(primary_key=True)
    hruid = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(AccountType, null=True, db_column='type', blank=True)
    user_perms = models.CharField(max_length=288, blank=True)
    is_admin = models.BooleanField(default=False)
    state = models.CharField(max_length=24)
    password = models.CharField(max_length=120, blank=True)
    token = models.CharField(max_length=96, blank=True)
    weak_password = models.CharField(max_length=768, blank=True)
    registration_date = models.DateTimeField()
    flags = models.CharField(max_length=15)
    comment = models.CharField(max_length=765, blank=True)
    email = models.CharField(max_length=765, blank=True)
    firstname = models.CharField(max_length=765, blank=True)
    lastname = models.CharField(max_length=765, blank=True)
    full_name = models.CharField(max_length=765, blank=True)
    directory_name = models.CharField(max_length=765, blank=True)
    sort_name = models.CharField(max_length=765, blank=True)
    display_name = models.CharField(max_length=765, blank=True)
    sex = models.CharField(max_length=18)
    email_format = models.CharField(max_length=12)
    skin = models.ForeignKey(Skin, null=True, db_column='skin', blank=True)
    last_version = models.CharField(max_length=48)
    best_domain = models.ForeignKey(EmailVirtualDomain, null=True, db_column='best_domain', blank=True)
    from_email = models.CharField(max_length=765)
    from_format = models.CharField(max_length=12)

    class Meta:
        db_table = 'accounts'

    def __str__(self):
        return '%s (%s)' % (self.hruid, self.full_name)

    @property
    def profile(self):
        return self.profiles.filter(perms='owner').get().profile


@python_2_unicode_compatible
class ProfileAlias(object):
    def __init__(self, alias_of, kind, lastname, firstname=None):
        self.alias_of = alias_of
        self.kind = kind
        self.lastname = lastname
        self.firstname = alias_of.firstname if firstname is None else firstname

    ALT_MARITAL = 'marital'
    ALT_PSEUDO = 'pseudo'
    ALT_ORDINARY = 'ordinary'

    @property
    def is_pseudo(self):
        return self.kind == self.ALT_PSEUDO

    def get_kind_display(self):
        if self.kind == self.ALT_MARITAL:
            if self.female:
                return "Mme"
            else:
                return "M."
        elif self.kind == self.ALT_PSEUDO:
            return "Pseudonyme"
        else:
            return ""

    def __getattr__(self, attr):
        return getattr(self.alias_of, attr)

    def __repr__(self):
        return '<ProfileAlias %s of %r>' % (self.kind, self.alias_of)


@python_2_unicode_compatible
class Profile(models.Model):

    alias_of = None

    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        self._aliases = None

    pid = models.AutoField(primary_key=True)
    hrpid = models.CharField(max_length=255, unique=True)
    xorg_id = models.IntegerField()
    ax_id = models.CharField(max_length=24, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    birthdate_ref = models.DateField(null=True, blank=True)
    next_birthday = models.DateField(null=True, blank=True)
    deathdate = models.DateField(null=True, blank=True)
    deathdate_rec = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=18)
    section = models.ForeignKey(ProfileSectionEnum, null=True, db_column='section', blank=True)
    cv = models.TextField(blank=True)
    freetext = models.TextField(blank=True)
    freetext_pub = models.CharField(max_length=21)
    medals_pub = models.CharField(max_length=21)
    alias_pub = models.CharField(max_length=21)
    nationality1 = models.ForeignKey(GeolocCountry, null=True, db_column='nationality1', blank=True, related_name='natives')
    nationality2 = models.ForeignKey(GeolocCountry, null=True, db_column='nationality2', blank=True, related_name='second_natives')
    nationality3 = models.ForeignKey(GeolocCountry, null=True, db_column='nationality3', blank=True, related_name='third_natives')
    email_directory = models.CharField(max_length=765, blank=True)
    last_change = models.DateField()
    title = models.CharField(max_length=12)

    class Meta:
        db_table = 'profiles'

    def __str__(self):
        return self.hrpid

    @property
    def is_alive(self):
        return self.deathdate is None

    @property
    def account(self):
        return self.accounts.filter(perms='owner').get().account


@python_2_unicode_compatible
class AccountProfile(models.Model):
    account = models.ForeignKey(Account, db_column='uid', related_name='profiles')
    profile = models.ForeignKey(Profile, db_column='pid', related_name='accounts')
    perms = models.CharField(max_length=15)

    class Meta:
        db_table = 'account_profiles'
        unique_together = (('account', 'profile'),)

    def __str__(self):
        return '%s -> %s' % (self.account.hruid, self.profile.hrpid)


# Email routing
# =============


@python_2_unicode_compatible
class EmailVirtual(models.Model):
    email = models.CharField(max_length=255)
    domain = models.ForeignKey(EmailVirtualDomain, db_column='domain')
    redirect = models.CharField(max_length=765)
    type = models.CharField(max_length=21, blank=True)
    expire = models.DateField()

    class Meta:
        db_table = 'email_virtual'
        unique_together = (('email', 'domain'),)

    def __str__(self):
        return "%s@%s (%s)" % (self.email, self.domain, self.type)


@python_2_unicode_compatible
class EmailRedirectAccount(models.Model):
    account = models.ForeignKey(Account, db_column='uid')
    redirect = models.CharField(max_length=765)
    rewrite = models.CharField(max_length=765)
    type = models.CharField(max_length=30)
    action = models.CharField(max_length=54)
    broken_date = models.DateField()
    broken_level = models.IntegerField()
    last = models.DateField()
    flags = models.CharField(max_length=24)
    hash = models.CharField(max_length=96, blank=True)
    allow_rewrite = models.BooleanField()

    class Meta:
        db_table = 'email_redirect_account'
        unique_together = (('account', 'redirect'),)

    def __str__(self):
        return "%s for %s (%s)" % (self.redirect, self.account.hruid, self.type)


@python_2_unicode_compatible
class EmailSourceAccount(models.Model):
    email = models.CharField(max_length=255)
    domain = models.ForeignKey(EmailVirtualDomain, db_column='domain')
    account = models.ForeignKey(Account, db_column='uid')
    type = models.CharField(max_length=9)
    flags = models.CharField(max_length=23)
    expire = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'email_source_account'
        unique_together = (('email', 'domain'),)

    def __str__(self):
        return "%s@%s (%s)" % (self.email, self.domain, self.type)


@python_2_unicode_compatible
class EmailSourceOther(models.Model):
    email = models.CharField(max_length=255)
    domain = models.ForeignKey(EmailVirtualDomain, db_column='domain')
    hrmid = models.CharField(max_length=255)
    type = models.CharField(max_length=8, blank=True, null=True)
    expire = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'email_source_other'
        unique_together = (('email', 'domain'),)

    def __str__(self):
        return "%s@%s (%s)" % (self.email, self.domain, self.type)


@python_2_unicode_compatible
class EmailRedirectOther(models.Model):
    hrmid = models.ForeignKey(EmailSourceOther, db_column='hrmid')
    redirect = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    action = models.CharField(max_length=18)

    class Meta:
        db_table = 'email_redirect_other'
        unique_together = (('hrmid', 'redirect'),)

    def __str__(self):
        return "%s -> %s (%s)" % (self.hrmid, self.redirect, self.type)


# GApps
# =====


class GappsAccount(models.Model):
    l_userid = models.ForeignKey(Account, null=True, db_column='l_userid', blank=True)
    l_sync_password = models.BooleanField(default=True)
    l_activate_mail_redirection = models.BooleanField(default=True)
    g_account_id = models.CharField(max_length=48, blank=True)
    g_account_name = models.CharField(max_length=255, primary_key=True)
    g_domain = models.CharField(max_length=120, blank=True)
    g_first_name = models.CharField(max_length=120)
    g_last_name = models.CharField(max_length=120)
    g_status = models.CharField(max_length=39, blank=True)
    g_admin = models.BooleanField()
    g_suspension = models.CharField(max_length=768, blank=True)
    r_disk_usage = models.BigIntegerField(null=True, blank=True)
    r_creation = models.DateField(null=True, blank=True)
    r_last_login = models.DateField(null=True, blank=True)
    r_last_webmail = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'gapps_accounts'


class GappsNickname(models.Model):
    l_userid = models.ForeignKey(Account, null=True, db_column='l_userid', blank=True)
    g_account_name = models.CharField(max_length=768)
    g_nickname = models.CharField(max_length=255, primary_key=True)

    class Meta:
        db_table = 'gapps_nicknames'


class GappsQueue(models.Model):
    q_id = models.AutoField(primary_key=True)
    q_owner = models.ForeignKey(Account, null=True, blank=True, related_name='owned_gapps_jobs')
    q_recipient = models.ForeignKey(Account, null=True, blank=True, related_name='received_gapps_jobs')
    p_entry_date = models.DateTimeField()
    p_notbefore_date = models.DateTimeField()
    p_start_date = models.DateTimeField(null=True, blank=True)
    p_end_date = models.DateTimeField(null=True, blank=True)
    p_status = models.CharField(max_length=24)
    p_priority = models.CharField(max_length=27)
    p_admin_request = models.BooleanField()
    j_type = models.CharField(max_length=30)
    j_parameters = models.TextField(blank=True)
    r_softfail_date = models.DateTimeField(null=True, blank=True)
    r_softfail_count = models.IntegerField()
    r_result = models.CharField(max_length=768, blank=True)

    class Meta:
        db_table = 'gapps_queue'


class GappsReporting(models.Model):
    date = models.DateField(primary_key=True)
    num_accounts = models.IntegerField(null=True, blank=True)
    count_1_day_actives = models.IntegerField(null=True, blank=True)
    count_7_day_actives = models.IntegerField(null=True, blank=True)
    count_14_day_actives = models.IntegerField(null=True, blank=True)
    count_30_day_actives = models.IntegerField(null=True, blank=True)
    count_30_day_idle = models.IntegerField(null=True, blank=True)
    count_60_day_idle = models.IntegerField(null=True, blank=True)
    count_90_day_idle = models.IntegerField(null=True, blank=True)
    usage_in_bytes = models.BigIntegerField(null=True, blank=True)
    quota_in_mb = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'gapps_reporting'


# Postfix
# =======


class MxWatch(models.Model):
    host = models.CharField(max_length=192, primary_key=True)
    state = models.CharField(max_length=21, blank=True)
    text = models.TextField()

    class Meta:
        db_table = 'mx_watch'


class PostfixBlacklist(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    reject_text = models.CharField(max_length=192)

    class Meta:
        db_table = 'postfix_blacklist'


class PostfixMailseen(models.Model):
    crc = models.CharField(max_length=24, primary_key=True)
    nb = models.IntegerField()
    update_time = models.DateTimeField()
    create_time = models.DateTimeField()
    release = models.CharField(max_length=18)

    class Meta:
        db_table = 'postfix_mailseen'


class PostfixWhitelist(models.Model):
    email = models.CharField(max_length=255, primary_key=True)

    class Meta:
        db_table = 'postfix_whitelist'



# Misc
# ====


class EmailListModerate(models.Model):
    ml = models.CharField(max_length=192)
    domain = models.CharField(max_length=192)
    mid = models.IntegerField()
    account = models.ForeignKey(Account, null=True, db_column='uid', blank=True)
    action = models.CharField(max_length=18)
    ts = models.DateTimeField()
    message = models.TextField(blank=True)
    handler = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'email_list_moderate'
        unique_together = (('ml', 'domain', 'mid'),)


class EmailSendSave(models.Model):
    account = models.OneToOneField(Account, primary_key=True, db_column='uid')
    data = models.TextField()

    class Meta:
        db_table = 'email_send_save'

class HomonymList(models.Model):
    hrmid = models.CharField(max_length=765)
    account = models.ForeignKey(Account, db_column='uid')

    class Meta:
        db_table = 'homonyms_list'
        unique_together = (('hrmid', 'account'),)
