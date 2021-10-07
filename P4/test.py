import random
# image_path = "imgs/image.png"
# bytes_array = open(image_path, 'rb').read()

# print(len(bytes_array))

# info = [bytes_array[i:i+114] for i in range(0, len(bytes_array), 114)]

# print(bytes_array == (info[0]+info[1]))

# # print(len(info))
# # print(len(info[1]))

# # print(b''.join(info))
# class CustomError(Exception):
#     pass

# import time

# timer1 = time.time() 

# # time.sleep(5)

# # print(time.time() - timer1)

# foo = True

# try: 
#     print("oi")


#     if foo == True:
#         raise CustomError
        

#     print("tchau")

# except CustomError:
#     print("boa")

# except:
#     print('?')

# try:
#     print("oi")
    

#     print("nao saiu")

# except:
#     print("?")


# foo = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t'

# head_list = []

# for i in range(8):
#     head_list.append(int.from_bytes(foo[i:i+1], "little"))


# head_list.append(int.from_bytes(foo[8:10], "little"))



# print(head_list)

# class EOPError(Exception):
#     pass

# a = 5

# try:
#     a += 6
#     if a != 2:
#         raise Exception

#     print("nao")

# except:
#     print("sim")

# ocioso = True
# a = 0

# while ocioso == True:
#     try:
#         if a < 5:
#             print(a)
#             a += 1
#             continue
#         print("fim")
#         ocioso = False

#     except:
#         print("?")

# bin = b'\x01\x0c\x17\x02\x00\xa6\x00\x00\x00\xc8'
# head_list = []

# for i in range(8):
#     head_list.append(int.from_bytes(bin[i:i+1], "little"))

# head_list.append(int.from_bytes(bin[8:10], "little"))

# print(int.from_bytes(bin[8:10], "big"))
# print(bin[8:10])

bin = int(200).to_bytes(2, 'little')

print(bin)

print(int.from_bytes(bin, "little"))

# bar = 5

# def foo(teste):
#     return teste + bar


# print(foo(4))