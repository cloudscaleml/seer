python fetch.py -t data/fetch -c "tacos burrito" -f
python prep.py -s data/fetch -t data/prep -f
python train.py -s data/prep -t data/train --epochs 5 --batch 10 --lr 0.0001