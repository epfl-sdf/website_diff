import argparse

def make_data(args):
    input_file = open(args.ficher_des_sites, 'r')
    output_file = open(args.fichier_cible, 'w')
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

def get_parser():
    """ Obtiens un parser les arguments de ligne de commande. """
    parser = argparse.ArgumentParser(description='Parser des liens sur les sites Jahia et Wordpress.')
    parser.add_argument('ficher_des_sites', help='le fichier contenant les sites a parser.')
    parser.add_argument('fichier_cible', help='le fichier du résultat.')
    return parser

if __name__ == "__main__":
    # Parser des arguments des lignes de commande.
    parser = get_parser()
    args = parser.parse_args()

    make_data(args)
