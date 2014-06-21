# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

import collections

from django.db import models


def is_ax_visible(field):
    return field in ('public', 'ax')


# Misc for Account/Profile
# ========================


class Skin(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=96)
    date = models.DateField()
    comment = models.CharField(max_length=765)
    auteur = models.CharField(max_length=90)
    skin_tpl = models.CharField(max_length=96)
    ext = models.CharField(max_length=9)
    class Meta:
        db_table = u'skins'

    def __unicode__(self):
        return self.name


class EmailVirtualDomain(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=765)
    aliasing = models.ForeignKey('self', db_column='aliasing')
    class Meta:
        db_table = u'email_virtual_domains'

    def __unicode__(self):
        return self.name


class ProfileSectionEnum(models.Model):
    #id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=150, unique=True)
    class Meta:
        db_table = u'profile_section_enum'

    def __unicode__(self):
        return self.text


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
        db_table = u'geoloc_countries'

    def __unicode__(self):
        return self.iso_3166_1_a2


# Account/Profile
# ===============


class AccountType(models.Model):
    type = models.CharField(max_length=48, primary_key=True)
    perms = models.CharField(max_length=321)
    description = models.TextField(blank=True)
    class Meta:
        db_table = u'account_types'

    def __unicode__(self):
        return self.type


class Account(models.Model):
    uid = models.AutoField(primary_key=True)
    hruid = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(AccountType, null=True, db_column='type', blank=True)
    user_perms = models.CharField(max_length=288, blank=True)
    is_admin = models.BooleanField()
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
        db_table = u'accounts'

    def __unicode__(self):
        return u'%s (%s)' % (self.hruid, self.full_name)

    @property
    def profile(self):
        return self.profiles.filter(perms='owner').get().profile


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
                return u"Mme"
            else:
                return u"M."
        elif self.kind == self.ALT_PSEUDO:
            return u"Pseudonyme"
        else:
            return u""

    def __getattr__(self, attr):
        return getattr(self.alias_of, attr)

    def __repr__(self):
        return '<ProfileAlias %s of %r>' % (self.kind, self.alias_of)


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
        db_table = u'profiles'

    def __unicode__(self):
        return self.hrpid

    @property
    def is_alive(self):
        return self.deathdate is None

    @property
    def account(self):
        return self.accounts.filter(perms='owner').get().account

    @property
    def firstname(self):
        return self.public_name.firstname_ordinary or self.public_name.firstname_main or self.public_name.firstname_initial

    @property
    def lastname(self):
        return self.public_name.lastname_main or self.public_name.lastname_initial

    @property
    def lastname_display(self):
        return self.public_name.lastname_ordinary or self.public_name.lastname_marital or self.public_name.lastname_main or self.public_name.lastname_initial

    @property
    def lastname_marital(self):
        return self.public_name.lastname_marital

    @property
    def lastname_ordinary(self):
        return self.public_name.lastname_ordinary

    @property
    def pseudonym(self):
        return self.public_name.pseudonym

    @property
    def promo(self):
        return self.profiledisplay.promo

    @property
    def female(self):
        return self.sex == 'female'

    @property
    def nationality(self):
        return self.nationality1 or self.nationality2 or self.nationality3

    @property
    def country_code(self):
        nat = self.nationality
        if nat is None:
            return 'FR'
        return nat.iso_3166_1_a2

    @property
    def country_name(self):
        nat = self.nationality
        if nat is None:
            return u"France"
        return nat.country

    @property
    def current_corps(self):
        try:
            return self.profilecorps.current
        except ProfileCorps.DoesNotExist:
            return None

    def get_aliases(self, include_deviations=True):
        if self._aliases is None:
            self._aliases = []

            alt_names = set([self.lastname])
            if self.lastname_marital and self.lastname_marital not in alt_names:
                alt_names.add(self.lastname_marital)
                self._aliases.append(
                    ProfileAlias(self, ProfileAlias.ALT_MARITAL, self.lastname_marital))

            if self.lastname_ordinary and self.lastname_ordinary not in alt_names:
                # Some people filled 'ordinary' instead of 'marital'
                alt_names.add(self.lastname_ordinary)
                self._aliases.append(
                    ProfileAlias(self, ProfileAlias.ALT_ORDINARY, self.lastname_ordinary))

            if self.pseudonym and self.pseudonym not in alt_names:
                alt_names.add(self.pseudonym)
                self._aliases.append(
                    ProfileAlias(self, ProfileAlias.ALT_PSEUDO, self.pseudonym, firstname=''))

        if include_deviations:
            return self._aliases
        else:
            return [a for a in self._aliases
                if not a.lastname.startswith(self.lastname)
                and not self.lastname.startswith(a.lastname)
            ]

    @property
    def mobile_line(self):
        if not hasattr(self, '_mobiles'):
            mobiles = [phone
                for phone in self.phones.all()
                if phone.link_type == phone.LINK_USER and phone.tel_type == phone.KIND_MOBILE
            ]
            self._mobiles = sorted(mobiles, key=lambda p: p.tel_id)
        if self._mobiles:
            return self._mobiles[0]
        return None

    def sorted_addresses(self, for_ax=False):
        personal_addresses = [addr
            for addr in self.addresses.all()
            if addr.is_home and (addr.ax_visible or not for_ax)
        ]

        address_phones = collections.defaultdict(lambda: collections.defaultdict(list))

        for phone in self.phones.all():
            if phone.is_address and (phone.ax_visible or not for_ax):
                address_phones[phone.link_id][phone.tel_type].append(phone)

        for address in personal_addresses:
            addr_phones = {}
            for kind, phones in address_phones[address.subid].items():
                if phones:
                    addr_phones[kind] = sorted(phones, key=lambda p: p.tel_id)[0]
                else:
                    addr_phones[kind] = None
            address.phones = addr_phones

        current = [addr for addr in personal_addresses if addr.current]
        secondary = [addr for addr in personal_addresses if addr.secondary and not addr.current]
        if not current:
            current, secondary = secondary, []

        return [(a, True) for a in current] + [(a, False) for a in secondary]

    def sorted_educations(self):
        edus = [edu for edu in self.educations.all() if edu.school and edu.school.abbreviation != 'X']
        return sorted(edus, key=lambda edu: edu.entry_year)

    def sorted_jobs(self):
        jobs = sorted(self.jobs.all(), key=lambda j: (j.id, j.entry_year))
        job_addresses = {}
        for addr in self.addresses.all():
            if addr.is_job:
                job_addresses[addr.job_id] = addr

        job_phones = collections.defaultdict(lambda: collections.defaultdict(list))
        for phone in self.phones.all():
            if phone.is_job:
                job_phones[phone.link_id][phone.tel_type].append(phone)

        for job in jobs:
            job.address = job_addresses.get(job.id)
            j_phones = {}
            for kind, phones in job_phones[job.id].items():
                if phones:
                    j_phones[kind] = sorted(phones, key=lambda p: p.tel_id)[0]
                else:
                    j_phones[kind] = None
            job.phones = j_phones

        return jobs


class AccountProfile(models.Model):
    account = models.ForeignKey(Account, db_column='uid', related_name='profiles')
    profile = models.ForeignKey(Profile, db_column='pid', related_name='accounts')
    pkey = models.CompositeField(account, profile, primary_key=True)
    perms = models.CharField(max_length=15)
    class Meta:
        db_table = u'account_profiles'

    def __unicode__(self):
        return u'%s -> %s' % (self.account.hruid, self.profile.hrpid)


# Account-related
# ===============


class AccountAuthOpenid(models.Model):
    #id = models.IntegerField(primary_key=True)
    account = models.ForeignKey(Account, unique=True, null=True, db_column='uid', blank=True)
    url = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table = u'account_auth_openid'

    def __unicode__(self):
        return u"%s at %s" % (self.account, self.url)

class AccountLostPassword(models.Model):
    certificat = models.CharField(max_length=96, primary_key=True)
    account = models.ForeignKey(Account, null=True, db_column='uid', blank=True)
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'account_lost_passwords'

    def __unicode__(self):
        return u"%s on %s" % (self.account.hruid, self.created)


