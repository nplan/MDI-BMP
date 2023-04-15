import argparse
from PIL import Image
import cairosvg
import os
import tempfile
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert SVG files to 1-bit BMP images.')

    parser.add_argument("input", type=str,
                        help='Path to input folder containing source SVG files.')

    parser.add_argument("output", type=str,
                        help='Path to output folder for BMP images.')

    parser.add_argument('--width', type=int, default=100,
                        help='Width of output BMP images in pixels.')

    parser.add_argument('--height', type=int, default=100,
                        help='Height of output BMP images in pixels.')

    parser.add_argument('--tags', type=str, nargs='+',
                        help='Tags to filter MDI icons. Only icons with this tag will be converted.')

    parser.add_argument("--list_file", type=str,
                        help="Path to a text file containing a list of MDI icons to convert. One icon per line.")

    parser.add_argument("--individual", type=str, nargs='+',
                        help="Individual MDI icons to convert.")

    parser.add_argument('--meta', type=str,
                        help='meta.json file path. Default is next to svg folder.')

    parser.add_argument('--list_out', action='store_true',
                        help='Save a list of converted icons as a txt file.')

    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    print("Selected tags: {}".format(args.tags))
    print("Individual: {}".format(args.individual))

    # locate meta.json file
    if not args.meta:
        meta_path = os.path.join(os.path.split(args.input)[0], 'meta.json')
    else:
        meta_path = args.meta

    icons_in = []
    # load list of icons from file
    if args.list_file:
        with open(args.list_file) as f:
            for line in f:
                icons_in.append(line.strip())
        print("Converting {} icons from list file...".format(len(icons_in)))
    if args.individual:
        icons_in.extend(args.individual)
        print("Converting {} individual icons...".format(len(args.individual)))

    icons_out = []
    # create list of icons to convert
    with open(meta_path) as f:
        meta = json.load(f)

        if not args.tags and not args.individual and not args.list_file:
            print("No icon selection. Converting all icons...")
            for icon in meta:
                if not icon['deprecated']:
                    icons_out.append(icon['name'])
                else:
                    print("Skipping deprecated icon {}".format(icon['name']))

        else:
            # check if all list file icons exist in meta.json
            for ic in icons_in:
                exist = False
                for icon in meta:
                    if ic == icon['name']:
                        exist = True
                        break
                else:
                    exist = False
                    print("Icon {} does not exist.".format(ic))

            for icon in meta:
                if icons_in:
                    for ic in icons_in:
                        if ic == icon['name']:
                            if not icon['deprecated']:
                                icons_out.append(icon['name'])
                            else:
                                print("Skipping deprecated icon {}".format(
                                    icon['name']))

                if args.tags:
                    for tag in args.tags:
                        if tag in icon['tags']:
                            if not icon['deprecated']:
                                icons_out.append(icon['name'])
                            else:
                                print("Skipping deprecated icon {}".format(
                                    icon['name']))

    print("Converting {} icons...".format(len(icons_out)))

    longest = ""
    # iterate over icon list
    for icon in icons_out:
        input_file_path = os.path.join(args.input, icon + '.svg')

        # check if file exists
        if not os.path.exists(input_file_path):
            print("File {} does not exist.".format(input_file_path))
            continue

        if len(icon) > len(longest):
            longest = icon

        output_file_path = os.path.join(
            args.output, os.path.splitext(os.path.split(input_file_path)[-1])[0] + '.bmp')

        temp_file = tempfile.TemporaryFile()

        # convert SVG to PNG
        cairosvg.svg2png(url=input_file_path, write_to=temp_file,
                         output_width=args.width, output_height=args.height,
                         background_color="white")

        # convert to 1-bit BMP
        img = Image.open(temp_file)
        img = img.convert('1', dither=Image.Dither.NONE)
        img.save(output_file_path)

    print("Longest icon name: {} length: {}".format(longest, len(longest)))
 
    if args.list_out:
        path = args.output + ".txt"
        print(path)
        with open(path, 'w') as f:
            for icon in icons_out:
                f.write(icon + "\r\n")
