### Scale2Pdf

A library made at LAION to scale the parsing of PDFs on CPUs. We tested our pipeline on 44-page pdf and on cheap 2 thread CPU with 12GB ram, it took us 3 mins 22 seconds to parse the pdf, save its content both structure, bulk and its images. We provide following results through our framework

1. Table extraction
2. Equation extraction
3. Image Captions
4. Page extraction
5. Keyword extraction
6. Section extraction
7. Authors extraction
8. Bibliography extraction
9. Paragraph extraction
10. Image extraction
11. Abstract extraction

At the moment, we support one pdf in a moment. Because we are still experimenting with the framework. Next, we plan to expand it with Ray and other distributed system with NUM-of-WORKERS. We plan this to be scalable and one function call library. Because we are planning to use it for 100M pdfs. 

#### Installation

```pip install scale2pdf```

then install 

```sudo apt install poppler-utils```

```Python
from scale2pdf import scalablepdf 
from scale2pdf import extractimages

pdf_path = "/content/2408.06257v3.pdf"
scalablepdf(pdf_path, extract_images=True) # folder is automatically created and results are saved
extractimages("2408.06257v3.pdf", "/path/to/output/folder")
```

#### CRAP CPU (NO GPU): 3 min 22 seconds to finish parsing and saving it to JSON. 

A Sleeping AI framework made for friends at LAION AI. 