import re
import math
import sys

#the first argument is the filename for training data.
#the second argument is either cpost or post.
fname = sys.argv[1]
post_cpost = sys.argv[2]

if post_cpost == 'cpost' :
	num = 3
else :
	num = 4

#dic_word_tag is the dictionary in which keys are current_word-current_tag pairs and value is its count
#dic_tag_previous is the dictionary in which keys are current_tag-previous_tag pairs and value is its count
#dic_tag is the dictionary in which keys are the tags and value is its count
dic_word_tag = {}
dic_tag_previous = {}
dic_tag = {}

with open(fname) as f:
    content = f.readlines()

#all sentences start with 'START' tag.
previous_tag = 'START'
current_tag = ''
current_word = ''


#temp is for the count of 'START' tag. it also gives the number of sentences.
#all sentences end with 'END' tag, so we also add this tag to the dictionary.
temp = 0
dic_tag['END'] = 0

#start reading input file line by line.
#content is a list of lines in the document. sentence holds each line as a list of tokens.
for text in content:
	sentence = text.split('\t')
	if len(sentence) == 10 : #if the line is not '\n'
		 #num holds the order of post or cpost. for example if im looking at cpost, then it is 3 since cpost is the 4th token.
		current_tag = sentence[num]
		current_word = sentence[1].lower()
		#if there is '_' rather than a word, we ignore
		if current_word != '_' :
			tuple_1 = (current_word, current_tag)
			if tuple_1 in dic_word_tag:
				dic_word_tag[tuple_1] = dic_word_tag[tuple_1] + 1
			else:
				dic_word_tag[tuple_1] = 1

			tuple_2 = current_tag
			if tuple_2 in dic_tag:
				dic_tag[tuple_2] = dic_tag[tuple_2] + 1
			else:
				dic_tag[tuple_2] = 1

			tuple_3 = (current_tag, previous_tag)
			if tuple_3 in dic_tag_previous:
				dic_tag_previous[tuple_3] = dic_tag_previous[tuple_3] + 1
			else:
				dic_tag_previous[tuple_3] = 1	

			previous_tag = current_tag
	#if we are at the end of the sentence, we add 'END' tag and assign 'START' to the previous_tag
	else:
		dic_tag['END']+=1
		tuple_4 = ('END', previous_tag)
		if tuple_4 in dic_tag_previous:
			dic_tag_previous[tuple_4]+=1
		else:
			dic_tag_previous[tuple_4] = 1
	
		previous_tag = 'START'
		temp+=1

dic_tag['START'] = temp #as I told above, temp is the number of 'START' tags, also number of sentences.


#after reading the training file, we create a new file called 'output.txt', to save our dictionaries created above.

f = open('output.txt','w')


for key in dic_tag:
	f.write('1')
	f.write(' ')
	f.write(key)
	f.write(' ')
	f.write(str(dic_tag[key]))
	f.write('\n')


for (tag1, tag2) in dic_tag_previous:
	f.write('2')
	f.write(' ')
	f.write(tag1)
	f.write(' ')
	f.write(tag2)
	f.write(' ')
	f.write(str(dic_tag_previous[(tag1, tag2)]))
	f.write('\n')


for (word, tag) in dic_word_tag:
	f.write('3')
	f.write(' ')
	f.write(word)
	f.write(' ')
	f.write(tag)
	f.write(' ')
	f.write(str(dic_word_tag[(word, tag)]))
	f.write('\n')


f.close()

#in addition to output.txt file, to read tags and cpost/post , I also create 2 files;
#tagList.txt keeps the tag list.
#post_cpost keeps the post decider from the user

f_2 = open('tagList.txt','w')
tagList = dic_tag.keys()
print(dic_tag.keys())

for tag in tagList:
	f_2.write(tag)
	f_2.write('\n')

f_2.close()

f_3 = open('post_cpost.txt', 'w')
f_3.write(post_cpost)
f_3.close()
