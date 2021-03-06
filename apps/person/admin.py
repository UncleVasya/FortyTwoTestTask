from django.contrib import admin
from apps.person.models import Person


class PersonAdmin(admin.ModelAdmin):
    model = Person

    @staticmethod
    def full_name(person):
        return "%s %s" % (person.name, person.surname)

    fieldsets = [
        ('Core data', {'fields': [['name', 'surname', 'birth'], 'bio']}),
        ('Contacts', {'fields': [['email', 'skype', 'jabber'], 'contacts']}),
    ]

    list_display = ('full_name', 'birth', 'email')


admin.site.register(Person, PersonAdmin)
