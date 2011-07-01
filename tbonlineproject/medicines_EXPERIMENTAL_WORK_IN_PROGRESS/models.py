'''WORK IN PROGRESS'''

from django.db import models
from django.utils.translation import ugettext_lazy as _

from enhancedtext.fields import EnhancedTextField 
from archive.models import Document
from gallery.models import Image

UNIT_MEASUREMENTS = (
    ('mg', _('milligrams')),
    ('g', _('grams')),
    ('ml', _('millilitres')),
)

FORMULATIONS = (
    ('T', _('tablet')),
    ('C', _('capsule')),
    ('S', _('syrup')),
)

APPROVAL_ACTIONS = (
    ('A', _('approval')),
    ('X', _('withdrawal')),
    ('W', _('warning')),
    ('L', _('leaflet change')),
)    

STUDY_TYPES = (
    ('RCT1', _('double-blinded randomised controlled trial')),
    ('RCT2', _('blinded randomised controlled trial')),
    ('RCT3', _('open label randomised controlled trial')),
    ('CASE', _('case controlled study')),
    ('PO', _('prospective observational study')),
    ('RO', _('retrospective cohort'))
)

STUDY_QUALITIES = (
    ('1', _('very high')),
    ('2', _('high')),
    ('3', _('average')),
    ('4', _('poor')),
    ('5', _('very poor'))
)


class Region(models.Model):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name',]

class Sector(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name',]

class GroupOfPeopleOrAnimals(models.Model):
    name = models.CharField(max_length=200)    

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name',]
    
class Study(models.Model):
    name = models.CharField(max_length=200)
    date_published = models.DateField()    
    description = models.TextField(blank=True)
    study_type = models.CharField(max_length=3, choices=STUDY_TYPES, blank=True)
    phase_if_clinical_trial = models.SmallIntegerField(blank=True, null=True)
    study_quality = models.CharField(max_length=1, choices=STUDY_QUALITIES, blank=True)
    source = models.CharField(max_length=300, blank=True)
    url = models.URLField(verify_exists=False, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['date_published',]

class Condition(models.Model):
    name = models.CharField(max_length=200)
    description = EnhancedTextField(blank=True, default="\W")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name',]
    
class SideEffect(models.Model):
    condition_or_symptom = models.ForeignKey(Condition)
    group_of_people_or_animals = models.ManyToManyField(GroupOfPeopleOrAnimals)
    frequency = models.FloatField(blank=True, null=True)
    studies = models.ManyToManyField(Study)

    def __unicode__(self):
        return self.condition_or_symptom.name

    class Meta:
        ordering = ['condition_or_symptom__name',]
    
class Drug(models.Model):
    name = models.CharField(max_length=200, unique=True)
    synopsis = EnhancedTextField(blank=True, default="\W")
    formula = models.CharField(max_length=200, blank=True)
    chemical_photo = models.ForeignKey(Image, blank=True, null=True)
    studies = models.ManyToManyField(Study)
    side_effects = models.ManyToManyField(SideEffect)
    
    

class Company(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(verify_exists=False)
    hq_address = models.TextField(blank=True)
    postal_address = models.TextField(blank=True)
    
class Brand(models.Model):
    name = models.CharField(max_length=200, unique=True)
    company = models.ForeignKey(Company)
    originator = models.BooleanField(default=False)

class Ingredient(models.Model):
    drug = models.ForeignKey(Drug)
    dosage = models.FloatField()
    dosage_units = models.CharField(max_length=5, choices=UNIT_MEASUREMENTS)

class Currency(models.Model):
    name = models.CharField(max_length=200, unique=True)
    abbreviation = models.CharField(max_length=3, blank=True)
    symbol = models.CharField(max_length=2, blank=True)

class ProductPrice(models.Model):
    region = models.ForeignKey(Region)
    sector = models.ForeignKey(Sector)
    currency = models.ForeignKey(Currency)
    price = models.DecimalField()
    price_date = models.DateField()
    source = models.CharField(max_length=300)

class Product(models.Model):
    brand = models.ForeignKey(Brand)
    ingredients = models.ManyToManyField(Ingredient)
    formulation = models.CharField(max_length=2, choices=FORMULATIONS)
    volume = models.FloatField()
    volume_units = models.CharField(max_length=5, choices=UNIT_MEASUREMENTS)
    prices = models.ManyToManyField(ProductPrice)

class ApprovedCondition(models.Model):
    name = models.ForeignKey(Condition)
    group_of_people_or_animals_for_whom_approved = models.ForeignKey(GroupOfPeopleOrAnimals)
    
class Authority(models.Model):
    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region)
 
class Approval(models.Model):
    authority = models.ForeignKey(Authority)
    product = models.ForeignKey(Product)
    approved_conditions = models.ManyToManyField(ApprovedCondition)

class ApprovalAction(models.Model):
    approval = models.ForeignKey(Approval)
    action = models.CharField(max_length=2, choices=APPROVAL_ACTIONS)
    action_date = models.DateField(blank=True, null=True)
    patient_leaflet = models.ForeignKey(Document, blank=True, null=True)


