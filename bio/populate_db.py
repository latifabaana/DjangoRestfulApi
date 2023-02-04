import os
import sys
import django
import csv
from collections import defaultdict

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bio.settings')
django.setup()

from biodata.models import *

#################    CREATING FILE PATHS   ############################

# go back one direction from current working directory so the variable holds the midterm-proj directory
midterm_directory = os.path.normpath(os.getcwd() + os.sep + os.pardir)

# stores the file basenames in an array.
file_names = ['organisms.csv', 'domainFamily.csv', 'domain.csv', 'proteins.csv']
# joins the midterm directory with each file base name to get a full path, then stores it in file_paths array
file_paths = []
for file_name in file_names:
    file_path = os.path.join(midterm_directory, file_name)
    file_paths.append(file_path)

# sets to store all data read by csv_reader.
organisms = set()
pfams = set()
domains = set()
proteins = set()

#################    READING FILES AND STORING DATA INTO SETS   ############################

# function that reads all the files and adds relevant columns depending on the model structure to the sets declared above. 
def read_file(file):
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter =',')
        header = csv_reader.__next__()
        for row in csv_reader:
            if os.path.basename(file) == 'organisms.csv':
                organisms.add((row[0], row[1], row[2], row[3], row[4], row[5]))
            elif os.path.basename(file) == 'domainFamily.csv':
                pfams.add((row[1], row[2]))
            elif os.path.basename(file) == 'domain.csv':
                domains.add((row[0], row[1], row[2], row[3], row[4]))
            elif os.path.basename(file) == 'proteins.csv':
                proteins.add((row[1], row[2], row[3]))

# calls the above function for all the file_paths csv's
for file in file_paths:
    read_file(file)

#################    ORGANISMS   ############################

# deletes any Organism objects already in the database. 
Organism.objects.all().delete()
# used to store the rows, so proteins can later identify and store it in it's foreign key.
org = {}
# empty list to store bulk creation
bulk_organisms = list()
# creates an organism for every row in the organism set.
for organism in organisms:
    row = Organism(taxa_id=organism[1],
                    clade=organism[2],
                    genus = organism[4], 
                    species = organism[5])
    bulk_organisms.append(row) 
    # stores the row depending on the protein_id
    org[organism[0]] = row
# bulk creates the organisms stored in bulk_organisms
new_organisms= Organism.objects.bulk_create(bulk_organisms)

#################    PFAMS   ############################

# deletes any Organism objects already in the database. 
PFam.objects.all().delete()
# empty list to store bulk creation
bulk_pfam = list()
# creates a pfam for every row in the pfam set.
for pfam in pfams:
    bulk_pfam.append(PFam(
                        domain_id = pfam[0],
                        domain_description=pfam[1],
                        ))
# bulk creates the pfams stored in bulk_pfams
new_pfams= PFam.objects.bulk_create(bulk_pfam)

#################    DOMAINS    ############################

# deletes any Organism objects already in the database. 
Domain.objects.all().delete()
# empty list to store bulk creation
bulk_domain = list()
# creates a domain for every row in the domain set.
for domain in domains:
    pfam_obj = PFam.objects.get(domain_id = domain[1]) 
    bulk_domain.append(Domain(
                            protein_id = domain[0],
                            description= domain[2],
                            start =  domain[3],
                            stop =  domain[4],
                            pfam_id = pfam_obj,
                            ))
# bulk creates the domains stored in bulk_domains
new_domains = Domain.objects.bulk_create(bulk_domain)

#################    PROTEINS   ############################

# deletes any Protein objects already in the databases, as well as objectes in the through table. 
Protein.objects.all().delete()
DomainProteinLink.objects.all().delete()
# empty lists to store bulk creation
bulk_protein = list()
bulk_links = list()
# creates a protein for every row in the protein set.
for protein in proteins:
    domain_objs = Domain.objects.filter(protein_id = protein[0]) 
    row = Protein(
                # gets the organism depending on the protein of the row and stores it in taxonomy
                taxonomy = org[protein[0]],
                protein_id=protein[0],
                sequence=protein[1],
                length = protein[2])
    bulk_protein.append(row)
    # adds corresponding domain and protein in the many-to-many through table.
    for domain_obj in domain_objs:
        link = DomainProteinLink(domain=domain_obj, protein = row)
        bulk_links.append(link)
# bulk creates the proteins stored in bulk_proteins as well as bulk creates the through table. 
new_proteins = Protein.objects.bulk_create(bulk_protein)
new_protein_domain_links = DomainProteinLink.objects.bulk_create(bulk_links)
