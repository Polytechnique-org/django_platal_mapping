# -*- coding: utf-8 -*-

from django.db import models

VISIBILITY_CHOICES = (
    'hidden',
    'private',
    'ax',
    'public',
)

#
# Geoloc
#

class GeolocCountries(models.Model):
    """Represents a country."""
    # country code
    iso_3166_1_a2 = models.CharField(max_length=2, primary_key=True)

    iso_3166_1_a3 = models.CharField(unique=True, max_length=3)
    iso_3166_1_num = models.IntegerField(unique=True)
    worldregion = models.CharField(db_column='worldRegion', max_length=2, blank=True) # Field name made lowercase.
    country = models.CharField(max_length=255, blank=True)
    countryen = models.CharField(db_column='countryEn', max_length=255, blank=True) # Field name made lowercase.
    capital = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255, blank=True)
    nationalityen = models.CharField(db_column='nationalityEn', max_length=255, blank=True) # Field name made lowercase.
    phoneprefix = models.IntegerField(db_column='phonePrefix', blank=True, null=True) # Field name made lowercase.
    phoneformat = models.CharField(db_column='phoneFormat', max_length=255) # Field name made lowercase.
    licenseplate = models.CharField(db_column='licensePlate', max_length=4, blank=True) # Field name made lowercase.
    belongsto = models.ForeignKey('self', db_column='belongsTo', blank=True, null=True) # Field name made lowercase.
    countryplain = models.CharField(db_column='countryPlain', max_length=255, blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'geoloc_countries'

#
# Profile
#

class ProfileSectionEnum(models.Model):
    """Enum of the sport sections."""
    id = models.IntegerField(primary_key=True)
    text = models.CharField(unique=True, max_length=50)
    class Meta:
        managed = False
        db_table = 'profile_section_enum'

class Profile(models.Model):
    """The base profile class."""
    SEX_CHOICES = (
        'female',
        'male',
    )

    TITLE_CHOICES = (
        'M',
        'MLLE',
        'MME',
    )

    pid = models.IntegerField(primary_key=True)
    hrpid = models.CharField(unique=True, max_length=255)
    xorg_id = models.IntegerField()
    ax_id = models.CharField(max_length=8, blank=True)
    birthdate = models.DateField(blank=True, null=True)
    birthdate_ref = models.DateField(blank=True, null=True)
    next_birthday = models.DateField(blank=True, null=True)
    deathdate = models.DateField(blank=True, null=True)
    deathdate_rec = models.DateField(blank=True, null=True)
    sex = models.CharField(choices=SEX_CHOICES)
    section = models.ForeignKey(ProfileSectionEnum, db_column='section', blank=True, null=True)
    cv = models.TextField(blank=True)
    freetext = models.TextField(blank=True)
    freetext_pub = models.CharField(choices=VISIBILITY_CHOICES)
    axfreetext = models.TextField(blank=True)
    medals_pub = models.CharField(choices=VISIBILITY_CHOICES)
    alias_pub = models.CharField(choices=VISIBILITY_CHOICES)
    nationality1 = models.ForeignKey(GeolocCountries, db_column='nationality1', blank=True, null=True)
    nationality2 = models.ForeignKey(GeolocCountries, db_column='nationality2', blank=True, null=True)
    nationality3 = models.ForeignKey(GeolocCountries, db_column='nationality3', blank=True, null=True)
    email_directory = models.CharField(max_length=255, blank=True)
    last_change = models.DateField()
    title = models.CharField(choices=TITLE_CHOICES)
    class Meta:
        managed = False
        db_table = 'profiles'