class AccountXnetLostPassword(models.Model):
    account = models.ForeignKey(Account, primary_key=True, db_column='uid')
    date = models.DateTimeField(null=True, blank=True)
    hash = models.CharField(max_length=96)
    class Meta:
        db_table = u'account_xnet_lost_passwords'

    def __unicode__(self):
        return u"%s on %s" % (self.account.hruid, self.date)


# Announces
# =========


class Announce(models.Model):
    #id = models.IntegerField(primary_key=True)
    account = models.ForeignKey(Account, null=True, db_column='uid', blank=True)
    creation_date = models.DateTimeField()
    titre = models.CharField(max_length=765)
    texte = models.TextField()
    expiration = models.DateField()
    promo_min = models.IntegerField()
    promo_max = models.IntegerField()
    flags = models.CharField(max_length=87)
    noinvite = models.IntegerField()
    post_id = models.IntegerField(null=True, blank=True, editable=False,
        help_text=u"NNTP post identifier")
    class Meta:
        db_table = u'announces'

    def __unicode__(self):
        return u"%s: %s" % (self.id, self.titre)


class AnnouncePhoto(models.Model):
    eid = models.ForeignKey(Announce, primary_key=True, db_column='eid')
    attachmime = models.CharField(max_length=12)
    attach = models.TextField()
    x = models.IntegerField()
    y = models.IntegerField()
    class Meta:
        db_table = u'announce_photos'

    def __unicode__(self):
        return u"%s (%s, %d x %d)" % (self.eid, self.attachmime, self.x, self.y)


class AnnounceRead(models.Model):
    evt = models.ForeignKey(Announce)
    account = models.ForeignKey(Account, db_column='uid')
    pkey = models.CompositeField(evt, account, primary_key=True)
    class Meta:
        db_table = u'announce_read'

    def __unicode__(self):
        return u"%s: %s" % (self.account, self.evt)


# Email routing
# =============


class EmailVirtual(models.Model):
    email = models.CharField(max_length=255)
    domain = models.ForeignKey(EmailVirtualDomain, db_column='domain')
    pkey = models.CompositeField(email, domain, primary_key=True)
    redirect = models.CharField(max_length=765)
    type = models.CharField(max_length=21, blank=True)
    expire = models.DateField()
    class Meta:
        db_table = u'email_virtual'

    def __unicode__(self):
        return u"%s@%s (%s)" % (self.email, self.domain, self.type)


class EmailRedirectAccount(models.Model):
    account = models.ForeignKey(Account, db_column='uid')
    redirect = models.CharField(max_length=765)
    pkey = models.CompositeField(account, redirect, primary_key=True)
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
        db_table = u'email_redirect_account'

    def __unicode__(self):
        return u"%s for %s (%s)" % (self.redirect, self.account.hruid, self.type)


class EmailSourceAccount(models.Model):
    email = models.CharField(max_length=255)
    domain = models.ForeignKey(EmailVirtualDomain, db_column='domain')
    pkey = models.CompositeField(email, domain, primary_key=True)

    account = models.ForeignKey(Account, db_column='uid')
    type = models.CharField(max_length=27)
    flags = models.CharField(max_length=69)
    expire = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'email_source_account'

    def __unicode__(self):
        return u"%s@%s (%s)" % (self.email, self.domain, self.type)


class EmailSourceOther(models.Model):
    email = models.CharField(max_length=255)
    domain = models.ForeignKey(EmailVirtualDomain, db_column='domain')
    pkey = models.CompositeField(email, domain, primary_key=True)

    hrmid = models.CharField(max_length=765)
    type = models.CharField(max_length=24, blank=True)
    expire = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'email_source_other'

    def __unicode__(self):
        return u"%s@%s (%s)" % (self.email, self.domain, self.type)


class EmailRedirectOther(models.Model):
    hrmid = models.ForeignKey(EmailSourceOther, db_column='hrmid')
    redirect = models.CharField(max_length=765)
    pkey = models.CompositeField(hrmid, redirect, primary_key=True)
    type = models.CharField(max_length=30)
    action = models.CharField(max_length=54)
    class Meta:
        db_table = u'email_redirect_other'

    def __unicode__(self):
        return u"%s -> %s (%s)" % (self.hrmid, self.redirect, self.type)


# innd-related
# ============


class InndForum(models.Model):
    """ACLs for innd"""
    id_innd = models.AutoField(primary_key=True)
    ipmin = models.IntegerField(null=True, blank=True)
    ipmax = models.IntegerField(null=True, blank=True)
    account = models.ForeignKey(Account, null=True, db_column='uid', blank=True)
    read_perm = models.CharField(max_length=300, blank=True)
    write_perm = models.CharField(max_length=300, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    comment = models.TextField(blank=True)
    class Meta:
        db_table = u'forum_innd'

    def __unicode__(self):
        return "%d: %s" % (self.id_innd, self.account.hruid)


class ForumProfile(models.Model):
    account = models.ForeignKey(Account, primary_key=True, db_column='uid')
    name = models.CharField(max_length=192)
    mail = models.CharField(max_length=210)
    sig = models.TextField()
    flags = models.CharField(max_length=63)
    tree_unread = models.CharField(max_length=24)
    tree_read = models.CharField(max_length=24)
    last_seen = models.DateTimeField()
    class Meta:
        db_table = u'forum_profiles'

    def __unicode__(self):
        return u"%s: %s" % (self.account.hruid, self.name)


class Forum(models.Model):
    fid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=192)
    class Meta:
        db_table = u'forums'

    def __unicode__(self):
        return self.name


class ForumSubs(models.Model):
    forum = models.ForeignKey(Forum, db_column='fid')
    account = models.ForeignKey(Account, db_column='uid')
    pkey = models.CompositeField(forum, account, primary_key=True)
    class Meta:
        db_table = u'forum_subs'

    def __unicode__(self):
        return u"%s by %s" % (self.forum.name, self.account.hruid)


# Payments
# ========


class PaymentBankAccount(models.Model):
    #id = models.IntegerField(primary_key=True)
    asso = models.ForeignKey('Group', blank=True, null=True)
    account = models.CharField(max_length=69)
    owner = models.CharField(max_length=300)
    status = models.CharField(max_length=36)
    class Meta:
        db_table = u'payment_bankaccounts'

    def __unicode__(self):
        return u'%s: %s' % (self.asso.name, self.account)


class Payment(models.Model):
    #id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=765)
    url = models.CharField(max_length=384)
    flags = models.CharField(max_length=51)
    amount_def = models.DecimalField(max_digits=12, decimal_places=2)
    amount_min = models.DecimalField(max_digits=12, decimal_places=2)
    amount_max = models.DecimalField(max_digits=12, decimal_places=2)
    mail = models.CharField(max_length=192)
    confirmation = models.TextField()
    asso = models.ForeignKey('Group', null=True, blank=True)
    rib = models.ForeignKey(PaymentBankAccount, null=True, blank=True)
    class Meta:
        db_table = u'payments'

    def __unicode__(self):
        return u"%s: %s" % (self.id, self.text)


class PaymentCodeC(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=192)
    class Meta:
        db_table = u'payment_codeC'

    def __unicode__(self):
        return self.text


class PaymentCodeRCB(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=192)
    codec = models.IntegerField(db_column='codeC') # Field name made lowercase.
    class Meta:
        db_table = u'payment_codeRCB'

    def __unicode__(self):
        return self.text


class PaymentMethod(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=96)
    include = models.CharField(max_length=96)
    short_name = models.CharField(max_length=30)
    flags = models.CharField(max_length=36, blank=True)
    class Meta:
        db_table = u'payment_methods'

    def __unicode__(self):
        return self.short_name


class PaymentReconcilation(models.Model):
    #id = models.IntegerField(primary_key=True)
    method = models.ForeignKey(PaymentMethod)
    period_start = models.DateField()
    period_end = models.DateField()
    status = models.CharField(max_length=33)
    payment_count = models.IntegerField()
    sum_amounts = models.DecimalField(max_digits=11, decimal_places=2)
    sum_commissions = models.DecimalField(max_digits=11, decimal_places=2)
    comments = models.TextField()
    recongroup_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'payment_reconcilations'

    def __unicode__(self):
        return u"%s: %s" % (self.method, self.status)


