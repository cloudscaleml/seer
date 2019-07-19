REM python fetch.py -d data -t data -c tacos burrito -f
REM python prep.py --data_path data --output_path data --target_output data -f
python train.py --data_path data --output_path data --target_output data --epochs 5 --batch 10 --lr 0.0001