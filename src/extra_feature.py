import os
import re
import random
import math
import sys

#result is a confusion matrix (69x69) - 2 Dimensional
result = []
#path_test is the path of test folder
path_test = sys.argv[1]
#path_training is the path of training folder
path_training = sys.argv[2]

sentence_ave = []
author_list = [] 
authors = []
article_nums = []
hash_array = []
word_nums = []
lenghtOfArticle = []
test_articleNums = []
vocabulary = set()
true_ = 0
false_ = 0
counter = 0

def calculation(newTokenList,sentence_over_lenght):
	probability_of_auth = []
	for k in range(0, 69):
		n = 0
		prob = 0
		for one_word in newTokenList:
			if one_word in hash_array[k]:
				num = (hash_array[k][one_word]+1)/(lenghtOfArticle[k]+len(vocabulary)*1)
				num = math.log(num,2)
				prob = prob + num
			else:
				num = (1)/(lenghtOfArticle[k]+len(vocabulary))
				num = math.log(num,2)
				prob = prob + num
		prob = prob - abs(sentence_over_lenght - sentence_ave[k])
		probability_of_auth.append(prob)


	result = probability_of_auth.index(max(probability_of_auth))
	return result


#each string in author_list is like its path : raw_texts/abbasGuclu
#first I put each author folder's path in author_list
for dirname, dirnames, filenames in os.walk(path_training):
	for subdirname in dirnames:
		author_path = os.path.join(dirname, subdirname)
		author_list.append(author_path)
	

#we get rid of raw_text/. authors have the name of each author
#in other words, we remove the path from the each element in the author_list,
#so that we actually get the name of each author's folder
#authors store the folder names of each author.
for author in author_list:
	author = author[len(path_training)+1:]
	authors.append(author)


#in this part, we start reading from training folder.
#we create a hashmap for each author (bag of words)
#after creating hashmap (bag of words) for each author,
#we add them into hash_array
#so, hash_array is an array size of 69, holding hashmaps for each author.
#lenghtOfArticle is an array size of 69, it holds the total lenght of articles that
#belong to current author.

n = -1
for auth in authors:
	n = n+1
	hashmap = {}
	length_article = 0; #it is initialized as 0 for each author.

	for dirname, dirnames, filenames in os.walk(path_training+'/'+auth):
		#tokenlist = []
		numOfsentence = 0
		#filenames is the list of training articles belong to this author.
		for i in filenames:
			tokenlist = []
			everything = open(path_training+'/'+auth+'/'+i,'r', encoding = 'cp1254')
			allwords = everything.read()
			tokenlist = tokenlist + re.split('\W+', allwords)
			sentences = re.split('[.?!]', allwords)
			numOfsentence = numOfsentence + len(sentences)
			trashes = (['','&', ';', ':', '...', ')', '(', '.', "'", ',', '``', '-', "''",'1','2','3','4','5','6','7','8','9','0'])

			newTokenList =  [ i for i in tokenlist if i not in trashes]
			#newTokenList =  [ i for i in newTokenList if not i.isdigit()]
			newTokenList = [oneToken.lower() for oneToken in newTokenList]

			#we keep summing up the article length to get total for this author.
			length_article = length_article + len(newTokenList) 

			for token in newTokenList:
				vocabulary.add(token)
				if token in hashmap:
					hashmap[token] = hashmap[token] + 1
				else:
					hashmap[token] = 1

		sentence_ave.append(numOfsentence/length_article)
		#adding the total lenght of articles of this author to the list.
		lenghtOfArticle.append(length_article)

	#for each author, we add its hashmap to the list.
	hash_array.append(hashmap)

#for each author, we start reading test folder.
n = -1
for auth in authors:
	result_per_auth = [0]*69
	n = n+1

	for dirname, dirnames, filenames in os.walk(path_test+'/'+auth):
		tokenlist = []
		
		#filenames is the list of test articles belong to current author
		for i in filenames:
			
			everything = open(path_test+'/'+auth+'/'+i,'r', encoding = 'cp1254')
			allwords = everything.read()
			tokenlist = tokenlist + re.split('\W+', allwords)
			sentences = re.split('[.?!]', allwords)
			trashes = (['','&', ';', ':', '...', ')', '(', '.', "'", ',', '``', '-', "''",'1','2','3','4','5','6','7','8','9','0'])
			newTokenList =  [ i for i in tokenlist if i not in trashes]
			#newTokenList =  [ i for i in newTokenList if not i.isdigit()]
			newTokenList = [oneToken.lower() for oneToken in newTokenList]
			length = len(newTokenList)
			numOfSentence = len(sentences)

			#after tokenizing the test article, we call the probability calculation
			#method, prob is the result of our function.
			#calculation returns the index of author, if it is equals to n
			#then it finds the correct result.

			prob = calculation(newTokenList, numOfsentence/length)
			#while reading test files, we create result matrix.
			#result_per_auth is a list, after reading all test articles of this author,
			#we add result_per_auth to result list.
			result_per_auth[prob] = result_per_auth[prob] + 1
			#print(authors[n]+ ' '+ authors[prob])
			if prob == n :
				true_ = true_ +1
			else:
				false_ = false_ + 1
	#here we fill result matrix. (confusion matrix)
	result.append(result_per_auth)	
print(true_)
print(false_)
print(true_ / (true_+false_))

