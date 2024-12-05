import random

_BASE64_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-'

def get():

    return ''.join(random.choice(_BASE64_CHARS) for i in range(22))

if __name__ == '__main__':

    import argparse

    p = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                description    ='Get a base-64 identifier1\nUseful to generate Kafka cluster IDs, etc')
    p.parse_args()
    print(get())
