from wca_api.wca_api import update_tsv_export, load
from wca_api.conditions import OneOf, Equal, DNF, TimeBetterThan

update_tsv_export()
s = load('Persons', 'id name')
t = load('Results', 'competitionId eventId roundId pos best average personName personCountryId formatId value1 value2 value3 value4 value5')

print(s[0:5])
print(getattr(s[0], 'id'))
s.filter(Equal('name', 'Jakob Kogler'))
print(list(s))
print()

t.filter(Equal('personCountryId', 'Austria'))
t.filter(OneOf('eventId', ['444bf', '555bf']))
print(t)
print()

t.sort(['eventId', 'best'], reverse=True)
t.restrict_fields(['personName', 'eventId', 'best', 'competitionId'])
print(t.all_to_string())
print()

t.filter(DNF('best', False))
print(t.all_to_string())
print()

t.filter(TimeBetterThan('best', 30000))
print(t.all_to_string())

