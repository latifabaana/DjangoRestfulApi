import json
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponse
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *

# to test these must run ./manage.py test.

class ProteinTest(APITestCase):
    # pre defines the objects so they can be used throughout the class.
    pfam = None
    organism = None
    protein = None
    domain = None
    proteinLink = None
    
    # sets up the declated variables above
    def setUp(self):
        self.pfam = PFamFactory.create()
        self.organism = OrganismFactory.create()
        self.protein = ProteinFactory.create(taxonomy = self.organism)
        self.domain = DomainFactory.create(pfam_id =self.pfam)
        self.proteinLink = DomainProteinLinkFactory(domain = self.domain, protein = self.protein) 

    # delete all objects in database so it does not conflict with foreign keys when testing.
    def tearDown(self):
        Protein.objects.all().delete()
        Organism.objects.all().delete()
        Domain.objects.all().delete()
        PFam.objects.all().delete()
        DomainProteinLink.objects.all().delete()

    # testing success allProtein api call
    def test_allProteinDetailReturnSuccess(self):
        url = reverse('allProtein', kwargs = {'protein_id': 'A0A016S8J7'})
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        # testing protein fields
        self.assertEqual(data['sequence'], 'MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA')
        self.assertEqual(data['length'], 101)
        # testing organism/taxonomy fields
        self.assertEqual(data['taxonomy']['taxa_id'], 53326)
        self.assertEqual(data['taxonomy']['genus'], 'Ancylostoma')
        self.assertEqual(data['taxonomy']['species'], 'ceylanicum')
        # testing domain and pfam fields
        self.assertEqual(data['domain'][0]['start'], 40 )
        self.assertEqual(data['domain'][0]['description'], 'Peptidase C13 legumain')
        self.assertEqual(data['domain'][0]['stop'], 94)
        self.assertEqual(data['domain'][0]['pfam_id']['domain_id'], 'PF01650')
        self.assertEqual(data['domain'][0]['pfam_id']['domain_description'], 'PeptidaseC13family')
        
    # testing if bad input for allProtein api
    def test_allProteinDetailReturnFail(self):
        url = '/api/protein/8/'
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, 404)

    # testing getPFams api call
    def test_getPfams(self):
        url = reverse('getPFams', kwargs = {'taxa_id': 53326})
        response = self.client.get(url)
        response.render()
        # tests if it renders okay
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        # testing pfam_id fields
        self.assertEqual(data[0]['id'], 1)
        self.assertEqual(data[0]['pfam_id']['domain_id'], 'PF01650')
        self.assertEqual(data[0]['pfam_id']['domain_description'], 'PeptidaseC13family')

    # check if url returns bad input with string 
    def test_getPfamsReturnFail(self):
        url = '/api/pfams/ht'
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, 404)

    # tests getDomainDescription api call
    def test_getPFam(self):
        url = reverse('getDomainDescription', kwargs = {'pfam_id': 'PF01650'})
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        # checks fields. 
        self.assertEqual(data['domain_id'], 'PF01650')
        self.assertEqual(data['domain_description'], 'PeptidaseC13family')

    # check if objects can be found with this url
    def test_getPfamReturnFail(self):
        url = '/api/pfam/hey'
        response = self.client.get(url, format = 'json')
        # returns 404 because PFAM with pfam_id = 36 does not exist
        self.assertEqual(response.status_code, 404)

    # tests proteinFromDomain api call
    def test_proteinFromDomain(self):
        url = reverse('proteinFromDomain', kwargs = {'taxa_id': 53326})
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data[0]['id'], 1)
        self.assertEqual(data[0]['protein_id'], 'A0A016S8J7')

    # check if url returns bad input with string 
    def test_getProteinFromDomain(self):
        url = '/api/pfams/ht'
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, 404)

    # tests coverage api call
    def test_coverage(self):
        url = reverse('coverage', kwargs = {'protein_id': 'A0A016S8J7'})
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        # checks the returned value with what it is supposed to be.
        self.assertEqual(data['coverage'], 0.5346534653465347)


    



            