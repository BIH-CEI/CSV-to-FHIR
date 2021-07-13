#%%
import re
import pandas as pd
from fhir.resources.codesystem import (CodeSystem, CodeSystemProperty, CodeSystemConcept, CodeSystemConceptProperty)
from fhir.resources.contactdetail import ContactDetail
from fhir.resources.contactpoint import ContactPoint

# %%
example_codesystem = {
    "resourceType": "CodeSystem",
    "status": "active",
    "content": "complete"
}

example_property = {
    "code": "DDD",
    "type": "code"
}

example_concept_property = {
    "code": "DDD",
    "valueString": "1,1 mg O 0,5 mg Fluorid"
}

# %%
data = pd.read_csv('./ATC_2021.csv', dtype=str, encoding = 'utf-8', sep=";")
# %%
data.dropna(axis=0, how='all', inplace=True)
data.dropna(axis=1, how='all', inplace=True)
data['ATC-Code'] = data['ATC-Code'].str.strip()
data['DDD-Info'] = data['DDD-Info'].str.strip()

# %%
codesystem = CodeSystem.parse_obj(example_codesystem)
codesystem.id = 'CodeSystemATC2021'
codesystem.url = 'http://fhir.de/CodeSystem/dimdi/atc'
codesystem.version = '2021'
codesystem.name = 'ATC'
codesystem.title = 'Anatomisch-therapeutisch chemische Klassifikation (ATC) Amtliche deutsche Fassung 2021'
codesystem.status = 'active'
codesystem.experimental = True
codesystem.date = '2021-07-12'
codesystem.publisher = 'Medizininformatik Initiative'
contact = ContactDetail.construct()
telecom = ContactPoint.construct()
telecom.system = 'url'
telecom.value = 'https://www.medizininformatik-initiative.de'
contact.telecom = [telecom]
codesystem.contact = [contact]
codesystem.description = 'Anatomisch-therapeutisch-chemische-Klassifikation mit Tagesdosen Amtliche Fassung des ATC-Index mit DDD-Angaben für Deutschland im Jahre 2021'
codesystem.copyright = 'Bundesinstitut für Arzneimittel und Medizinprodukte (BfArM)'
codesystem.caseSensitive = False
codesystem.valueSet = 'http://fhir.de/ValueSet/dimdi/atc'
codesystem.hierarchyMeaning = 'is-a'
codesystem.content = 'complete'
codesystem_property = CodeSystemProperty.parse_obj(example_property) 
codesystem_property.code = 'DDD'
codesystem_property.description = 'Definierte Tagesdosis (defined daily dose, DDD)'
codesystem_property.type = 'string'
codesystem.property = [codesystem_property]

concepts_5 = []
concepts_4 = []
concepts_3 = []
concepts_2 = []
concepts_1 = []
concepts_0 = []
for index, row in data.iterrows():
    concept = CodeSystemConcept.construct()
    concept.code = row['ATC-Code']
    concept.display = row['ATC-Bedeutung']

    if pd.isnull(row['DDD-Info']) == True:
        pass
    else:
        concept_property = CodeSystemConceptProperty.parse_obj(example_concept_property)
        concept_property.code = 'DDD'
        concept_property.valueString = row['DDD-Info']
        concept.property = [concept_property]

    concepts_0.append(concept)

for concept in concepts_0:
    match_5 = re.match(r"[0-9a-zA-Z]{7}", concept.code)
    match_4 = re.match(r"[0-9a-zA-Z]{5}", concept.code)
    match_3 = re.match(r"[0-9a-zA-Z]{4}", concept.code)
    match_2 = re.match(r"[0-9a-zA-Z]{3}", concept.code)
    match_1 = re.match(r"[0-9a-zA-Z]{1}", concept.code)
    if match_5:
        concepts_5.append(concept)
    elif match_4:
        concepts_4.append(concept)
    elif match_3:
        concepts_3.append(concept)
    elif match_2:
        concepts_2.append(concept)
    elif match_1:
        concepts_1.append(concept)

for idx, concept_4 in enumerate(concepts_4):
    concept_4_children = []
    for concept_5 in concepts_5:
        if concept_4.code in concept_5.code:
            concept_4_children.append(concept_5)
        concept_4.concept = concept_4_children
        concepts_4[idx] = concept_4

for idx, concept_3 in enumerate(concepts_3):
    concept_3_children = []
    for concept_4 in concepts_4:
        if concept_3.code in concept_4.code:
            concept_3_children.append(concept_4)
        concept_3.concept = concept_3_children
        concepts_3[idx] = concept_3

for idx, concept_2 in enumerate(concepts_2):
    concept_2_children = []
    for concept_3 in concepts_3:
        if concept_2.code in concept_3.code:
            concept_2_children.append(concept_3)
        concept_2.concept = concept_2_children
        concepts_2[idx] = concept_2

for idx, concept_1 in enumerate(concepts_1):
    concept_1_children = []
    for concept_2 in concepts_2:
        if concept_1.code in concept_2.code:
            concept_1_children.append(concept_2)
        concept_1.concept = concept_1_children
        concepts_1[idx] = concept_1

codesystem.concept = concepts_1
# %%
json_file = open('CodeSystem-ATC-2021.json', 'w')
json_file.write(codesystem.json())
json_file.close()