class PaymentTransaction(models.Model):
    id = models.CharField(max_length=192, primary_key=True)
    method = models.ForeignKey(PaymentMethod, null=True, blank=True)
    account = models.ForeignKey(Account, db_column='uid')
    ref = models.IntegerField()
    fullref = models.CharField(max_length=45)
    ts_confirmed = models.DateTimeField(null=True, blank=True)
    ts_initiated = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    commission = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    pkey = models.CharField(max_length=15)
    comment = models.CharField(max_length=765)
    status = models.CharField(max_length=27)
    recon = models.ForeignKey(PaymentReconcilation, null=True, blank=True)
    display = models.IntegerField()
    class Meta:
        db_table = u'payment_transactions'

    def __unicode__(self):
        return u"%s (%s)" % (self.fullref, self.ref)


class PaymentTransfer(models.Model):
    #id = models.IntegerField(primary_key=True)
    recongroup_id = models.IntegerField()
    payment = models.ForeignKey(Payment)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    account = models.ForeignKey(Account, null=True, blank=True)
    message = models.CharField(max_length=765)
    date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'payment_transfers'

    def __unicode__(self):
        return u"%s: %s" % (self.id, self.amount)


# Groups
# ======


class GroupDom(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.TextField(db_column='nom')
    cat = models.CharField(max_length=117)
    class Meta:
        db_table = u'group_dom'

    def __unicode__(self):
        return u"%s :: %s" % (self.cat, self.name)


class Group(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=765, db_column='nom')
    diminutif = models.CharField(max_length=192, unique=True)
    cat = models.CharField(max_length=117)
    dom = models.ForeignKey(GroupDom, null=True, db_column='dom', blank=True)
    descr = models.TextField()
    logo = models.TextField(blank=True)
    logo_mime = models.TextField(blank=True)
    site = models.CharField(max_length=765)
    mail = models.CharField(max_length=765)
    resp = models.CharField(max_length=765)
    forum = models.CharField(max_length=765)
    mail_domain = models.CharField(max_length=765)
    ax = models.IntegerField()
    pub = models.CharField(max_length=21)
    sub_url = models.CharField(max_length=765)
    inscriptible = models.IntegerField()
    unsub_url = models.CharField(max_length=765)
    flags = models.CharField(max_length=117)
    axdate = models.DateField(null=True, db_column='axDate', blank=True) # Field name made lowercase.
    welcome_msg = models.TextField(blank=True)
    class Meta:
        db_table = u'groups'

    def __unicode__(self):
        return self.name


# Group::membership
# -----------------


class GroupMember(models.Model):
    asso = models.ForeignKey(Group)
    account = models.ForeignKey(Account, db_column='uid')
    pkey = models.CompositeField(asso, account, primary_key=True)

    perms = models.CharField(max_length=18)
    comm = models.CharField(max_length=765, blank=True)
    position = models.CharField(max_length=54, blank=True)
    flags = models.CharField(max_length=18)
    class Meta:
        db_table = u'group_members'

    def __unicode__(self):
        return u"%s to %s" % (self.account.hruid, self.asso.name)


class GroupMemberSubRequest(models.Model):
    asso = models.ForeignKey(Group)
    account = models.ForeignKey(Account, db_column='uid')
    pkey = models.CompositeField(asso, account, primary_key=True)

    ts = models.DateTimeField()
    reason = models.TextField(blank=True)
    class Meta:
        db_table = u'group_member_sub_requests'

    def __unicode__(self):
        return u"%s to %s" % (self.account.hruid, self.asso.name)


class GroupFormerMember(models.Model):
    asso = models.ForeignKey(Group)
    account = models.ForeignKey(Account, db_column='uid')
    pkey = models.CompositeField(asso, account, primary_key=True)

    remember = models.IntegerField()
    unsubsciption_date = models.DateField()
    class Meta:
        db_table = u'group_former_members'

    def __unicode__(self):
        return u"%s to %s" % (self.account.hruid, self.asso.name)


# Group::Announces
# ----------------


class GroupAnnounce(models.Model):
    #id = models.IntegerField(primary_key=True)
    account = models.ForeignKey(Account, null=True, db_column='uid', blank=True)
    asso = models.ForeignKey(Group)
    create_date = models.DateTimeField()
    titre = models.CharField(max_length=765)
    texte = models.TextField()
    contacts = models.TextField()
    expiration = models.DateField()
    promo_min = models.IntegerField()
    promo_max = models.IntegerField()
    flags = models.CharField(max_length=36)
    post_id = models.IntegerField(null=True, blank=True,
        help_text=u"NNTP post ID")
    class Meta:
        db_table = u'group_announces'

    def __unicode__(self):
        return u"%s: %s" % (self.asso.name, self.titre)


class GroupAnnouncePhoto(models.Model):
    eid = models.ForeignKey(GroupAnnounce, primary_key=True, db_column='eid')
    attachmime = models.CharField(max_length=12)
    attach = models.TextField()
    x = models.IntegerField()
    y = models.IntegerField()
    class Meta:
        db_table = u'group_announces_photo'

    def __unicode__(self):
        return u"%s (%s, %d x %d)" % (self.eid, self.attachmime, self.x, self.y)


class GroupAnnounceRead(models.Model):
    announce = models.ForeignKey(GroupAnnounce)
    account = models.ForeignKey(Account, db_column='uid')
    pkey = models.CompositeField(announce, account, primary_key=True)
    class Meta:
        db_table = u'group_announces_read'

    def __unicode__(self):
        return u"%s: %s" % (self.account.hruid, self.announce_id)


# Group::Event
# ------------


class GroupEvent(models.Model):
    eid = models.IntegerField(primary_key=True)
    asso = models.ForeignKey(Group, null=True, blank=True)
    account = models.ForeignKey(Account, null=True, db_column='uid', blank=True)
    intitule = models.CharField(max_length=300)
    short_name = models.CharField(max_length=90)
    paiement = models.ForeignKey(Payment, null=True, blank=True)
    descriptif = models.TextField()
    debut = models.DateTimeField()
    fin = models.DateTimeField(null=True, blank=True)
    show_participants = models.BooleanField()
    deadline_inscription = models.DateField(null=True, blank=True)
    noinvite = models.IntegerField()
    accept_nonmembre = models.BooleanField()
    archive = models.BooleanField()
    subscription_notification = models.CharField(max_length=24)
    class Meta:
        db_table = u'group_events'

    def __unicode__(self):
        return u"%s: %s" % (self.asso.name, self.intitule)


class GroupEventItem(models.Model):
    event = models.ForeignKey(GroupEvent, db_column='eid')
    item_id = models.IntegerField()
    pkey = models.CompositeField(event, item_id, primary_key=True)

    titre = models.CharField(max_length=300)
    details = models.TextField()
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    class Meta:
        db_table = u'group_event_items'

    def __unicode__(self):
        return u"%s - %s" % (self.event, self.item_id)


class GroupEventParticipant(models.Model):
    event = models.ForeignKey(GroupEvent, db_column='eid')
    item_id = models.IntegerField()
    account = models.ForeignKey(Account, db_column='uid')
    item = models.ForeignKey(GroupEventItem, to_field='pkey')
    pkey = models.CompositeField(event, account, item, primary_key=True)

    nb = models.IntegerField()
    flags = models.CharField(max_length=42)
    paid = models.FloatField()
    class Meta:
        db_table = u'group_event_participants'

    def __unicode__(self):
        return u"%s to %s" % (self.account.hruid, self.item)


# Group::misc
# -----------


class GroupAuth(models.Model):
    #id = models.IntegerField(primary_key=True)
    privkey = models.CharField(max_length=120, unique=True)
    name = models.CharField(max_length=96)
    datafields = models.CharField(max_length=765)
    returnurls = models.CharField(max_length=765)
    last_used = models.DateField(null=True, blank=True)
    group = models.ForeignKey(Group, null=True, blank=True)
    flags = models.CharField(max_length=63, blank=True)
    class Meta:
        db_table = u'group_auth'

    def __unicode__(self):
        return self.name


# Logging
# =======


class IpWatch(models.Model):
    state = models.CharField(max_length=27)
    detection = models.DateField(null=True, blank=True)
    last = models.DateTimeField()
    account = models.ForeignKey(Account, null=True, db_column='uid', blank=True)
    description = models.TextField()
    ip = models.IntegerField(primary_key=True)
    mask = models.IntegerField()
    class Meta:
        db_table = u'ip_watch'

    def __unicode__(self):
        return self.ip


class LogAction(models.Model):
    #id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=96)
    description = models.CharField(max_length=765)
    class Meta:
        db_table = u'log_actions'

    def __unicode__(self):
        return self.text


class LogSession(models.Model):
    #id = models.IntegerField(primary_key=True)
    auth = models.CharField(max_length=18)
    account = models.ForeignKey(Account, null=True, db_column='uid', blank=True, related_name='sessions')
    start = models.DateTimeField()
    host = models.CharField(max_length=384)
    sauth = models.CharField(max_length=18)
    suid = models.ForeignKey(Account, null=True, db_column='suid', blank=True, related_name='su_sessions')
    browser = models.CharField(max_length=765)
    forward_host = models.CharField(max_length=384, blank=True)
    flags = models.CharField(max_length=15)
    ip = models.IntegerField()
    forward_ip = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'log_sessions'

    def __unicode__(self):
        return u"%s: %s@%s" % (self.id, self.account.hruid, self.host)


class LogLastSession(models.Model):
    account = models.ForeignKey(Account, primary_key=True, db_column='uid')
    id = models.ForeignKey(LogSession, db_column='id')
    class Meta:
        db_table = u'log_last_sessions'

    def __unicode__(self):
        return self.account.hruid


class LogEvent(models.Model):
    stamp = models.DateTimeField(primary_key=True)
    session = models.ForeignKey(LogSession, db_column='session')
    action = models.ForeignKey(LogAction, db_column='action')
    data = models.TextField(blank=True)
    class Meta:
        db_table = u'log_events'

    def __unicode__(self):
        return u"%s@%s: %s" % (self.session_id, self.stamp, self.action.text)


# Newsletters
# ===========


class Newsletter(models.Model):
    #id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(Group, unique=True)
    name = models.CharField(max_length=765)
    custom_css = models.BooleanField()
    criteria = models.CharField(max_length=42, blank=True)
    class Meta:
        db_table = u'newsletters'

    def __unicode__(self):
        return self.name


class NewsletterIssue(models.Model):
    nlid = models.ForeignKey(Newsletter, unique=True, db_column='nlid')
    #id = models.IntegerField(primary_key=True)
    date = models.DateField()
    send_before = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=21)
    sufb_json = models.TextField(blank=True)
    title = models.CharField(max_length=765)
    head = models.TextField()
    signature = models.TextField()
    short_name = models.CharField(max_length=48, unique=True, blank=True)
    mail_title = models.CharField(max_length=765)
    unsubscribe = models.IntegerField()
    reply_to = models.CharField(max_length=765)
    class Meta:
        db_table = u'newsletter_issues'

    def __unicode__(self):
        return self.title


