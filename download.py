import os
from pathlib import Path
import logging
import wget  # pip install python3-wget
import hashlib


logging.basicConfig(level=logging.INFO)


def get_md5(path):
    md5sum = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5sum.update(chunk)
    checksum = md5sum.hexdigest()
    return checksum


# http://occlusionperson.zhzh.ml:5288/occlusion_person
base_url = 'http://occlusionperson.zhzh.ml:5288/occlusion_person/occlusion_person.zip.'
base_path = Path('data')
if not os.path.exists(base_path):
    os.makedirs(base_path)

# obtain pre-generated checksum
with open('checksum.txt') as f:
    checksum_txt = f.readlines()
checksums = dict()
for r in checksum_txt:
    c, _, fname = r.split(' ')
    findex = int(fname[-4:-1])
    checksums[findex] = c


for i in range(1, 54):
    cur_url = '{}{:03d}'.format(base_url, i)
    out_path = base_path/'occlusion_person.zip.{:03d}'.format(i)
    pre_checksum = checksums[i]
    flag_success = False
    while True:
        if os.path.exists(out_path):
            checksum = get_md5(out_path)
            flag_success = pre_checksum == checksum
            if flag_success:
                logging.info('{} exists and checksum is correct'.format(out_path))
                break  # to next file
            else:
                logging.info('{} corrupted, removing it ...'.format(out_path))
                os.remove(out_path)  # remove corrupted file

        logging.info('downloading the {}-th file to {}'.format(i, out_path))
        wget.download(cur_url, out=str(out_path.absolute()), bar=wget.bar_adaptive)

# extract file
os.system('7z x data/occlusion_person.zip.001')
checksum = get_md5('images.zip')
if not checksum == 'abff95cad80bf02ab335e711855399a6':
    logging.info('Seems images.zip corrupted ...')
else:
    logging.info('All done for images.zip')
