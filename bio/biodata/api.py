from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.http import HttpResponse

# rename all api paths.
@api_view(['POST'])
# add protein. 
def add_protein(request):
    serializer = AddProteinSerializer(data = request.data)
    # is_valid is the validator, checks if all information that is needed is entered. 
    if serializer.is_valid():
        serializer.save()
        # if created returns 201 status 
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    # if invalid data entered, returns a 400 status.
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# get all detail about protein
def protein_detail(request, protein_id):
    try:
        # gets protein objects with the same protein_id that was entered in url.
        protein = Protein.objects.get(protein_id=protein_id)
    except Protein.DoesNotExist:
        # if protein does not exist returns a 404 error.
        return HttpResponse(status = 404)
    if request.method == 'GET':
        # serializes (formats) the data then returns the data back to the client.
        serializer = ProteinSerializer(protein)
        return Response(serializer.data)

@api_view(['GET'])
# coverage and protein_id from domain
def pFam_for_domain(request, protein_id):
    try:
        # gets all the domains that have the same protein_id as in the params
        domains= Domain.objects.filter(protein_id = protein_id)
        # if coverage is in the url 
        if 'coverage' in request.path:
            sumLength = 0
            # calculates different between stop and start for all the domains. 
            for domain in domains:
                sumLength+= (domain.stop-domain.start)
            # gets the protein that matches the protein_id in the url param
            protein = Protein.objects.get(protein_id = protein_id)
            # divides the sum of the differences by the protein length
            coverage = sumLength/protein.length
    except Domain.DoesNotExist:
        return HttpResponse(status = 404)
    if request.method == 'GET' and 'domain' in request.path:
        # formats the data to include fields depending on which serializer is called.
        serializer = DomainSerializer(domains, many= True)
        return Response(serializer.data, safe=False)
    elif request.method == 'GET' and 'coverage' in request.path:
        # returns teh dictionary below.
        return Response({'coverage': coverage})

@api_view(['GET'])
# get pfam id and description from pfam table. 
def get_pfam(request, pfam_id):
    try:
        # gets the pfam object that has the same domain_id as the one in the url
        pfam = PFam.objects.get(domain_id = pfam_id)
    except PFam.DoesNotExist:
        return HttpResponse(status = 404)
    if request.method == 'GET':
        # serializes the data
        serializer = PFamSerializer(pfam)
        # returns the data back to client
        return Response(serializer.data)

@api_view(['GET'])
# get pfam from domain model and get protein id from domain model
def protein_from_domain(request, taxa_id):
    try:
        # gets all proteins with the same taxonomoy id as the one entered in params
        proteins = Protein.objects.filter(taxonomy__taxa_id = taxa_id)
        domains = []
        # gets all the domains for this protein using the many-to-many through model.
        for protein in proteins:
            domain = Domain.objects.filter(domainproteinlink__protein = protein)
            for dom in domain:
                domains.append(dom)
    except Protein.DoesNotExist: 
        return HttpResponse(status = 400) 
    # depending on if protein or pfams is in the url, it will call a different serializer. 
    if request.method == 'GET' and'proteins' in request.path :
        serializer = ProteinFromDomainSerializer(domains, many = True)
    elif request.method == 'GET' and 'pfams' in request.path:
        serializer = pfamFromDomainSerializer(domains, many = True)
    return Response(serializer.data)



