from django.urls import path, include
from rest_framework.schemas import get_schema_view
from . import views
from . import api



urlpatterns = [
    # home page
    path('', views.index, name = 'index'),
    # add protein
    path('api/protein/', api.add_protein, name = 'addProtein'),
    # gets all data from protein table
    path('api/protein/<str:protein_id>', api.protein_detail, name = 'allProtein'),
    # gets pfams from domain model
    path('api/pfams/<int:taxa_id>', api.protein_from_domain, name = 'getPFams'),
    # gets coverage of protein
    path('api/coverage/<str:protein_id>', api.pFam_for_domain, name = 'coverage'),
    # gets protein_id from the domain model
    path('api/proteins/<int:taxa_id>', api.protein_from_domain, name = 'proteinFromDomain'),
    # gets only pfam from pfam model 
    path('api/pfam/<str:pfam_id>', api.get_pfam, name = 'getDomainDescription'),

]


