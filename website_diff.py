#import pillow
import csv
from PIL import Image
import math
import numpy as np
from urllib.parse import urlparse
import time
import os
import glob
import collections
import argparse
from datetime import datetime

from selenium import webdriver

from pyvirtualdisplay import Display

Size = collections.namedtuple("size", ("x", "y"))
WAIT_TIME = 10

SIZES = [Size(1080, 1920)]

def cut_histogram_min(h, min_value=10):
    return map(lambda value: min(min_value, value), h)

def cut_histogram_color(h, color=10):
    return map(lambda value: 0 if value == color else value, h)

def bhattacharyya(h1, h2):
    '''Calculates the Byattacharyya distance of two histograms.'''

    def normalize(h):
        h_float = list(map(float, h))
        return map(lambda x : x / np.sum(h_float), h_float)

    multi = np.multiply(list(normalize(h1)), list(normalize(h2)))
    return 1 - np.sum(np.sqrt(multi))

def get_histogram(image):
    histogram = []
    (width, height) = image.size
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            if pixel[0] != 255 and pixel[1] != 255 and pixel[2] != 255:
                histogram.append(pixel[0] * pixel[1] * pixel[2])
    
    return np.histogram(histogram, bins=100)[0].tolist()

def diff_image_color(image_path0, image_path1):
    """Return similarity of image clamped between 0 and 1, based
    on color histogram.
    """
    image0 = Image.open(image_path0)
    #color_image0 = get_histogram(image0)
    color_image0 = image0.histogram()
    cut_color_image0 = cut_histogram_min(color_image0)
    image1 = Image.open(image_path1)
    color_image1 = image1.histogram()
    #color_image1 = get_histogram(image1)
    cut_color_image1 = cut_histogram_min(color_image1)
    color_difference = bhattacharyya(color_image0, color_image1)
    return color_difference


def diff_image_feature(image0, image1):
    """Return similarity of image clamped between 0 and 1
    on feature.
    """
    return 0

def screenshot(url, path, alter=None, browser=''):
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.http', '10.92.104.219')
    profile.set_preference('network.proxy.http_port', 8080)
    
    browser = webdriver.Firefox(profile)

    browser.get(url)
    time.sleep(WAIT_TIME)
    page = browser.page_source
    for size in SIZES:
        browser.set_window_position(0, 0)
        browser.set_window_size(size.x, size.y)
        #wait for the site to adapt
        time.sleep(0.3)
        browser.save_screenshot(path)
    browser.quit()

def compare_sites(args):
    input_file = open(args.ficher_des_sites, 'r')
    output_file = open('coeffs.csv', 'a')
    next(input_file)

    for line in input_file:
        parts = line.split(',')
        url_jahia = parts[1]
        url_wp = parts[2]
        site_title = parts[3]

        timestamp = str(datetime.now())
        filename_jahia = site_title + '_jahia'+ timestamp +'.png'
        filename_wp = site_title + '_wp' + timestamp +'.png'
        screenshot(url_jahia, filename_jahia)
        screenshot(url_wp, filename_wp)
        coeff = 1 / diff_image_color(filename_jahia, filename_wp)

        print(','.join((site_title, url_jahia, url_wp, str(coeff), timestamp)), file = output_file)

def get_parser():
    """ Obtiens un parser les arguments de ligne de commande. """
    parser = argparse.ArgumentParser(description='Parser des liens sur les sites Jahia et Wordpress.')
    parser.add_argument('ficher_des_sites', help='le fichier contenant les sites a parser.')
    return parser

if __name__ == "__main__":
    display = Display(visible=0, size=(800, 600))
    display.start()

    # Parser des arguments des lignes de commande.
    parser = get_parser()
    args = parser.parse_args()

    compare_sites(args)

