#python detect.py --source dataset/test/images --weights runs/train/exp111/weights/best.pt --name TEST --nosave
# python detect.py --source /home/mzins/dev/3D-Aware-Ellipses-for-Visual-Localization/7-Scenes_Chess_dataset_test.json --weights runs/train/exp113/weights/best.pt --name TEST
# python detect.py --source /home/mzins/dev/3D-Aware-Ellipses-for-Visual-Localization/7-Scenes_Chess_dataset_test.json --weights runs/train/exp242/weights/best.pt --name TEST 
# python detect.py --source /home/mzins/dev/3D-Aware-Ellipses-for-Visual-Localization/7-Scenes_Chess_dataset_test.json --weights runs/train/exp350/weights/best.pt --name TEST 

# python detect.py --source /home/mzins/dev/3D-Aware-Ellipses-for-Visual-Localization/7-Scenes_Chess_dataset_test.json --weights runs/train/exp532/weights/best.pt --name TEST 

# python detect.py --source /home/mzins/dev/3D-Aware-Ellipses-for-Visual-Localization/7-Scenes_Chess_dataset_test.json --weights runs/train/exp533/weights/best.pt --name TEST 
# python detect.py --source /home/mzins/dev/3D-Aware-Ellipses-for-Visual-Localization/7-Scenes_Chess_dataset_test.json --weights runs/train/exp534/weights/best.pt --name TEST 
# python detect.py --source /home/mzins/dev/3D-Aware-Ellipses-for-Visual-Localization/7-Scenes_Chess_dataset_test.json --weights runs/train/exp535/weights/best.pt --name TEST 


# python detect.py --source /home/mzins/dev/3D-Aware-Ellipses-for-Visual-Localization/7-Scenes_Chess_dataset_test.json --weights runs/train/exp43/weights/best.pt --name TEST 
# python detect.py --source freiburg2_desk.json --weights yolov5m.pt --name TEST  --output LOSC.json


# python detect.py --source freiburg2_desk.json --weights runs/train/exp46/weights/best.pt --name TEST  --output out_detections_yolov5_fr2_desk.json    # fr2_desk


# MuseeNancy train because seq 03-04 (test) were annotated (inverse train and test)
# python detect.py --source /media/mzins/DATA1/MuseeNancy/all_seq/MuseeNancy_dataset_train.json --weights runs/train/exp48/weights/best.pt --name TEST  --output out_detections_yolov5_MuseeNancy.json   # MuseeNancy


# MuseeNancy train because seq 03-04 (test) were annotated (inverse train and test)
# all heads are the same category
# python detect.py --source /media/mzins/DATA1/MuseeNancy/all_seq/MuseeNancy_dataset_train.json --weights runs/train/exp49/weights/best.pt --name TEST  --output out_detections_yolov5_MuseeNancy_2.json   # MuseeNancy
# all seq 
# python detect.py --source /media/mzins/DATA1/MuseeNancy/all_seq/MuseeNancy_dataset_all_seq.json --weights runs/train/exp49/weights/best.pt --name TEST  --output out_detections_yolov5_MuseeNancy_all_seq.json   # MuseeNancy





# train on 01 02 and test on 04
# python detect.py --source /media/mzins/DATA1/MuseeNancy/all_seq/MuseeNancy_dataset_seq_04.json --weights runs/train/exp50/weights/best.pt --name TEST  --output out_detections_yolov5_MuseeNancy_seq_04.json   # MuseeNancy

# test on 01 with train on 04
# python detect.py --source /media/mzins/DATA1/MuseeNancy/all_seq/MuseeNancy_dataset_seq_01.json --weights runs/train/exp49/weights/best.pt --name TEST  --output out_detections_yolov5_MuseeNancy_seq_01.json   # MuseeNancy




# RedWood: Chair
# python detect.py --source dataset_Redwood_chair_all.json --weights yolov5m.pt --name Chair 
# python detect.py --source dataset_Redwood_chair_all.json --weights runs/train/exp52/weights/last.pt --name Chair ## 500 epochs
# python detect.py --source dataset_Redwood_chair_all.json --weights runs/train/exp53/weights/last.pt --name Chair ## 2000 epochs



# Run pretrained yolov5 (no fine-tuning) on Freiburg2 desk
# python detect.py --source freiburg2_desk.json --weights yolov5m.pt --name fr2_desk  --output out_detections_yolov5_fr2_desk_pretrained.json    # fr2_desk



# python detect.py --source dataset_freiburg3_long_office_household.json --weights yolov5m.pt --name fr3_long_office  --output out_detections_yolov5_fr3_long_office_pretrained.json    # fr2_desk

