import json
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponse
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
import csv 
from itertools import islice
import os
import sys


# change these to ..if it's in a folder.
from .model_factories import *
from .serializers import *

class databaseTest(TestCase):

    midterm_directory = ''
    pfam_instance = None

    organisms = set()
    pfams = set()
    domains = set()
    proteins = set()

    #################################    SET UP    #####################################

    # set up some variables: in this case, set up pfam_instance
    def setUp(self):
        # go back one direction from current working directory so the variable holds the midterm-proj directory
        self.midterm_directory = os.path.normpath(os.getcwd() + os.sep + os.pardir)

        # creates path names for csv files in file_names and adds them to array file_paths. 
        file_names = ['organisms.csv','domain.csv', 'proteins.csv']
        file_paths = []
        for file_name in file_names:
            file_path = os.path.join(self.midterm_directory, file_name)
            file_paths.append(file_path)

        # fills the organism, protein and domain sets with first row data.
        for file in file_paths:
            with open(file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter =',')
                header = csv_reader.__next__()
                row = next(csv_reader)
                if os.path.basename(file) == 'organisms.csv':
                    self.organisms.add((row[0], row[1], row[2], row[3], row[4], row[5]))
                elif os.path.basename(file) == 'domain.csv':
                    self.domains.add((row[0], row[1], row[2], row[3], row[4]))
                elif os.path.basename(file) == 'proteins.csv':
                    self.proteins.add((row[1], row[2], row[3]))

        # fill pfam set wiht the row that matches with the domain
        pfam_file =  os.path.join(self.midterm_directory, 'domainFamily.csv') 
        with open(pfam_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter =',')
            # must get the pfam that matches with the domain, since we're only testing one row
            for i in range(1008): csv_reader.__next__()
            # returns the 1008 row of data. 
            row1 = next(csv_reader)
        # adds column 1 and 2 of row1 to the set. 
        self.pfams.add((row1[1], row1[2]))

        # for each set in pfams, it returns a saved pfam instance. 
        for pfam in self.pfams:
            self.pfam_instance = PFamFactory.create(domain_id = pfam[0],
                                    domain_description = pfam[1])

    # delete all objects in database so it does not conflict with foreign keys when testing.
    def tearDown(self):
        PFam.objects.all().delete()
        Protein.objects.all().delete()
        Organism.objects.all().delete()
        Domain.objects.all().delete() 
        DomainProteinLink.objects.all().delete()

    #################################    PFAM TEST    #####################################

    def test_pfamData(self):
            # checks if the fields in the pfam instance is the same as the first row fields in the actual pfam file. 
            self.assertEqual(self.pfam_instance.domain_id, 'PF02800')
            self.assertEqual(self.pfam_instance.domain_description, 'Glyceraldehyde3-phosphatedehydrogenase: C-terminaldomain')
    
    #################################    ORGANISM TEST    #####################################
    org = {}
    def test_organismData(self):
        # for each set in organism, it returns a saved organism instance 
        for organism in self.organisms:
            organism_instance = OrganismFactory.create(
                                    # protein_id = organism[0],
                                    taxa_id=organism[1],
                                    clade=organism[2],
                                    genus = organism[4], 
                                    species = organism[5])
            # checks if the fields in the organism instance is the same as the first row fields in the actual organism file. 
            self.assertEqual(organism_instance.taxa_id, '568076')
            self.assertEqual(organism_instance.clade, 'E')
            self.assertEqual(organism_instance.genus, 'Metarhizium')
            self.assertEqual(organism_instance.species, 'robertsii')
            
            self.org[organism[0]] = organism_instance

    #################################    DOMAIN TEST    #####################################
    def test_domainData(self):
        for domain in self.domains:
            domain_instance = DomainFactory.create(
                                                    protein_id = domain[0],
                                                    description= domain[2],
                                                    start =  domain[3],
                                                    stop =  domain[4],
                                                    pfam_id = self.pfam_instance
                                                    )
           # checks if the fields in the domain instance is the same as the first row fields in the actual domain file.  
            self.assertEqual(domain_instance.protein_id, 'A0A014PQC0')
            self.assertEqual(domain_instance.description, 'Glyceraldehyde 3-phosphate dehydrogenase catalytic domain')
            self.assertEqual(domain_instance.start, '157')
            self.assertEqual(domain_instance.stop, '314')
            self.assertEqual(domain_instance.pfam_id.domain_id, 'PF02800')
            self.assertEqual(domain_instance.pfam_id.domain_description, 'Glyceraldehyde3-phosphatedehydrogenase: C-terminaldomain')

    #################################    PROTEIN TEST    #####################################
    def test_proteinData(self):
        for protein in self.proteins:
            dom_objs = DomainFactory(protein_id = protein[0])
            protein_instance = ProteinFactory.create(
                                        taxonomy = self.org[protein[0]],
                                        protein_id=protein[0],
                                        sequence=protein[1],
                                        length = protein[2])
           # checks if the fields in the protein instance is the same as the first row fields in the actual protein file.  
            self.assertEqual(protein_instance.protein_id, 'A0A014PQC0')
            self.assertEqual(protein_instance.taxonomy.taxa_id, '568076')
            self.assertEqual(protein_instance.taxonomy.genus, 'Metarhizium')

            # many to many through field. 
            link = DomainProteinLinkFactory(domain=dom_objs, protein = protein_instance)
            # checks if the link contains the right linked data, by making sure the protein_id's are the same for both.
            self.assertEqual(link.domain.protein_id, 'A0A014PQC0' )
            self.assertEqual(link.protein.protein_id, 'A0A014PQC0' )
            