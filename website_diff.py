import csv
import math
import numpy as np
import time
import os
import glob
import collections
import argparse
import timeit

from PIL import Image
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from urllib.parse import urlparse
from pyvirtualdisplay import Display
from version import __version__

sites_path = '../data_web_diff/sites.csv'
result_path = '../data_web_diff/result.csv'
screenshot_dir = '../data_web_diff/copy_screen/' 

Size = collections.namedtuple("size", ("x", "y"))
WAIT_TIME = 0.5

# Pour permettre d'afficher le temps
PRINT_TIME = False
def print_time(message, start_time):
    if PRINT_TIME:
        print(message,timeit.default_timer() - start_time)

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
    start_time = timeit.default_timer()
    browser.get(url)
    #time.sleep(WAIT_TIME)
    try:
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'nav-logo')))
    except WebDriverException:
        screenshot(url, path, alter, browser)
        return
    time.sleep(WAIT_TIME)
    page = browser.page_source
    for size in SIZES:
        browser.set_window_position(0, 0)
        browser.set_window_size(size.x, size.y)
        #wait for the site to adapt
        time.sleep(0.3)
        browser.save_screenshot(path)
    print_time('screenshot: ', start_time)

def compare_sites():
    start_time = timeit.default_timer()
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.http', '10.92.104.219')
    profile.set_preference('network.proxy.http_port', 8080)
    profile.set_preference('network.proxy.ssl', '10.92.104.219')
    profile.set_preference('network.proxy.ssl_port', 8080)
    print_time('init profile: ',start_time)

    start_time = timeit.default_timer()
    browser = webdriver.Firefox(profile)
    print_time('init browser: ',start_time)
    input_file = open(sites_path, 'r')
    output_file = open(result_path, 'a')

    next(input_file)

    for line in input_file:
        start_time = timeit.default_timer()
        parts = line.split(',')
        url_jahia = parts[1].strip()
        url_wp = parts[2].strip()
        site_title = parts[0].strip()

        timestamp = datetime.now().strftime('%Y%m%d.%H%M%S')
        filename_jahia = screenshot_dir + site_title + '_jahia'+ timestamp +'.png'
        filename_wp = screenshot_dir + site_title + '_wp' + timestamp +'.png'
        screenshot(url_jahia, filename_jahia, browser=browser)
        screenshot(url_wp, filename_wp, browser=browser)
        coeff = 1 / diff_image_color(filename_jahia, filename_wp)
        print(','.join((site_title, url_jahia, url_wp, str(coeff), timestamp)), file = output_file)
        print_time('compare ' + site_title + ': ',start_time)

    browser.quit()
    input_file.close()
    output_file.close()

if __name__ == "__main__":
    start_time = timeit.default_timer()
    display = Display(visible=0, size=(800, 600))
    display.start()

    print('website_diff version ' + __version__)
    compare_sites()
    print_time('total: ',start_time)

