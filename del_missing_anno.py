import os
import shutil
import json
import glob
import argparse


def del_missing_ano(train_dir, boxes):
	'''
		helper function to delete files with missing annotations as the
		fish can hardly be seen in these images
	'''
	fish_classes = glob.glob(os.path.join(train_dir, '*'))
	for fc in fish_classes:
		if fc.split('/')[-1].lower() != 'nof':
			delete_count = 0
			with open(os.path.join('/'.join(train_dir.split('/')[:-1]), boxes, \
				fc.split('/')[-1].lower()+'_labels.json')) as fl_in:
				ann = json.load(fl_in)
				ann_imgs = [f['filename'].split('/')[-1] for f in ann]
				train_imgs = [f.split('/')[-1] for f in \
				glob.glob(os.path.join(fc, '*.jpg'))]
				for f in train_imgs:
					if f not in ann_imgs:
						delete_count += 1
						os.remove(os.path.join(fc, f))
			print '{} files with missing annotaitons in {}'.format(delete_count, \
				fc.split('/')[-1])


if __name__ == '__main__':
	# get original training directory
	parser = argparse.ArgumentParser(add_help=False)
	parser.add_argument('-d', '--directory', required=True)
	parser.add_argument('-b', '--boxes', required=True)
	dirs = parser.parse_args()

	# delete files with missing annotations
	del_missing_ano(dirs.directory, dirs.boxes)