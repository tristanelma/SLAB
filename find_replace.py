import os
import fileinput

if __name__ == "__main__":
    directory = "labels"
    i = 0
    for filename in os.listdir(directory):
        if(i % 500 == 0):
            print(i)
        
        abs_path = "labels/" + filename
        f = open(abs_path,'r')
        filedata = f.read()
        f.close()
        os.remove(abs_path)

        newdata = filedata.replace("images/","")

        f = open(abs_path,'w')
        f.write(newdata)
        f.close()

        i += 1