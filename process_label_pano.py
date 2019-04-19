# General Utilities
import re
import os
import sys
import random
import subprocess
from PIL import Image
from PIL import ImageDraw
import argparse
from os import listdir
from os.path import isfile, join
import urllib.request as urllib
from coordinates_to_xml import write_xml
import shutil

# ML / Deep learning Utilities
import cv2
import numpy as np
from numpy import loadtxt
import pandas as pd
import csv


# Helper functions
def mkdir(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
        else:
            print("(%s) already exists" % (path))

def check_titles(target_word, titles):
    for value in titles:
        if target_word in value:
            return True
    return False

def save_sliding_xml(x1,y1,x2,y2,slide_x1,slide_y1,i,image_key, slide_key):
    new_x1 = max(slide_x1, x1[i]) - slide_x1
    new_y1 = max(slide_y1, y1[i]) - slide_y1
    new_x2 = min(slide_x1+600, x2[i]) - slide_x1
    new_y2 = min(slide_y1+600, y2[i]) - slide_y1
    xml_file = "labels/sign_"+str(image_key)+"_"+str(slide_key)+".xml"
    pic_file = "sign_"+str(image_key)+"_"+str(slide_key)+".jpg"

    write_xml(xml_file, 'sign' , new_x1, new_x2, new_y1, new_y2, 600, 600, pic_file)



# for sign detection
def picture_present(x1, y1, x2, y2, slide_x1, slide_y1):
    photo_percentage = 0.5

    for i in range(len(x1)):
        if(x1[i] <= (slide_x1 + 600) and x2[i] >= slide_x1 and y1[i] <= (slide_y1 + 600) and y2[i] >= slide_y1):
            w = x2[i]-x1[i]
            h = y2[i]-y1[i]
            a1 = w*h

            new_w = min(x2[i],slide_x1+600) - max(x1[i],slide_x1)
            new_h = min(y2[i],slide_y1+600) - max(y1[i],slide_y1)
            a2 = new_h*new_w

            if(a2/a1 >= photo_percentage):
                return i
    return -1

def panorama_loop(image_url, x1, y1, x2, y2, image_key):
    temp_file_name = "temp.jpg"
    urllib.urlretrieve(image_url,temp_file_name)

    pano = Image.open(temp_file_name)
    pano_x = pano.size[0]
    pano_y = pano.size[1]
    j = 0
    for slide_x1 in range(0, pano_x, 300):
        if(slide_x1 > (pano_x-600)):
            continue
        for slide_y1 in range(0, pano_y, 300):
            if(slide_y1 > (pano_y-600)):
                break
            i = picture_present(x1,y1,x2,y2,slide_x1,slide_y1)
            if(i > -1):
                save_sliding_xml(x1,y1,x2,y2,slide_x1,slide_y1,i,image_key,j)
                pic_file = "images/sign_"+str(image_key)+"_"+str(j)+".jpg"
                new_pic = pano.crop((slide_x1, slide_y1, slide_x1+600, slide_y1+600))
                new_pic = new_pic.convert('L')
                new_pic.save(pic_file)
                j += 1

def sign_detection():
    images_file = "signs.csv"

    x1 = []
    x2 = []
    y1 = []
    y2 = []
    prev_pk = 0
    current_pk = 1
    image_url = ""

    with open(images_file) as csv_file:
        i = 0
        upper_limit = 10000

        # Getting rid of filepaths
        newlabels = r'labels'
        newimages = r'images'
        if os.path.exists(newlabels):
            shutil.rmtree(newlabels)
        if os.path.exists(newimages):
            shutil.rmtree(newimages)
        os.makedirs(newlabels)
        os.makedirs(newimages)

        for row in csv.reader(csv_file, delimiter=','):
            if (i % 500 == 0):
                print(i)
            if i > upper_limit or row[5] == "":
                break
            if not (row[6] == '' or row[9] == '' or row[10] == '' or row[11] == '' or row[12] == ''):
                try:
                    current_pk = int(row[6])
                except:
                    continue
                if(prev_pk == current_pk):
                    x1.append(int(row[9]))
                    x2.append(int(row[10]))
                    y1.append(int(row[11]))
                    y2.append(int(row[12]))
                else:
                    if(prev_pk >= 1):
                        panorama_loop(image_url, x1, y1, x2, y2, prev_pk)
                    image_url = row[5]
                    prev_pk = current_pk
                    x1 = []
                    x2 = []
                    y1 = []
                    y2 = []
                    x1.append(int(row[9]))
                    x2.append(int(row[10]))
                    y1.append(int(row[11]))
                    y2.append(int(row[12]))
                i += 1


#word specific detection
def word_present(titles, x1, y1, x2, y2, slide_x1, slide_y1, target_word):
    photo_percentage = 0.5

    target_word_locations = []
    for i in range(len(titles)):
        if target_word in titles[i]:
            target_word_locations.append(i)

    for i in target_word_locations:
        if(x1[i] <= (slide_x1 + 600) and x2[i] >= slide_x1 and y1[i] <= (slide_y1 + 600) and y2[i] >= slide_y1):
            w = x2[i]-x1[i]
            h = y2[i]-y1[i]
            a1 = w*h

            new_w = min(x2[i],slide_x1+600) - max(x1[i],slide_x1)
            new_h = min(y2[i],slide_y1+600) - max(y1[i],slide_y1)
            a2 = new_h*new_w
            print(a2/a1)
            if(a2/a1 >= photo_percentage):
                return i

    return -1


def cnn_panorama_loop(image_url, titles, x1, y1, x2, y2, image_key, target_word):
    temp_file_name = "temp.jpg"
    urllib.urlretrieve(image_url,temp_file_name)

    pano = Image.open(temp_file_name)
    pano_x = pano.size[0]
    pano_y = pano.size[1]
    j = 0
    for slide_x1 in range(0, pano_x, 300):
        if(slide_x1 > (pano_x-600)):
            continue
        for slide_y1 in range(0, pano_y, 300):
            if(slide_y1 > (pano_y-600)):
                break
            i = word_present(titles,x1,y1,x2,y2,slide_x1, slide_y1,target_word)
            if (i == -1):
                i = picture_present(x1,y1,x2,y2,slide_x1, slide_y1)
            if(i > -1):
                if target_word in titles[i]:
                    pic_file = "positive/sign_"+str(image_key)+"_"+str(j)+".jpg"
                else:
                    pic_file = "negative/sign_"+str(image_key)+"_"+str(j)+".jpg"
                new_pic = pano.crop((slide_x1, slide_y1, slide_x1+600, slide_y1+600))
                new_pic = new_pic.convert('L')
                new_pic.save(pic_file)
                j += 1



def word_detection(target_word):
    images_file = "signs.csv"

    x1 = []
    x2 = []
    y1 = []
    y2 = []
    titles = []
    prev_pk = 1
    current_pk = 1
    image_url = ""


    with open(images_file) as csv_file:
        i = 0

        # Getting rid of filepaths
        containing_word = r'positive'
        not_containing_word = r'negative'
        if os.path.exists(containing_word):
            shutil.rmtree(containing_word)
        if os.path.exists(not_containing_word):
            shutil.rmtree(not_containing_word)
        os.makedirs(containing_word)
        os.makedirs(not_containing_word)

        for row in csv.reader(csv_file, delimiter=','):
            if (i % 2000 == 0):
                print(i)

            if not (row[6] == '' or row[9] == '' or row[10] == '' or row[11] == '' or row[12] == ''):
                try:
                    current_pk = int(row[6])
                except:
                    continue
                if(current_pk == 1):
                    image_url = row[5]
                if(prev_pk == current_pk):
                    titles.append(row[1].lower())
                    x1.append(int(row[9]))
                    x2.append(int(row[10]))
                    y1.append(int(row[11]))
                    y2.append(int(row[12]))
                else:
                    prev_pk = current_pk
                    if(check_titles(target_word, titles)):
                        cnn_panorama_loop(image_url, titles, x1, y1, x2, y2, current_pk, target_word)
                    x1 = []
                    x2 = []
                    y1 = []
                    y2 = []
                    titles = []
                    titles.append(row[1].lower())
                    x1.append(int(row[9]))
                    x2.append(int(row[10]))
                    y1.append(int(row[11]))
                    y2.append(int(row[12]))
                    image_url = row[5]
                i += 1

# Main function
if __name__ == '__main__':
    sign_detection()
