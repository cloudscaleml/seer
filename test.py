import os
import argparse
from datetime import datetime
from pathlib import Path

def main(input_path, output_path):
    in_path = Path(input_path).resolve()
    out_path = Path(output_path).resolve()
    print(f'Input path => {str(in_path)}')
    print('Input Files:')
    for f in os.listdir(str(in_path)):
        print(f'\t{f}')
        
    print(f'Output path => {str(out_path)}')
    print('Writing file to directory... ', end='')
    with open(str(out_path / 'test.txt'), 'w+') as f:
        f.write(f'{str(datetime.now())}\n')
    print('done')
    
    print('Output Files:')
    for f in os.listdir(str(out_path)):
        print(f'\t{f}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='test')
    parser.add_argument('-s', '--source_path', help='source directory')
    parser.add_argument('-t', '--target_path', help='target path')
    args = parser.parse_args()

    main(args.source_path, args.target_path)