class NewsletterCat(models.Model):
    cid = models.AutoField(primary_key=True)
    nlid = models.ForeignKey(Newsletter, db_column='nlid')
    pos = models.IntegerField()
    title = models.CharField(max_length=384)
    class Meta:
        db_table = u'newsletter_cat'

    def __unicode__(self):
        return self.title


class NewsletterArt(models.Model):
    issue = models.ForeignKey(NewsletterIssue, db_column='id')
    aid = models.IntegerField()
    pkey = models.CompositeField(issue, aid, primary_key=True)
    cid = models.ForeignKey(NewsletterCat, null=True, db_column='cid', blank=True)
    pos = models.IntegerField()
    title = models.TextField()
    body = models.TextField()
    append = models.TextField()
    class Meta:
        db_table = u'newsletter_art'

    def __unicode__(self):
        return u"%s: %s" % (self.issue_id, self.title)


class NewsletterIns(models.Model):
    account = models.ForeignKey(Account, db_column='uid')
    nl = models.ForeignKey(Newsletter, db_column='nlid')
    pkey = models.CompositeField(account, nl, primary_key=True)
    last = models.ForeignKey(NewsletterIssue, null=True, db_column='last', blank=True)
    hash = models.CharField(max_length=96, blank=True)
    class Meta:
        db_table = u'newsletter_ins'

    def __unicode__(self):
        return u"%s to %s" % (self.account.hruid, self.nl.title)


# Profile
# =======


class ProfileDisplay(models.Model):
    profile = models.OneToOneField(Profile, primary_key=True, db_column='pid')
    yourself = models.CharField(max_length=765)
    public_name = models.CharField(max_length=765)
    private_name = models.CharField(max_length=765)
    directory_name = models.CharField(max_length=765)
    short_name = models.CharField(max_length=765)
    sort_name = models.CharField(max_length=765)
    promo = models.CharField(max_length=765)
    class Meta:
        db_table = u'profile_display'

    def __unicode__(self):
        return self.profile.hrpid


class ProfilePhone(models.Model):
    LINK_ADDRESS = 'address'
    LINK_PRO = 'pro'
    LINK_USER = 'user'
    LINK_HQ = 'hq'
    LINK_GROUP = 'group'
    LINK_CHOICES = (
        (LINK_ADDRESS, u"Address"),
        (LINK_PRO, u"Pro"),
        (LINK_USER, u"User"),
        (LINK_HQ, u"HQ"),
        (LINK_GROUP, u"Group"),
    )

    KIND_FIXED = 'fixed'
    KIND_MOBILE = 'mobile'
    KIND_FAX = 'fax'
    KIND_CHOICES = (
        (KIND_FIXED, u"Fixed"),
        (KIND_MOBILE, u"Mobile"),
        (KIND_FAX, u"Fax"),
    )

    profile = models.ForeignKey(Profile, db_column='pid', related_name='phones')
    link_type = models.CharField(max_length=21, choices=LINK_CHOICES)
    link_id = models.IntegerField()
    tel_id = models.IntegerField()
    pkey = models.CompositeField(profile, link_type, link_id, tel_id, primary_key=True)

    tel_type = models.CharField(max_length=18, choices=KIND_CHOICES)
    search_tel = models.CharField(max_length=75)
    display_tel = models.CharField(max_length=90)
    pub = models.CharField(max_length=21)
    comment = models.CharField(max_length=240)

    class Meta:
        db_table = u'profile_phones'

    def __unicode__(self):
        return u"%s: %s (%s)" % (self.profile.hrpid, self.display_tel, self.tel_type)

    @property
    def is_address(self):
        return self.link_type == self.LINK_ADDRESS

    @property
    def is_job(self):
        return self.link_type == self.LINK_PRO

    @property
    def ax_visible(self):
        return is_ax_visible(self.pub)


class ProfilePhoto(models.Model):
    profile = models.OneToOneField(Profile, primary_key=True, db_column='pid', related_name='photo')
    attachmime = models.CharField(max_length=12)
    attach = models.TextField()
    x = models.IntegerField()
    y = models.IntegerField()
    pub = models.CharField(max_length=21)
    last_update = models.DateTimeField()
    class Meta:
        db_table = u'profile_photos'

    def __unicode__(self):
        return self.profile.hrpid


class ProfilePrivateName(models.Model):
    profile = models.ForeignKey(Profile, db_column='pid', related_name='private_name')
    type = models.CharField(max_length=27)
    id = models.IntegerField()
    pkey = models.CompositeField(profile, type, id, primary_key=True)
    name = models.CharField(max_length=765)
    class Meta:
        db_table = u'profile_private_names'

    def __unicode__(self):
        return u"%s: %s" % (self.profile.hrpid, self.type)


