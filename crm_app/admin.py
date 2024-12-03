from django.contrib import admin
from .models import Client, Contact, Opportunity, Interaction

# Enregistrement avec personnalisation
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'email','address','phone')
    search_fields = ('name', 'industry')
    list_filter = ('industry',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'position', 'client')
    search_fields = ('first_name', 'last_name', 'email', 'client__name')


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'estimated_value', 'client')
    list_filter = ('status',)
    search_fields = ('title', 'client__name')

    # Action personnalisée
    @admin.action(description="Marquer comme gagnées")
    def mark_as_won(self, request, queryset):
        queryset.update(status='won')

    actions = [mark_as_won]


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('date', 'summary', 'opportunity')
    list_filter = ('opportunity',)
    search_fields = ('opportunity__title',)
