# py-long-s
This Python tool accurately inserts the historical long S character (&nbsp;ſ&nbsp;) back into the given text to make it appear as if it were written before the 20th century.

English, French, German, Spanish, and Italian are supported.

#### Installation
```
pip install long-s
```
<br>

The libraries used in this project can be installed separately by using:
```
pip install numpy python-docx odfpy unidecode
```

<br>

## Online Converter
There's also a [JavaScript version](https://github.com/travisgk/long-s-converter) available that can be used online.

<br>

## Example
```
import long_s

print(long_s.convert("The discussion was surprisingly insightful.", lang="en"))
print(long_s.convert("La discussion était étonnamment perspicace.", lang="fr"))
print(long_s.convert("Die Diskussion war überraschend aufschlussreich.", lang="de"))
print(long_s.convert("La discusión fue sorprendentemente perspicaz.", lang="es"))
print(long_s.convert("La discussione è stata sorprendentemente perspicace.", lang="it"))
```

```
The diſcuſſion was ſurpriſingly inſightful.
La diſcuſſion était étonnamment perſpicace.
Die Diskuſſion war überraſchend aufſchluſsreich.
La diſcuſión fue ſorprendentemente perſpicaz.
La diſcuſſione è ſtata ſorprendentemente perſpicace.
```

<br>

## Converting Files
### .txt files
```
long_s.convert_text_file(src_path="story.txt", dst_path=None, lang="en"))
```
Since `dst_path` is None, the program will save the converted text file as `story-long-s.txt`.

<br>

### .odf files
```
long_s.convert_odf_file(src_path="story.odt", dst_path="old-story.odt", lang="en"))
```

<br>

### .docx files
```
long_s.convert_docx_file(src_path="märschen.docx", lang="de"))
```

<br>

## Special Thanks

Thank you Andrew West of the TeX Users Group for the documentation found under [The Rules for Long S](https://www.tug.org/TUGboat/tb32-1/tb100west.pdf), which was fundamental in writing the conversion functions for English, French, Spanish, and Italian. 