class ProfilePublicName(models.Model):
    profile = models.OneToOneField(Profile, primary_key=True, db_column='pid', related_name='public_name')
    lastname_initial = models.CharField(max_length=765)
    lastname_main = models.CharField(max_length=765)
    lastname_marital = models.CharField(max_length=765)
    lastname_ordinary = models.CharField(max_length=765)
    firstname_initial = models.CharField(max_length=765)
    firstname_main = models.CharField(max_length=765)
    firstname_ordinary = models.CharField(max_length=765)
    pseudonym = models.CharField(max_length=765)
    class Meta:
        db_table = u'profile_public_names'

    def __unicode__(self):
        return self.profile.hrpid


# Profile::addresses
# ------------------


class ProfileAddress(models.Model):

    KIND_HOME = 'home'
    KIND_HQ = 'hq'
    KIND_JOB = 'job'
    KIND_GROUP = 'group'

    KIND_CHOICES = (
        (KIND_HOME, u"Home"),
        (KIND_HQ, u"Headquarters"),
        (KIND_JOB, u"Job"),
        (KIND_GROUP, u"Group"),
    )

    profile = models.ForeignKey(Profile, db_column='pid', related_name='addresses')
    job = models.ForeignKey('ProfileJobEnum', db_column='jobid', blank=True, null=True,
        related_name='addresses')
    #job = models.IntegerField(db_column='jobid')
    group = models.ForeignKey('Group', db_column='groupid', blank=True, null=True)
    #groupid = models.IntegerField()
    addr_type = models.CharField(max_length=15, db_column='type', choices=KIND_CHOICES)
    subid = models.IntegerField(db_column='id')
    pkey = models.CompositeField(profile, job, group, addr_type, subid, primary_key=True)
    pjob_key = models.CompositeField(profile, subid)
    pjob = models.ForeignKey('ProfileJob', aux_field='pjob_key')

    flags = models.CharField(max_length=180, blank=True)
    text = models.TextField()
    postaltext = models.TextField(db_column='postalText') # Field name made lowercase.
    formatted_address = models.TextField()
    types = models.CharField(max_length=891)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    southwest_latitude = models.FloatField(null=True, blank=True)
    southwest_longitude = models.FloatField(null=True, blank=True)
    northeast_latitude = models.FloatField(null=True, blank=True)
    northeast_longitude = models.FloatField(null=True, blank=True)
    location_type = models.CharField(max_length=54, blank=True)
    partial_match = models.IntegerField()
    pub = models.CharField(max_length=21)
    comment = models.CharField(max_length=765, blank=True)
    geocoding_date = models.DateField(null=True, blank=True)
    geocoding_calls = models.IntegerField()
    postal_code_fr = models.CharField(max_length=15, blank=True)

    components = models.ManyToManyField('ProfileAddressComponentEnum',
        through='ProfileAddressComponent', related_name='addresses')

    class Meta:
        db_table = u'profile_addresses'

    def __unicode__(self):
        if self.addr_type == self.KIND_HOME:
            rel = self.profile.hrpid
        elif self.addr_type == self.KIND_HQ:
            if self.jobid:
                rel = unicode(self.job)
            else:
                rel = u"[BADJOB]"
        elif self.addr_type == self.KIND_GROUP:
            rel = unicode(self.group)
        else:
            rel = u"%s at %s" % (self.profile.hrpid, self.pjob.company)
        return u"%s address %d for %s" % (
            self.get_addr_type_display(), self.subid, rel)

    @property
    def ax_visible(self):
        return is_ax_visible(self.pub)

    def get_components_by_type(self):
        flags = collections.defaultdict(list)
        for component in self.components.all():
            for cp_type in component.types.split(','):
                flags[cp_type].append(component)
        return flags

    @property
    def flag_list(self):
        return self.flags.split(',')

    FLAG_CURRENT = 'current'
    FLAG_MAIL = 'mail'
    FLAG_SECONDARY = 'secondary'

    @property
    def current(self):
        return self.FLAG_CURRENT in self.flag_list

    @property
    def mail(self):
        return self.FLAG_MAIL in self.flag_list

    @property
    def secondary(self):
        return self.FLAG_SECONDARY in self.flag_list

    @property
    def is_home(self):
        return self.addr_type == self.KIND_HOME

    @property
    def is_job(self):
        return self.addr_type == self.KIND_JOB


class ProfileAddressComponentEnum(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    short_name = models.CharField(max_length=765)
    long_name = models.CharField(max_length=765)
    types = models.CharField(max_length=891)
    class Meta:
        db_table = u'profile_addresses_components_enum'

    def __unicode__(self):
        return u'%s (%s)' % (self.short_name, self.types)


class ProfileAddressComponent(models.Model):
    profile = models.ForeignKey(Profile, db_column='pid')
    job = models.ForeignKey('ProfileJobEnum', db_column='jobid')
    group = models.ForeignKey(Group, db_column='groupid', blank=True, null=True)
    addr_type = models.CharField(max_length=15, db_column='type')
    subid = models.IntegerField(db_column='id')
    pkey = models.CompositeField(profile, job, group, addr_type, subid, primary_key=True)

    component = models.ForeignKey(ProfileAddressComponentEnum, related_name='component_links')
    address = models.ForeignKey(ProfileAddress, related_name='component_links',
        aux_field='pkey')
    class Meta:
        db_table = u'profile_addresses_components'

    def __unicode__(self):
        return u"%s (%s) for %s" % (
            self.component.long_name,
            self.component.types,
            self.address,
        )


# Profile::networking
# -------------------


class ProfileBinetEnum(models.Model):
    #id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=150)
    url = models.CharField(max_length=765)
    class Meta:
        db_table = u'profile_binet_enum'


class ProfileBinet(models.Model):
    profile = models.ForeignKey(Profile, db_column='pid')
    binet = models.ForeignKey(ProfileBinetEnum)
    pkey = models.CompositeField(profile, binet, primary_key=True)
    class Meta:
        db_table = u'profile_binets'


class ProfileHobby(models.Model):
    profile = models.ForeignKey(Profile, db_column='pid')
    id = models.IntegerField()
    pkey = models.CompositeField(profile, id, primary_key=True)
    type = models.CharField(max_length=18)
    text = models.CharField(max_length=765)
    pub = models.CharField(max_length=21)
    class Meta:
        db_table = u'profile_hobby'


class ProfileNetworkingEnum(models.Model):
    nwid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=90)
    icon = models.CharField(max_length=150)
    filter = models.CharField(max_length=18)
    network_type = models.CharField(max_length=18)
    link = models.CharField(max_length=765)
    class Meta:
        db_table = u'profile_networking_enum'


class ProfileNetworking(models.Model):
    profile = models.ForeignKey(Profile, db_column='pid')
    id = models.IntegerField()
    nwid = models.ForeignKey(ProfileNetworkingEnum, db_column='nwid')
    pkey = models.CompositeField(id, nwid, primary_key=True)
    address = models.CharField(max_length=765)
    pub = models.CharField(max_length=21)
    class Meta:
        db_table = u'profile_networking'


# Profile::corps
# --------------


class ProfileCorpsEnum(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=15, unique=True)
    still_exists = models.IntegerField()
    class Meta:
        db_table = u'profile_corps_enum'

    def __unicode__(self):
        return self.name


class ProfileCorpsRankEnum(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=15, unique=True)
    class Meta:
        db_table = u'profile_corps_rank_enum'

    def __unicode__(self):
        return self.name


class ProfileCorps(models.Model):
    profile = models.OneToOneField(Profile, primary_key=True, db_column='pid')
    original = models.ForeignKey(ProfileCorpsEnum, db_column='original_corpsid', related_name='original_members')
    current = models.ForeignKey(ProfileCorpsEnum, db_column='current_corpsid', related_name='current_members')
    rank = models.ForeignKey(ProfileCorpsRankEnum, db_column='rankid')
    # Ignored: corps is public information anyway.
    corps_pub = models.CharField(max_length=21)
    class Meta:
        db_table = u'profile_corps'

    def __unicode__(self):
        return u"%s: %s" % (self.profile.hrpid, self.current.name)


# Profile::edu
# ------------


class ProfileEducationEnum(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, blank=True)
    abbreviation = models.CharField(max_length=765)
    url = models.CharField(max_length=765, blank=True)
    country = models.ForeignKey(GeolocCountry, null=True, db_column='country', blank=True)
    class Meta:
        db_table = u'profile_education_enum'

    def __unicode__(self):
        return self.name

    @property
    def short(self):
        return self.abbreviation or self.name


