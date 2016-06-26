from wca_api.wca_api import update_tsv_export, load
from wca_api.table import table

update_tsv_export()
s = table(load('Persons', 'id name'))
t = table(load('Results', 'competitionId eventId roundId pos best average personName personCountryId formatId value1 value2 value3 value4 value5'))

print(s[0:5])
print(getattr(s[0], 'id'))
s.filter({'name': ['Jakob Kogler', 'Röhrer']})
print(list(s))

print()

t.filter({'personCountryId': 'Austria', 'eventId': ['444']})
print(t[:3])
t.sort('average')
t.restrict_fields(['personName', 'average', 'competitionId'])
print(t[-3:])
