python prep.py -s data/food -t data/parse
python train.py -s data/parse -t data/train --epochs 10 --batch 32 --lr 0.0001
python register.py -s data/train -t data/model
az ml service update --name seer-svc --inference-config inferenceconfig.json --deploy-config-file deployconfig.json