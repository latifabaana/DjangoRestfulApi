from rest_framework import serializers
from .models import *

# all serializers to format data before it gets returned to the client.
# rename serializers
class AddTaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Organism
        fields = '__all__'
        

class PFamSerializer(serializers.ModelSerializer):
    class Meta:
        model = PFam
        exclude = ('id',)

class AddDomainSerializer(serializers.ModelSerializer):
    pfam_id = PFamSerializer(read_only = True)
    class Meta:
        model = Domain
        fields = [
            'id',
            'pfam_id', 
            'description',
            'start',
            'stop',
        ]
        depth = 1

class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Organism
        exclude = ('id',)

class DomainSerializer(serializers.ModelSerializer):
    pfam_id = PFamSerializer(read_only = True)
    class Meta:
        model = Domain
        fields = [
            'pfam_id', 
            'description',
            'start',
            'stop',
        ]
        depth = 1
        
class ProteinSerializer(serializers.ModelSerializer):
    taxonomy = serializers.CharField()
    taxonomy = TaxonomySerializer(read_only = True)
    domain = DomainSerializer(read_only = True, many = True)
    class Meta:
        model = Protein
        fields= [
            'protein_id',
            'sequence',
            'taxonomy',
            'length',
            'domain'
        ]
        depth = 2


class AddProteinSerializer(serializers.ModelSerializer):
    taxonomy = serializers.CharField()
    taxonomy = AddTaxonomySerializer(read_only = True)
    domain = AddDomainSerializer(read_only = True, many = True)
    # don't think you need to include this,because domainSerializer already includes this. 
    pfam_id = PFamSerializer(read_only = True)
    class Meta:
        model = Protein
        fields= [
            'id',
            'protein_id',
            'sequence',
            'taxonomy',
            'length',
            'domain',
            'pfam_id'

        ]
        depth = 2

    # creates a new protein 
    def create(self, validated_data):
        taxonomy_data = self.initial_data.get('taxonomy')
        domains_data = self.initial_data.get('domain')
        # sets the protein's taxonomy field to the corrsponding organism object.
        protein = Protein(**{**validated_data, 
                        'taxonomy' : Organism.objects.get(pk = taxonomy_data['id'])
        })
        protein.save()

        # adds each domain that has the same domain id to the protien foreign key domain.
        for domain_data in domains_data:
            dom_id = Domain.objects.get(pk = domain_data['id'])
            protein.domain.add(dom_id)

        protein.save()
        return protein

class ProteinFromDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields= [
            'id',
            'protein_id'
        ]

class pfamFromDomainSerializer(serializers.ModelSerializer):
    pfam_id = PFamSerializer(read_only = True)
    class Meta: 
        model = Domain
        fields = [
            'id',
            'pfam_id'
        ]

