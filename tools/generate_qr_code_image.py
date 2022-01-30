import argparse
from PIL import Image
from rle_encode import encode

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optimize QR code for smartwatch')
    parser.add_argument('infile',
                        help='Screenshot of QR code to be encoded')
    parser.add_argument('outfile',
                        help='Destination file')

    args = parser.parse_args()

    i = Image.open(args.infile)
    scaled_image = i.resize((200,197), Image.NEAREST)
    with open(args.outfile, 'wb') as f:
        f.write(encode(scaled_image)[2])
