#python detect.py --source dataset/test/images --weights runs/train/exp111/weights/best.pt --name TEST --nosave
# python detect.py --source /home/mzins/dev/3D-Aware-Ellipses-for-Visual-Localization/7-Scenes_Chess_dataset_test.json --weights runs/train/exp113/weights/best.pt --name TEST
# python detect.py --source /home/mzins/dev/3D-Aware-Ellipses-for-Visual-Localization/7-Scenes_Chess_dataset_test.json --weights runs/train/exp242/weights/best.pt --name TEST 
# python detect.py --source /home/mzins/dev/3D-Aware-Ellipses-for-Visual-Localization/7-Scenes_Chess_dataset_test.json --weights runs/train/exp328/weights/best.pt --name TEST 
python detect.py --source /home/mzins/dev/3D-Aware-Ellipses-for-Visual-Localization/7-Scenes_Chess_dataset_test.json --weights runs/train/magritdnn_exp12/weights/best.pt --name TEST 
# python detect.py --source /home/mzins/dev/3D-Aware-Ellipses-for-Visual-Localization/7-Scenes_Chess_dataset_test.json --weights runs/train/magritdnn_exp12/weights/last.pt --name TEST 