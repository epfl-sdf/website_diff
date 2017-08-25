import argparse

INPUT_FILE= '../credentials/credentials.csv'
OUTPUT_FILE= '../data_web_diff/sites.csv'

def make_data():
    input_file = open(INPUT_FILE, 'r')
    output_file = open(OUTPUT_FILE, 'w')
    next(input_file)
    print('name, url1, url2', file = output_file)

    for line in input_file:
        parts = line.split(',')
        url_jahia = parts[1]
        url_wp = parts[2]
        test_name = parts[3]
        
        print(','.join((test_name, url_jahia, url_wp)), file = output_file)

    input_file.close()
    output_file.close()

if __name__ == "__main__":
    make_data()
