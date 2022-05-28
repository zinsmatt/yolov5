import json
import os
import glob





input_path = "/media/mzins/DATA1/Redwood/chair/09647/rgb"
output_file = "dataset_redwood_chair_all.json"

input_path = "/media/mzins/DATA1/TUM_RGB-D/rgbd_dataset_freiburg3_long_office_household/rgb"
output_file = "dataset_freiburg3_long_office_household.json"

input_path = "/media/mzins/DATA1/TUM_RGB-D/rgbd_dataset_freiburg1_desk/rgb"
output_file = "dataset_freiburg1_desk.json"

input_path = "/media/mzins/DATA1/TUM_RGB-D/rgbd_dataset_freiburg1_desk2/rgb"
output_file = "dataset_freiburg1_desk2.json"

input_path = "/media/mzins/DATA1/TUM_RGB-D/rgbd_dataset_freiburg1_room/rgb"
output_file = "dataset_freiburg1_room.json"

input_path = "/media/mzins/DATA1/TUM_RGB-D/rgbd_dataset_freiburg2_dishes/rgb"
output_file = "dataset_freiburg2_dishes.json"

input_path = "/media/mzins/DATA1/7-Scenes/redkitchen/seq-01"
output_file = "dataset_redkitchen_01.json"

input_path = "/media/mzins/DATA1/7-Scenes/redkitchen/seq-02"
output_file = "dataset_redkitchen_02.json"

input_path = "/media/mzins/DATA1/7-Scenes/redkitchen/seq-04"
output_file = "dataset_redkitchen_04.json"

input_path = "/media/mzins/DATA1/7-Scenes/office/seq-01"
output_file = "dataset_office_01.json"
input_path = "/media/mzins/DATA1/7-Scenes/office/seq-02"
output_file = "dataset_office_02.json"
input_path = "/media/mzins/DATA1/7-Scenes/office/seq-06"
output_file = "dataset_office_06.json"

input_path = "/media/mzins/DATA1/7-Scenes/office/seq-09"
output_file = "dataset_office_09.json"

input_path = "/media/mzins/DATA1/Kitti/data_odometry_gray/dataset/sequences/00/image_0"
output_file = "dataset_kitti_00.json"

input_path = "/media/mzins/DATA1/VideoAppart/bottles_1/frames"
output_file = "dataset_bottles_1.json"

input_path = "/media/mzins/DATA1/VideoAppart/bottles_2/frames"
output_file = "dataset_bottles_2.json"

input_path = "/media/mzins/DATA1/VideoAppart/bottles_3/frames"
output_file = "dataset_bottles_3.json"

input_path = "/media/mzins/DATA1/VideoAppart/apple_mouse_keyboard/frames"
output_file = "dataset_apple_mouse_keyboard.json"

input_path = "/media/mzins/DATA1/VideoAppart/bulle_1/frames"
output_file = "dataset_bulle_1.json"

input_path = "/media/mzins/DATA1/VideoAppart/bulle_2/frames"
output_file = "dataset_bulle_2.json"

input_path = "/media/mzins/DATA1/VideoAppart/bulle_3/frames"
output_file = "dataset_bulle_3.json"

input_path = "/media/mzins/DATA1/VideoAppart/bulle_4/frames"
output_file = "dataset_bulle_4.json"

input_path = "/media/mzins/DATA1/VideoAppart/bulle_5/frames"
output_file = "dataset_bulle_5.json"



input_path = "/media/mzins/DATA1/VideoAppart/statues_train"
output_file = "dataset_statues_train.json"


input_path = "/media/mzins/DATA1/VideoAppart/ISMAR/reloc/frames"
output_file = "dataset_ismar_reloc.json"


for i in [1]: #range(1, 3):
    # input_path = "/media/mzins/DATA1/VideoAppart/kitchen_%d/frames" % i
    # output_file = "dataset_kitchen_%d.json" % i

    input_path = "/media/mzins/DATA1/VideoAppart/musee_meuble_%d/frames" % i
    output_file = "dataset_musee_meuble_%d.json" % i



    # files = sorted(glob.glob(os.path.join(input_path, "*.jpg")) + glob.glob(os.path.join(input_path, "*.color.png")))
    files = sorted(glob.glob(os.path.join(input_path, "*.png")))
    print(os.path.join(input_path, "*.png"))

    w = 640
    h = 360 #480

    out_data = []
    for f in files[::1]: #############################################################################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print(f)
        out_data.append({"file_name": f, "height": h, "width": w})

    with open(output_file, "w") as fout:
        json.dump(out_data, fout)