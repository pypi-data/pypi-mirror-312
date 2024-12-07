import fitz
from PIL import Image

def extractimages(pdf_file_path, output_folder):
    pdf_file = fitz.open(pdf_file_path)

    for page_index in range(len(pdf_file)):
        page = pdf_file.load_page(page_index)
        image_list = page.get_images(full=True)

        if image_list:
            print(f"[+] Found a total of {len(image_list)} images on page {page_index}")
        else:
            print("[!] No images found on page", page_index)
        
        for image_index, img in enumerate(image_list, start=1):
            xref = img[0]
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_name = f"{output_folder}/image{page_index+1}_{image_index}.{image_ext}"
            with open(image_name, "wb") as image_file:
                image_file.write(image_bytes)
                print(f"[+] Image saved as {image_name}")