class ProfileEducationDegreeEnum(models.Model):
    #id = models.IntegerField(primary_key=True)
    degree = models.CharField(max_length=255, unique=True, blank=True)
    abbreviation = models.CharField(max_length=765)
    level = models.IntegerField()
    class Meta:
        db_table = u'profile_education_degree_enum'

    def __unicode__(self):
        return self.degree


class ProfileEducationFieldEnum(models.Model):
    #id = models.IntegerField(primary_key=True)
    field = models.CharField(max_length=255, unique=True, blank=True)
    class Meta:
        db_table = u'profile_education_field_enum'

    def __unicode__(self):
        return self.field


class ProfileEducation(models.Model):
    id = models.IntegerField()
    profile = models.ForeignKey(Profile, db_column='pid', related_name='educations')
    pkey = models.CompositeField(id, profile, primary_key=True)

    school = models.ForeignKey(ProfileEducationEnum, null=True, db_column='eduid', blank=True)
    degree = models.ForeignKey(ProfileEducationDegreeEnum, null=True, db_column='degreeid', blank=True)
    field = models.ForeignKey(ProfileEducationFieldEnum, null=True, db_column='fieldid', blank=True)
    entry_year = models.IntegerField(null=True, blank=True)
    grad_year = models.IntegerField(null=True, blank=True)
    promo_year = models.IntegerField(null=True, blank=True)
    program = models.CharField(max_length=765, blank=True)
    flags = models.CharField(max_length=81)
    class Meta:
        db_table = u'profile_education'

    def __unicode__(self):
        return u"%s: %s" % (self.profile.hrpid, self.edu.name)


class ProfileEducationDegree(models.Model):
    edu = models.ForeignKey(ProfileEducationEnum, db_column='eduid')
    degree = models.ForeignKey(ProfileEducationDegreeEnum, db_column='degreeid')
    pkey = models.CompositeField(edu, degree, primary_key=True)
    class Meta:
        db_table = u'profile_education_degree'

    def __unicode__(self):
        return u"%s - %s" % (self.edu, self.degree)


# Profile::jobs
# -------------


class ProfileJobEnum(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    acronym = models.CharField(max_length=765, blank=True)
    url = models.CharField(max_length=765, blank=True)
    email = models.CharField(max_length=765, blank=True)
    holding = models.ForeignKey('self', null=True, db_column='holdingid', blank=True)
    naf_code = models.CharField(max_length=15, db_column='NAF_code', blank=True) # Field name made lowercase.
    ax_code = models.BigIntegerField(null=True, db_column='AX_code', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'profile_job_enum'

    def __unicode__(self):
        return self.name

    @property
    def address(self):
        if not hasattr(self, '_address'):

            self._address = None
            for address in self.addresses.all():
                if address.addr_type == address.KIND_HQ:
                    self._address = address
                    break
        return self._address


class ProfileJob(models.Model):
    id = models.IntegerField()
    profile = models.ForeignKey(Profile, db_column='pid', related_name='jobs')
    pkey = models.CompositeField(profile, id, primary_key=True)

    company = models.ForeignKey(ProfileJobEnum, null=True, db_column='jobid', blank=True)
    description = models.CharField(max_length=765)
    url = models.CharField(max_length=765)
    email = models.CharField(max_length=765)
    pub = models.CharField(max_length=21)
    email_pub = models.CharField(max_length=21)
    entry_year = models.CharField(max_length=12, blank=True)
    class Meta:
        db_table = u'profile_job'

    @property
    def ax_visible(self):
        return is_ax_visible(self.pub)

    @property
    def ax_visible_email(self):
        return is_ax_visible(self.email_pub)

    def __unicode__(self):
        return u"%s at %s" % (self.profile.hrpid, self.company.name if self.company else '<NONE>')


# Profile::job::terms
# -------------------


class ProfileJobTermEnum(models.Model):
    jtid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=765)
    full_name = models.CharField(max_length=765)
    class Meta:
        db_table = u'profile_job_term_enum'

    def __unicode__(self):
        return self.name


class ProfileJobTermRelation(models.Model):
    jtid_1 = models.ForeignKey(ProfileJobTermEnum, db_column='jtid_1', related_name='relations_from')
    jtid_2 = models.ForeignKey(ProfileJobTermEnum, db_column='jtid_2', related_name='relations_to')
    rel = models.CharField(max_length=24)
    computed = models.CharField(max_length=24)
    pkey = models.CompositeField(jtid_1, jtid_2, computed, primary_key=True)
    class Meta:
        db_table = u'profile_job_term_relation'

    def __unicode__(self):
        return u"%s <-> %s" % (self.jtid_1.name, self.jtid_2.name)


class ProfileJobTermSearch(models.Model):
    search = models.CharField(max_length=150)
    job_term = models.ForeignKey(ProfileJobTermEnum, db_column='jtid')
    pkey = models.CompositeField(search, job_term, primary_key=True)
    class Meta:
        db_table = u'profile_job_term_search'

    def __unicode__(self):
        return u"%s => %s" % (self.search, self.job_term.name)


class ProfileJobTerm(models.Model):
    profile = models.ForeignKey(Profile, db_column='pid')
    company = models.ForeignKey(ProfileJobEnum, db_column='jid')
    job = models.ForeignKey(ProfileJob, to_field='pkey')
    job_term = models.ForeignKey(ProfileJobTermEnum, db_column='jtid')
    computed = models.CharField(max_length=24)
    pkey = models.CompositeField(profile, company, job_term, primary_key=True)
    class Meta:
        db_table = u'profile_job_term'

    def __unicode__(self):
        return u"%s at %s: %s" % (self.profile.hrpid, self.company.name, self.job_term.name)


class ProfileJobEntrepriseTerm(models.Model):
    job = models.ForeignKey(ProfileJobEnum, db_column='eid')
    job_term = models.ForeignKey(ProfileJobTermEnum, db_column='jtid')
    pkey = models.CompositeField(job, job_term, primary_key=True)
    class Meta:
        db_table = u'profile_job_entreprise_term'

    def __unicode__(self):
        return u"%s: %s" % (self.job.name, self.job_term.name)


# Profile::skills
# ---------------


class ProfileLangSkillEnum(models.Model):
    iso_639_2b = models.CharField(max_length=9, primary_key=True)
    language = models.CharField(max_length=765)
    language_en = models.CharField(max_length=765)
    iso_639_2t = models.CharField(max_length=9)
    iso_639_1 = models.CharField(max_length=6, blank=True)
    class Meta:
        db_table = u'profile_langskill_enum'

    def __unicode__(self):
        return self.iso_639_2b


class ProfileLangSkill(models.Model):
    profile = models.ForeignKey(Profile, db_column='pid')
    lang = models.ForeignKey(ProfileLangSkillEnum, db_column='lid')
    pkey = models.CompositeField(profile, lang, primary_key=True)
    level = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'profile_langskills'

    def __unicode__(self):
        return u"%s: %s" % (self.profile.hrpid, self.lang.iso_639_2b)


class ProfileSkillEnum(models.Model):
    id = models.CharField(max_length=9, primary_key=True)
    text_fr = models.CharField(max_length=330)
    text_en = models.CharField(max_length=330)
    flags = models.CharField(max_length=15)
    class Meta:
        db_table = u'profile_skill_enum'

    def __unicode__(self):
        return self.text_en


class ProfileSkill(models.Model):
    profile = models.ForeignKey(Profile, db_column='pid')
    skill = models.ForeignKey(ProfileSkillEnum, db_column='cid')
    pkey = models.CompositeField(profile, skill, primary_key=True)
    level = models.CharField(max_length=54)
    class Meta:
        db_table = u'profile_skills'

    def __unicode__(self):
        return u"%s: %s" % (self.profile.hrpid, self.skill.text_en)


# Profile::medals
# ---------------


class ProfileMedalEnum(models.Model):
    #id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=30)
    text = models.CharField(max_length=765, blank=True)
    img = models.CharField(max_length=765, blank=True)
    flags = models.CharField(max_length=63)
    class Meta:
        db_table = u'profile_medal_enum'


class ProfileMedalGradeEnum(models.Model):
    medal = models.ForeignKey(ProfileMedalEnum, db_column='mid')
    gid = models.IntegerField()
    pkey = models.CompositeField(medal, gid, primary_key=True)
    text = models.CharField(max_length=765, blank=True)
    pos = models.IntegerField()
    class Meta:
        db_table = u'profile_medal_grade_enum'


class ProfileMedal(models.Model):
    profile = models.ForeignKey(Profile, db_column='pid')
    medal = models.ForeignKey(ProfileMedalEnum)
    gid = models.IntegerField()
    grade = models.ForeignKey(ProfileMedalGradeEnum, to_field='pkey')
    pkey = models.CompositeField(profile, medal, gid, primary_key=True)
    level = models.CharField(max_length=18)
    class Meta:
        db_table = u'profile_medals'


# Profile::mentor
# ---------------


class ProfileMentor(models.Model):
    profile = models.OneToOneField(Profile, primary_key=True, db_column='pid')
    expertise = models.TextField()
    class Meta:
        db_table = u'profile_mentor'


class ProfileMentorCountry(models.Model):
    profile = models.ForeignKey(Profile, db_column='pid')
    country = models.ForeignKey(GeolocCountry, db_column='country')
    pkey = models.CompositeField(profile, country, primary_key=True)
    class Meta:
        db_table = u'profile_mentor_country'


class ProfileMentorTerm(models.Model):
    profile = models.ForeignKey(Profile, db_column='pid')
    job_term = models.ForeignKey(ProfileJobTermEnum, db_column='jtid')
    pkey = models.CompositeField(profile, job_term, primary_key=True)
    class Meta:
        db_table = u'profile_mentor_term'


# Profile::partner
# ----------------


class ProfilePartnersharingEnum(models.Model):
    #id = models.IntegerField(primary_key=True)
    api_account = models.ForeignKey(Account, null=True, db_column='api_uid', blank=True)
    shortname = models.CharField(max_length=192)
    name = models.CharField(max_length=765)
    url = models.CharField(max_length=765)
    default_sharing_level = models.CharField(max_length=21, blank=True)
    has_directory = models.IntegerField()
    has_bulkmail = models.IntegerField()
    class Meta:
        db_table = u'profile_partnersharing_enum'


class ProfilePartnersharingSetting(models.Model):
    profile = models.ForeignKey(Profile, db_column='pid')
    partner = models.ForeignKey(ProfilePartnersharingEnum)
    pkey = models.CompositeField(profile, partner, primary_key=True)
    exposed_uid = models.CharField(max_length=765)
    sharing_level = models.CharField(max_length=21, blank=True)
    allow_email = models.CharField(max_length=18, blank=True)
    last_connection = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'profile_partnersharing_settings'


class ProfilePhotoToken(models.Model):
    profile = models.ForeignKey(Profile, primary_key=True, db_column='pid')
    token = models.CharField(max_length=765)
    expires = models.DateTimeField()
    class Meta:
        db_table = u'profile_photo_tokens'


# Profile::misc
# -------------


class ProfileMergeIssue(models.Model):
    profile = models.ForeignKey(Profile, primary_key=True, db_column='pid')
    issues = models.CharField(max_length=144, blank=True)
    entry_year_ax = models.IntegerField(null=True, blank=True)
    deathdate_ax = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=765, blank=True)
    name_type = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'profile_merge_issues'


