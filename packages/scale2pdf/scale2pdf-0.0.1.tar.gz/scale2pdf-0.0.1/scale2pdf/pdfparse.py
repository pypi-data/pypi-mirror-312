import json
from papermage.recipes import CoreRecipe

def scalablepdf(pdf_path, output_json):
    def serialize_entity(entity):
        if hasattr(entity, 'text'):
            return entity.text
        return str(entity)

    recipe = CoreRecipe()
    doc = recipe.run(pdf_path)

    content = {
        'sections': [],
        'authors': [],
        'paragraphs': [],
        'titles': [],
        'abstracts': None,
        'bibliographies': [],
        'captions': [],
        'keywords': []
    }

    fields_to_extract = [
        'sections', 'authors', 'paragraphs', 'titles', 'abstracts',
        'bibliographies', 'captions', 'keywords'
    ]

    for field in fields_to_extract:
        if hasattr(doc, field):
            if field == 'abstracts':
                if len(getattr(doc, field)) > 0:
                    if content['abstracts'] is None:
                        content['abstracts'] = serialize_entity(getattr(doc, field)[0])
            elif field == 'bibliographies':
                for bibliography in getattr(doc, field):
                    for sentence in bibliography.sentences:
                        content['bibliographies'].append(serialize_entity(sentence))
            else:
                for item in getattr(doc, field):
                    content[field].append(serialize_entity(item))

    with open(output_json, 'w') as json_file:
        json.dump(content, json_file, indent=4)

    print(f"Content saved to '{output_json}'.")
