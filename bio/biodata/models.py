from django.db import models

# Create your models here.

class Organism(models.Model):
    taxa_id = models.IntegerField(null = False, blank = False)
    clade = models.CharField(max_length = 1,  default = 'E') 
    genus = models.CharField(max_length = 100, null=False, blank = False) 
    species = models.CharField(max_length = 100, null= False, blank = False)  
    
    def int(self):
        return self.taxa_id

class Protein(models.Model):
    protein_id = models.CharField(max_length = 256, null=False, blank = False)
    sequence = models.CharField(max_length = 256, null=True, blank = False)
    length = models.IntegerField(null = True, blank = False)
    taxonomy = models.ForeignKey(Organism, on_delete=models.CASCADE, related_name = 'taxonomy')
    # change this to domains
    domain = models.ManyToManyField('Domain', through ='DomainProteinLink')
    
    def __str__(self):
        return self.protein_id

class PFam(models.Model):
    domain_id = models.CharField(max_length = 20, null=False, blank = False)
    domain_description = models.CharField(max_length = 140, null=False, blank = False)
    
    def __str__(self):
        return self.domain_id

class Domain(models.Model):
    protein_id = models.CharField(max_length = 256, null=False, blank = False)
    description = models.CharField(max_length = 140, null=False, blank = False) 
    start = models.IntegerField(null = False, blank = False)
    stop = models.IntegerField(null = False, blank = False)
    pfam_id = models.ForeignKey(PFam,on_delete = models.CASCADE, related_name='pfam_id')

    def __str__(self):
        return self.description

class DomainProteinLink(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.DO_NOTHING)
    protein = models.ForeignKey(Protein, on_delete=models.DO_NOTHING)