class ProfileModification(models.Model):
    profile = models.ForeignKey(Profile, db_column='pid')
    account = models.ForeignKey(Account, db_column='uid')
    field = models.CharField(max_length=180)
    pkey = models.CompositeField(profile, field, primary_key=True)
    oldtext = models.TextField(db_column='oldText')
    newtext = models.TextField(db_column='newText')
    type = models.CharField(max_length=33)
    timestamp = models.DateTimeField()
    class Meta:
        db_table = u'profile_modifications'


class ProfileVisibilityEnum(models.Model):
    access_level = models.CharField(max_length=21, blank=True, primary_key=True)
    best_display_level = models.CharField(max_length=21, blank=True)
    display_levels = models.CharField(max_length=72, blank=True)
    class Meta:
        db_table = u'profile_visibility_enum'



class ProfileDeltaten(models.Model):
    profile = models.OneToOneField(Profile, primary_key=True, db_column='pid')
    message = models.TextField()
    class Meta:
        db_table = u'profile_deltaten'


# Reminders
# =========


class ReminderType(models.Model):
    #type_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    weight = models.IntegerField()
    remind_delay_yes = models.IntegerField()
    remind_delay_no = models.IntegerField()
    remind_delay_dismiss = models.IntegerField()
    class Meta:
        db_table = u'reminder_type'


class Reminder(models.Model):
    account = models.ForeignKey(Account, db_column='uid')
    type = models.ForeignKey(ReminderType)
    pkey = models.CompositeField(account, type, primary_key=True)
    status = models.CharField(max_length=21)
    remind_last = models.DateTimeField()
    remind_next = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'reminder'


class ReminderTip(models.Model):
    #id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=192)
    text = models.TextField()
    priority = models.IntegerField()
    expiration = models.DateField()
    promo_min = models.IntegerField()
    promo_max = models.IntegerField()
    state = models.CharField(max_length=18)
    class Meta:
        db_table = u'reminder_tips'


# Surveys
# =======


class Survey(models.Model):
    #id = models.IntegerField(primary_key=True)
    questions = models.TextField()
    title = models.CharField(max_length=765)
    description = models.TextField()
    account = models.ForeignKey(Account, null=True, db_column='uid', blank=True)
    end = models.DateField()
    mode = models.IntegerField()
    promos = models.CharField(max_length=765)
    class Meta:
        db_table = u'surveys'


class SurveyVote(models.Model):
    #id = models.IntegerField(primary_key=True)
    survey = models.ForeignKey(Survey)
    account = models.ForeignKey(Account, null=True, db_column='uid', blank=True)
    class Meta:
        db_table = u'survey_votes'


class SurveyAnswer(models.Model):
    #id = models.IntegerField(primary_key=True)
    vote = models.ForeignKey(SurveyVote)
    question_id = models.IntegerField()
    answer = models.TextField()
    class Meta:
        db_table = u'survey_answers'


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
        db_table = u'gapps_accounts'


class GappsNickname(models.Model):
    l_userid = models.ForeignKey(Account, null=True, db_column='l_userid', blank=True)
    g_account_name = models.CharField(max_length=768)
    g_nickname = models.CharField(max_length=255, primary_key=True)
    class Meta:
        db_table = u'gapps_nicknames'


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
        db_table = u'gapps_queue'


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
        db_table = u'gapps_reporting'



# Watch
# =====


class Watch(models.Model):
    account = models.ForeignKey(Account, primary_key=True, db_column='uid')
    flags = models.CharField(max_length=39)
    actions = models.CharField(max_length=105)
    last = models.DateTimeField()
    class Meta:
        db_table = u'watch'


class WatchGroup(models.Model):
    account = models.ForeignKey(Account, db_column='uid')
    group = models.ForeignKey(Group, db_column='groupid')
    pkey = models.CompositeField(account, group, primary_key=True)
    class Meta:
        db_table = u'watch_group'


class WatchNonins(models.Model):
    account = models.ForeignKey(Account, db_column='uid', related_name='watching')
    watched = models.ForeignKey(Account, db_column='ni', related_name='watched_by')
    pkey = models.CompositeField(account, watched, primary_key=True)
    class Meta:
        db_table = u'watch_nonins'


class WatchProfile(models.Model):
    profile = models.ForeignKey(Profile, db_column='pid')
    ts = models.DateTimeField()
    field = models.CharField(max_length=36)
    pkey = models.CompositeField(profile, field, primary_key=True)
    class Meta:
        db_table = u'watch_profile'


class WatchPromo(models.Model):
    account = models.ForeignKey(Account, db_column='uid')
    promo = models.IntegerField()
    pkey = models.CompositeField(account, promo, primary_key=True)
    class Meta:
        db_table = u'watch_promo'


