import json
import os
import re
from papermage.recipes import CoreRecipe
import fitz

def sanitize_filename(filename):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', filename)

def scalablepdf(pdf_path, extract_images=True):
    def serialize_entity(entity):
        if hasattr(entity, 'text'):
            return entity.text
        return str(entity)

    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    sanitized_name = sanitize_filename(pdf_name)
    output_folder = os.path.join(os.getcwd(), sanitized_name)
    img_folder = os.path.join(output_folder, "img")
    os.makedirs(output_folder, exist_ok=True)
    if extract_images:
        os.makedirs(img_folder, exist_ok=True)

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
        'keywords': [],
        'equations': [],
        'tables': []
    }

    fields_to_extract = [
        'sections', 'authors', 'paragraphs', 'titles', 'abstracts',
        'bibliographies', 'captions', 'keywords', 'equations', 'tables'
    ]

    for field in fields_to_extract:
        if hasattr(doc, field):
            if field == 'abstracts':
                if len(getattr(doc, field)) > 0:
                    content['abstracts'] = serialize_entity(getattr(doc, field)[0])
            elif field == 'bibliographies':
                for bibliography in getattr(doc, field):
                    for sentence in bibliography.sentences:
                        content['bibliographies'].append(serialize_entity(sentence))
            elif field == 'tables':
                for table in getattr(doc, field):
                    content['tables'].append(serialize_entity(table))
            elif field == 'equations':
                for equation in getattr(doc, field):
                    content['equations'].append(serialize_entity(equation))
            else:
                for item in getattr(doc, field):
                    content[field].append(serialize_entity(item))

    structured_output_path = os.path.join(output_folder, f"{sanitized_name}.json")
    with open(structured_output_path, 'w') as json_file:
        json.dump(content, json_file, indent=4)

    page_content = {}
    markdown_content = []

    for page_num, page in enumerate(doc.pages):
        sentences = [sentence.text for sentence in page.sentences]
        page_content[f'page_{page_num + 1}'] = sentences
        markdown_content.extend(sentences)

    pages_json_path = os.path.join(output_folder, f"{sanitized_name}-pages.json")
    pages_md_path = os.path.join(output_folder, f"{sanitized_name}-pages.md")
    
    with open(pages_json_path, 'w') as json_file:
        json.dump(page_content, json_file, indent=4)

    with open(pages_md_path, 'w') as md_file:
        md_file.write('\n\n'.join(markdown_content))

    if extract_images:
        pdf_file = fitz.open(pdf_path)
        for page_index in range(len(pdf_file)):
            page = pdf_file.load_page(page_index)
            image_list = page.get_images(full=True)
            for image_index, img in enumerate(image_list, start=1):
                xref = img[0]
                base_image = pdf_file.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_name = f"{img_folder}/image{page_index+1}_{image_index}.{image_ext}"
                with open(image_name, "wb") as image_file:
                    image_file.write(image_bytes)

    print(f"All content saved to '{output_folder}'.")

# pdf_path = "/content/2408.06257v3.pdf"
# scalablepdf(pdf_path, extract_images=True)
