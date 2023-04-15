# MDI-BMP

A repository hosting BMP format of [Material Design Icons](https://github.com/Templarian/MaterialDesign).
Used by [*Home Buttons*](https://github.com/nplan/HomeButtons).

## Converting SVG to BMP

`mdi2bmp.py` can be used to convert MDI source SVG files to BMP.

Usage:
```
mdi2bmp.py [-h] [--width WIDTH] [--height HEIGHT] [--tags TAGS [TAGS ...]] [--list_file LIST_FILE] [--individual INDIVIDUAL [INDIVIDUAL ...]] [--meta META] [--list_out] input output

Convert SVG files to 1-bit BMP images.

positional arguments:
  input                 Path to input folder containing source SVG files.
  output                Path to output folder for BMP images.

options:
  -h, --help                                   show this help message and exit
  --width WIDTH                                Width of output BMP images in pixels.
  --height HEIGHT                              Height of output BMP images in pixels.
  --tags TAGS [TAGS ...]                       Tags to filter MDI icons. Only icons with this tag will be converted.
  --list_file LIST_FILE                        Path to a text file containing a list of MDI icons to convert. One icon per line.
  --individual INDIVIDUAL [INDIVIDUAL ...]     Individual MDI icons to convert.
  --meta META                                  meta.json file path. Default is next to svg folder.
  --list_out                                   Save a list of converted icons as a txt file.
```

> Icons marked as *deprecated* will not be exported.