# Postfix
# =======


class MxWatch(models.Model):
    host = models.CharField(max_length=192, primary_key=True)
    state = models.CharField(max_length=21, blank=True)
    text = models.TextField()
    class Meta:
        db_table = u'mx_watch'


class PostfixBlacklist(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    reject_text = models.CharField(max_length=192)
    class Meta:
        db_table = u'postfix_blacklist'


class PostfixMailseen(models.Model):
    crc = models.CharField(max_length=24, primary_key=True)
    nb = models.IntegerField()
    update_time = models.DateTimeField()
    create_time = models.DateTimeField()
    release = models.CharField(max_length=18)
    class Meta:
        db_table = u'postfix_mailseen'


class PostfixWhitelist(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    class Meta:
        db_table = u'postfix_whitelist'


# Register
# ========


class RegisterMarketing(models.Model):
    account = models.ForeignKey(Account, db_column='uid', related_name='received_marketings')
    sender = models.ForeignKey(Account, null=True, db_column='sender', blank=True, related_name='sent_marketings')
    email = models.CharField(max_length=765)
    pkey = models.CompositeField(account, email, primary_key=True)

    date = models.DateField()
    last = models.DateField()
    nb = models.IntegerField()
    type = models.CharField(max_length=15, blank=True)
    hash = models.CharField(max_length=96)
    message = models.CharField(max_length=48)
    message_data = models.CharField(max_length=192, blank=True)
    personal_notes = models.TextField(blank=True)
    class Meta:
        db_table = u'register_marketing'


class RegisterMstat(models.Model):
    account = models.OneToOneField(Account, primary_key=True, db_column='uid', related_name='received_marketings_stats')
    sender = models.ForeignKey(Account, null=True, db_column='sender', blank=True, related_name='sent_marketings_stats')
    success = models.DateField()
    class Meta:
        db_table = u'register_mstats'


class RegisterPending(models.Model):
    account = models.OneToOneField(Account, primary_key=True, db_column='uid')
    forlife = models.CharField(max_length=255, unique=True)
    bestalias = models.CharField(max_length=255, unique=True)
    mailorg2 = models.CharField(max_length=765, blank=True)
    password = models.CharField(max_length=120)
    email = models.CharField(max_length=765)
    date = models.DateField()
    relance = models.DateField()
    naissance = models.DateField()
    hash = models.CharField(max_length=36)
    services = models.CharField(max_length=78)
    class Meta:
        db_table = u'register_pending'


class RegisterPendingXnet(models.Model):
    account = models.ForeignKey(Account, primary_key=True, db_column='uid', related_name='pending_xnet_register')
    hruid = models.ForeignKey(Account, unique=True, db_column='hruid', related_name='pending_xnet_register_by_hruid')
    email = models.CharField(max_length=765)
    date = models.DateField()
    last_date = models.DateField(null=True, blank=True)
    hash = models.CharField(max_length=36)
    sender_name = models.CharField(max_length=765)
    group_name = models.CharField(max_length=765)
    class Meta:
        db_table = u'register_pending_xnet'


class RegisterSubs(models.Model):
    account = models.ForeignKey(Account, db_column='uid')
    type = models.CharField(max_length=15)
    sub = models.CharField(max_length=96)
    domain = models.CharField(max_length=192)
    pkey = models.CompositeField(account, type, sub, domain, primary_key=True)
    class Meta:
        db_table = u'register_subs'


# Search
# ======


class SearchAutocomplete(models.Model):
    name = models.CharField(max_length=60)
    query = models.CharField(max_length=300)
    pkey = models.CompositeField(name, query, primary_key=True)
    result = models.TextField()
    generated = models.DateTimeField()
    class Meta:
        db_table = u'search_autocomplete'


class SearchName(models.Model):
    profile = models.ForeignKey(Profile, db_column='pid')
    token = models.CharField(max_length=765)
    pkey = models.CompositeField(profile, token, primary_key=True)
    score = models.IntegerField()
    soundex = models.CharField(max_length=12)
    flags = models.CharField(max_length=18)
    general_type = models.CharField(max_length=27)
    class Meta:
        db_table = u'search_name'


# Requests
# ========


class Request(models.Model):
    account = models.ForeignKey(Account, db_column='uid')
    type = models.CharField(max_length=48)
    data = models.TextField()
    stamp = models.DateTimeField()
    profile = models.ForeignKey(Profile, null=True, db_column='pid', blank=True)
    pkey = models.CompositeField(account, stamp, type, primary_key=True)
    class Meta:
        db_table = u'requests'


class RequestAnswer(models.Model):
    #id = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=45)
    title = models.CharField(max_length=150)
    answer = models.TextField()
    class Meta:
        db_table = u'requests_answers'


class RequestHidden(models.Model):
    account = models.ForeignKey(Account, primary_key=True, db_column='uid')
    hidden_requests = models.TextField()
    class Meta:
        db_table = u'requests_hidden'


# Misc
# ====


class AXLetter(models.Model):
    #id = models.IntegerField(primary_key=True)
    short_name = models.CharField(max_length=48, unique=True, blank=True)
    subject = models.CharField(max_length=765)
    title = models.CharField(max_length=765)
    body = models.TextField()
    signature = models.TextField()
    promo_min = models.IntegerField()
    promo_max = models.IntegerField()
    subset = models.TextField(blank=True)
    subset_rm = models.IntegerField(null=True, blank=True)
    echeance = models.DateTimeField()
    date = models.DateField()
    bits = models.CharField(max_length=48)
    class Meta:
        db_table = u'axletter'


class Carva(models.Model):
    account = models.ForeignKey(Account, primary_key=True, db_column='uid')
    url = models.CharField(max_length=765)
    class Meta:
        db_table = u'carvas'


class Contact(models.Model):
    account = models.ForeignKey(Account, db_column='uid')
    contact = models.ForeignKey(Profile, db_column='contact')
    pkey = models.CompositeField(account, contact, primary_key=True)
    class Meta:
        db_table = u'contacts'


class Downtime(models.Model):
    debut = models.DateTimeField()
    duree = models.TimeField() # This field type is a guess.
    resume = models.CharField(max_length=765)
    description = models.TextField()
    services = models.CharField(max_length=54)
    class Meta:
        db_table = u'downtimes'


class EmailListModerate(models.Model):
    ml = models.CharField(max_length=192)
    domain = models.CharField(max_length=192)
    mid = models.IntegerField()
    pkey = models.CompositeField(ml, domain, mid, primary_key=True)
    account = models.ForeignKey(Account, null=True, db_column='uid', blank=True)
    action = models.CharField(max_length=18)
    ts = models.DateTimeField()
    message = models.TextField(blank=True)
    handler = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'email_list_moderate'


class EmailSendSave(models.Model):
    account = models.OneToOneField(Account, primary_key=True, db_column='uid')
    data = models.TextField()
    class Meta:
        db_table = u'email_send_save'


class EmailWatch(models.Model):
    email = models.CharField(max_length=180, primary_key=True)
    state = models.CharField(max_length=27)
    detection = models.DateField(null=True, blank=True)
    last = models.DateTimeField()
    account = models.ForeignKey(Account, null=True, db_column='uid', blank=True)
    description = models.TextField()
    class Meta:
        db_table = u'email_watch'


class GeolocLanguage(models.Model):
    iso_3166_1_a2 = models.ForeignKey(GeolocCountry, db_column='iso_3166_1_a2')
    language = models.CharField(max_length=15)
    pkey = models.CompositeField(iso_3166_1_a2, language, primary_key=True)
    country = models.CharField(max_length=765, blank=True)
    countryplain = models.CharField(max_length=765, db_column='countryPlain', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'geoloc_languages'


class HomonymList(models.Model):
    hrmid = models.CharField(max_length=765)
    account = models.ForeignKey(Account, db_column='uid')
    pkey = models.CompositeField(hrmid, account, primary_key=True)
    class Meta:
        db_table = u'homonyms_list'


class UrlShortener(models.Model):
    alias = models.CharField(max_length=255, primary_key=True)
    url = models.TextField()
    class Meta:
        db_table = u'url_shortener'

