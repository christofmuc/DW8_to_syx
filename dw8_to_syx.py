import os
import re


# https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


for root, dirs, files in os.walk(".", topdown=False):
   for name in files:
        input_name = os.path.join(root, name)
        basename, ext = os.path.splitext(input_name)
        if ext.upper() == '.DW8':
            #input_file = R'D:\Christof\Music\DW8000\Patches\DW8-Format-from-textfile.com\FCTSIDEA.DW8'
            patch_number = 1
            with open(input_name, 'rb') as input_file:
                data = list(input_file.read())
                # print(data)
                if data[0] == 0 and data[1] == 64:
                    print("Valid DW8 file with correct header")
                    readPointer = 2
                    while readPointer + 70 <= len(data):
                        # First byte is used length of patch name
                        nameLen = data[readPointer]
                        if nameLen > 16:
                            print("Invalid patch name length, error parsing file!")
                            break
                        # 16 bytes length of patch name
                        name = bytearray(data[readPointer + 1: readPointer + 1 + 16])[:nameLen].decode('ascii',
                                                                                                       errors='ignore')

                        unknownByte1 = data[readPointer + 1 + 16]
                        sys_ex = data[readPointer + 1 + 16 + 1: readPointer + 1 + 16 + 1 + 0x33]
                        unknownByte2 = data[readPointer + 1 + 16 + 1 + 0x33]
                        #  print("Name of length", nameLen, "is", name, "unknown", unknownByte1,
                        #  "and", unknownByte2, "sys_ex", sys_ex)

                        filename = get_valid_filename("%s-%03d-%s.syx" %
                                                      (os.path.basename(input_name), patch_number, name))
                        with open(filename, "wb") as output_file:
                            # Create an Edit Buffer dump for the DW8000
                            syx = [0xf0, 0x42, 0x33, 0x03, 0x40] + sys_ex + [0xf7]
                            output_file.write(bytearray(syx))
                            print("Wrote", filename)
                        patch_number += 1
                        readPointer += 70
                else:
                    print("Wrong header, this might not be a DW8 file after all!")
