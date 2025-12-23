# import Client.img.AddRemoveTakeList as Client
# import utils.inputAndValidate as check
# from Client.img.SaveFace import save_face_event
# client = Client.CameraClient("192.168.100.119","admin","Batek@abcd")


# chose = 2
# while(True):
#     client.login()
#     if chose == 1:
#         info = check.input_and_validate1()
#         client.add_face(info)
#     if chose == 2:
#         while True:
#             print("Group ID phải là số nguyên!")
#             value = input("Enter group ID you want to select: ").strip()
#             if value.isdigit():
#                 client.get_images_feature(int(value))
#     if chose == 3:
#         pass