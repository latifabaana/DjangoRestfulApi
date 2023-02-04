from django.contrib import admin
from .models import Protein, Organism, Domain, PFam, DomainProteinLink

# Register your models here.

admin.site.register(Protein)
admin.site.register(Organism)
admin.site.register(Domain)
admin.site.register(PFam)
admin.site.register(DomainProteinLink)