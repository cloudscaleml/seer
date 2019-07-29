REM python parse.py -s data/food -t data/parse
python train.py -s data/parse -t data/train --epochs 10 --batch 32 --lr 0.0001