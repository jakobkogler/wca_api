from wca_api import update_tsv_export, load

update_tsv_export()
s = load('Persons', 'id name')
t = load('Results', 'competitionId eventId roundId pos best average personName personCountryId formatId value1 value2 value3 value4 value5')

print(s[:10])