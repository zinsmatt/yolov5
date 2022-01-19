# python train.py --batch 8 --epochs 10 --data dataset_instance.yaml --weights yolov5m.pt --cfg yolov5m.yaml --hyp data/hyps/hyp.finetune.yaml #--resume
python train.py --batch 8 --epochs 200 --data dataset.yaml --weights yolov5m.pt --cfg yolov5m.yaml --hyp data/hyps/hyp.finetune.yaml # --cache False #--resume

# python train.py --batch 8 --epochs 200 --data dataset_instance.yaml --weights yolov5m.pt --cfg yolov5m.yaml --hyp data/hyps/hyp.finetune.yaml #--resume

# python train.py --batch 8 --epochs 10 --data dataset_instance.yaml --weights yolov5x.pt --cfg yolov5x.yaml --hyp data/hyps/hyp.finetune.yaml #--resume

# python train.py --batch 4 --epochs 50 --data dataset_instance.yaml --weights yolov5x.pt --cfg yolov5x.yaml --hyp data/hyps/hyp.finetune.yaml #--resume

