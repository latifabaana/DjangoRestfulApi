import factory
from django.test import TestCase
from django.conf import settings
from django.core.files import File

from .models import *

# creates model factories for each model with dummy data already inserted. 

class OrganismFactory(factory.django.DjangoModelFactory):
    taxa_id = 53326
    clade = 'E'
    genus = 'Ancylostoma'
    species = 'ceylanicum'

    class Meta:
        model = Organism


class PFamFactory(factory.django.DjangoModelFactory):
    domain_id = 'PF01650'
    domain_description = 'PeptidaseC13family'

    class Meta:
        model = PFam

class DomainFactory(factory.django.DjangoModelFactory):
    protein_id = 'A0A016S8J7'
    description = 'Peptidase C13 legumain'
    start = 40
    stop = 94
    pfam_id = factory.SubFactory(PFamFactory)

    class Meta:
        model = Domain

class ProteinFactory(factory.django.DjangoModelFactory):
    protein_id = 'A0A016S8J7'
    sequence = 'MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA'
    length = 101
    taxonomy = factory.SubFactory(OrganismFactory)

    class Meta:
        model = Protein

    @factory.post_generation
    def domain(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for domain in extracted:
                self.domain.add(domain)

class DomainProteinLinkFactory(factory.django.DjangoModelFactory):
    protein = factory.SubFactory(ProteinFactory)
    domain = factory.SubFactory(DomainFactory)

    class Meta:
        model = DomainProteinLink