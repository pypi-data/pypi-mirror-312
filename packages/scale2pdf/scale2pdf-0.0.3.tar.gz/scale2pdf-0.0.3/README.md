LAION made scale possible and we made CPU scale possible. A library to scale pdf parsing on CPU. 

```Python
from scale2pdf import scalablepdf 
from scale2pdf import extractimages

scalablepdf("/content/2408.06257v3.pdf", "example-pdf.json")
extractimages("2408.06257v3.pdf", "/path/to/output/folder")
```

#### CRAP CPU (NO GPU): 3 min 42 seconds to finish parsing and saving it to JSON. 