# python detect.py --source dataset_freiburg1_desk.json --weights yolov5m.pt --name fr1_desk  --output out_detections_yolov5_fr1_desk_pretrained.json
# python detect.py --source dataset_freiburg1_desk2.json --weights yolov5m.pt --name fr1_desk2  --output out_detections_yolov5_fr1_desk2_pretrained.json


# python detect.py --source dataset_freiburg1_room.json --weights yolov5m.pt --name fr1_room  --output out_detections_yolov5_fr1_room_pretrained.json
# python detect.py --source dataset_freiburg2_dishes.json --weights yolov5m.pt --name fr2_dishes  --output out_detections_yolov5_fr2_dishes_pretrained.json

# python detect.py --source dataset_redkitchen_01.json --weights yolov5m.pt --name redkitchen_01  --output out_detections_yolov5_redkitchen_01_pretrained.json

# python detect.py --source dataset_redkitchen_02.json --weights yolov5m.pt --name redkitchen_02  --output out_detections_yolov5_redkitchen_02_pretrained.json
# python detect.py --source dataset_redkitchen_04.json --weights yolov5m.pt --name redkitchen_04  --output out_detections_yolov5_redkitchen_04_pretrained.json

# python detect.py --source dataset_office_01.json --weights yolov5m.pt --name office_01  --output out_detections_yolov5_office_01_pretrained.json
# python detect.py --source dataset_office_02.json --weights yolov5m.pt --name office_02  --output out_detections_yolov5_office_02_pretrained.json
# python detect.py --source dataset_office_06.json --weights yolov5m.pt --name office_06  --output out_detections_yolov5_office_06_pretrained.json
# python detect.py --source dataset_office_09.json --weights yolov5m.pt --name office_09  --output out_detections_yolov5_office_09_pretrained.json

# python detect.py --source dataset_kitti_00.json --weights yolov5m.pt --name kitti_00  --output out_detections_yolov5_kitti_00_pretrained.json

# python detect.py --source dataset_bottles_1.json --weights yolov5m.pt --name bottles_1  --output out_detections_yolov5_bottles_1_pretrained.json
# python detect.py --source dataset_bottles_2.json --weights yolov5m.pt --name bottles_2  --output out_detections_yolov5_bottles_2_pretrained.json
# python detect.py --source dataset_bottles_3.json --weights yolov5m.pt --name bottles_3  --output out_detections_yolov5_bottles_3_pretrained.json

# python detect.py --source dataset_apple_mouse_keyboard.json --weights yolov5m.pt --name apple_mouse_keyboard  --output out_detections_yolov5_apple_mouse_keyboard_pretrained.json

# python detect.py --source dataset_bulle_1.json --weights yolov5m.pt --name bulle_1  --output out_detections_yolov5_bulle_1_pretrained.json
# python detect.py --source dataset_bulle_2.json --weights yolov5m.pt --name bulle_2  --output out_detections_yolov5_bulle_2_pretrained.json
# python detect.py --source dataset_bulle_3.json --weights yolov5m.pt --name bulle_3  --output out_detections_yolov5_bulle_3_pretrained.json
# python detect.py --source dataset_bulle_4.json --weights yolov5m.pt --name bulle_4  --output out_detections_yolov5_bulle_4_pretrained.json
# python detect.py --source dataset_bulle_5.json --weights yolov5m.pt --name bulle_5  --output out_detections_yolov5_bulle_5_pretrained.json



# python detect.py --source dataset_statues_train.json --weights runs/train/exp54/weights/last.pt --name statues_train  --output out_detections_yolov5_statues.json

# python detect.py --source dataset_statues_test_1.json --weights runs/train/exp54/weights/last.pt --name statues_test_1  --output out_detections_yolov5_statues_test_1.json
# python detect.py --source dataset_statues_test_2.json --weights runs/train/exp54/weights/last.pt --name statues_test_2  --output out_detections_yolov5_statues_test_2.json
# python detect.py --source dataset_statues_test_3.json --weights runs/train/exp54/weights/last.pt --name statues_test_3  --output out_detections_yolov5_statues_test_3.json
# python detect.py --source dataset_statues_test_4.json --weights runs/train/exp54/weights/last.pt --name statues_test_4  --output out_detections_yolov5_statues_test_4.json
# python detect.py --source dataset_statues_test_5.json --weights runs/train/exp54/weights/last.pt --name statues_test_5  --output out_detections_yolov5_statues_test_5.json
# python detect.py --source dataset_statues_test_6.json --weights runs/train/exp54/weights/last.pt --name statues_test_6  --output out_detections_yolov5_statues_test_6.json



