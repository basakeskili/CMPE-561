import os
import shutil
import sys
import re
import random


article_nums = [] #list of 69. Holds the number of articles for each author.
authors = []
author = []
author_list = []

path_ = sys.argv[1]
path_test = sys.argv[2]
path_training = sys.argv[3]
train_articles = []

#each string in author_list is like its path : raw_texts/abbasGuclu
for dirname, dirnames, filenames in os.walk(path_):
	for subdirname in dirnames:
		author_path = os.path.join(dirname, subdirname)
		author_list.append(author_path)

#we get rid of raw_text/. authors have the name of each author
for author in author_list:
	author = author[10:]
	authors.append(author)

#we get numbr of articles because we will need it ti calculate random ones.
for auth in authors:
	for dirname, dirnames, filenames in os.walk(path_+'/'+auth):
		article_nums.append(len(filenames))


#creating training folder
os.makedirs(path_training)

n = -1
for auth in authors:
	rand_articles = []
	os.makedirs(path_training+'/'+auth)
	n = n+1	
	for dirname, dirnames, filenames in os.walk(path_+'/'+auth):
		num = article_nums[n]*0.6
		training = int(num)
		test = article_nums[n] - training
		rand_articles = random.sample(range(0, article_nums[n]), int(num))
		print(auth+' = '+str(training)+' & '+str(test))
		train_articles.append(rand_articles)

		for i in rand_articles:
			src = path_+'/'+auth+'/'+filenames[i]
			dst = path_training+'/'+auth+'/'+filenames[i]
			shutil.copyfile(src, dst)


#creating test folder
os.makedirs(path_test)
n = -1
for auth in authors:
	n = n+1
	os.makedirs(path_test+'/'+auth)

	for dirname, dirnames, filenames in os.walk(path_+'/'+auth):
		for i in range(0, article_nums[n]):
			if i not in train_articles[n]:
				src = path_+'/'+auth+'/'+filenames[i]
				dst = path_test+'/'+auth+'/'+filenames[i]
				shutil.copyfile(src, dst)






