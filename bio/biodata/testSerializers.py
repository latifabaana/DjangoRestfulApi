import json
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponse
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

# change these to ..becauase it's in a folder now.
from .model_factories import *
from .serializers import *

# test serializers
class SerializerTest(APITestCase):
    
    # test protein serializer
    def test_proteinSerializer(self):
        protein = ProteinFactory.create()
        proteinSerializer = ProteinSerializer(instance = protein)
        protein_data = proteinSerializer.data
        self.assertEqual(set(protein_data.keys()), set(['protein_id', 'sequence', 'length', 'taxonomy', 'domain']))
        # tests.py checks if it api requests returns the right data. 

    # test domain serializer
    def test_domainSerilizer(self):
        domain = DomainFactory.create()
        domainSerializer = DomainSerializer(instance = domain)
        domain_data = domainSerializer.data
        self.assertEqual(set(domain_data.keys()), set(['pfam_id', 'description', 'start', 'stop']))
    
    # test organism/taxonomy serializer
    def test_taxonomySerilizer(self):
        organism = OrganismFactory.create()
        taxonomySerializer = TaxonomySerializer(instance = organism)
        data = taxonomySerializer.data
        self.assertEqual(set(data.keys()), set(['taxa_id', 'clade', 'genus', 'species']))

    # test pfam serializer
    def test_pfamSerilizer(self):
        pfam = PFamFactory.create()
        serializer = PFamSerializer(instance = pfam)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(['domain_id', 'domain_description']))

    # test AddProteinSerializer
    def test_addProteinSerilizer(self):
        domain1 = DomainFactory.create()
        protein = ProteinFactory.create(domain = {domain1})
        proteinSerializer = AddProteinSerializer(instance = protein)
        data = proteinSerializer.data
        self.assertEqual(set(data['domain'][0].keys()), set(['start', 'id', 'description', 'stop', 'pfam_id'])) 
        self.assertEqual(set(data.keys()), set(['id','protein_id', 'sequence', 'length', 'taxonomy', 'domain'])) 
        self.assertEqual(set(data['taxonomy'].keys()), set(['id', 'taxa_id', 'clade', 'genus', 'species']))
    
    # test pfamFromDomainSerializer
    def test_pfamFromDomainSerializer(self):
        pfam1 = PFamFactory.create()
        domain = DomainFactory.create(pfam_id = (pfam1))
        serializer = pfamFromDomainSerializer(instance = domain) 
        data = serializer.data
        self.assertEqual(set(data.keys()), set(['id','pfam_id'])) 
    
    # test proteinFromDomainSerializer
    def test_proteinFromDomainSerializer(self):
        domain = DomainFactory.create()
        serialzier = ProteinFromDomainSerializer(instance = domain)
        data = serialzier.data
        self.assertEqual(set(data.keys()), set(['id','protein_id']))  

    # test for addDomainSerializer
    def test_addDomainSerializer(self):
        pfam1 = PFamFactory.create() 
        domain = DomainFactory.create(pfam_id = (pfam1))
        serialzier = AddDomainSerializer(instance = domain)
        data = serialzier.data
        self.assertEqual(set(data.keys()), set(['id','description', 'start', 'stop','pfam_id']))  

    # test organism/taxonomy serializer
    def test_addTaxonomySerilizer(self):
        organism = OrganismFactory.create()
        serializer = AddTaxonomySerializer(instance = organism)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'taxa_id', 'clade', 'genus', 'species']))