# python detect.py --source dataset_statues_test_7.json --weights runs/train/exp54/weights/last.pt --name statues_test_7  --output out_detections_yolov5_statues_test_7.json
# python detect.py --source dataset_statues_test_8.json --weights runs/train/exp54/weights/last.pt --name statues_test_8  --output out_detections_yolov5_statues_test_8.json
# python detect.py --source dataset_statues_test_9.json --weights runs/train/exp54/weights/last.pt --name statues_test_9  --output out_detections_yolov5_statues_test_9.json
# python detect.py --source dataset_statues_test_10.json --weights runs/train/exp54/weights/last.pt --name statues_test_10  --output out_detections_yolov5_statues_test_10.json
# python detect.py --source dataset_statues_test_11.json --weights runs/train/exp54/weights/last.pt --name statues_test_11  --output out_detections_yolov5_statues_test_11.json
# python detect.py --source dataset_statues_test_12.json --weights runs/train/exp54/weights/last.pt --name statues_test_12  --output out_detections_yolov5_statues_test_12.json
# python detect.py --source dataset_statues_test_13.json --weights runs/train/exp54/weights/last.pt --name statues_test_13  --output out_detections_yolov5_statues_test_13.json
# python detect.py --source dataset_statues_test_14.json --weights runs/train/exp54/weights/last.pt --name statues_test_14  --output out_detections_yolov5_statues_test_14.json
# python detect.py --source dataset_statues_test_15.json --weights runs/train/exp54/weights/last.pt --name statues_test_15  --output out_detections_yolov5_statues_test_15.json


# network statues and objects
# for i in $(seq 1 1 17)
# do
#     python detect.py --source dataset_statues_objects_test_$i.json --weights runs/train/exp56/weights/last.pt --name statues_objects_test_$i  --output out_detections_yolov5_statues_objects_test_$i.json --nosave
# done


# python detect.py --source dataset_kitchen_1.json --weights yolov5m.pt --name kitchen_1  --output out_detections_yolov5_kitchen_1.json --nosave
# python detect.py --source dataset_kitchen_2.json --weights yolov5m.pt --name kitchen_2  --output out_detections_yolov5_kitchen_2.json --nosave
# python detect.py --source dataset_kitchen_3.json --weights yolov5m.pt --name kitchen_3  --output out_detections_yolov5_kitchen_3.json --nosave
# for i in 4 5
# do
#     python detect.py --source dataset_kitchen_$i.json --weights yolov5m.pt --name kitchen_$i  --output out_detections_yolov5_kitchen_$i.json --nosave
# done

# for i in 1
# do
#     python detect.py --source dataset_musee_meuble_$i.json --weights checkpoint_statues_objects/last.pt --name musee_meuble_$i  --output out_detections_yolov5_musee_meuble_$i.json --nosave
# done

for i in 6 7  #1 2 3 4 #17 18  #13 14 #7 8 9 10 11 12 # 1 2 3 4 5 6  #13 14  #8 9 10 #5 6 7 # 1 2 3 4 #5 6 7 8 9 10 #1 2 3 4 #13 14 15  #9 #8 10 11  #6 7 #4 5 #1 2 3
do
    # python detect.py --source dataset_desk_$i.json --weights yolov5m.pt --name desk_$i  --output out_detections_yolov5_desk_$i.json --nosave
    # python detect.py --source dataset_sink_$i.json --weights yolov5m.pt --name sink_$i  --output out_detections_yolov5_sink_$i.json --nosave
    # python detect.py --source dataset_test_detect_objects_$i.json --weights yolov5m.pt --name test_detect_objects_$i  --output out_detections_yolov5_test_detect_objects_$i.json #--nosave
    # python detect.py --source dataset_table_$i.json --weights yolov5m.pt --name table_$i  --output out_detections_yolov5_table_$i.json --nosave
    # python detect.py --source dataset_bureau_$i.json --weights yolov5m.pt --name bureau_$i  --output out_detections_yolov5_bureau_$i.json --nosave
    # python detect.py --source dataset_meuble_$i.json --weights checkpoint_statues_objects/last.pt --name meuble_$i  --output out_detections_yolov5_meuble_$i.json --nosave
    python detect.py --source dataset_big_statue_$i.json --weights checkpoint_statues_objects_big_statue/last.pt --name big_statue_$i  --output out_detections_yolov5_big_statue_$i.json  --nosave
done

