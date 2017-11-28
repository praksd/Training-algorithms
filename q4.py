from __future__ import division
import numpy as np 
import  csv
import sys
import os
import re 
import heapq

train = sys.argv[1]
test = sys.argv[2]
bow = {}

list_of_classes = []
list_of_classes = os.listdir(train)
classes = ['galsworthy','galsworthy_2','mill','shelley','thackerey','thackerey_2','wordsmith_prose','cia','johnfranklinjameson','diplomaticcorr']

#d is list of directories or classes
#f is filename of that class
def bag_of_words():
	i = 0
	for d in list_of_classes:
		#print "inside d"
		list_of_files = []
		list_of_files = os.listdir(train + '/' +d)
		for f in list_of_files:
		#	print "inside f"
			f_s = open(train+ '/' + d + '/' + f, "r").read().replace('\n','') # a string storing the whole data in the file
			f_s = re.sub('<[^>]*>','',f_s)
			f_s = f_s.replace('  ', ' ')
			tmp_list = f_s.split(' ')
			#print tmp_list
			for w in tmp_list:
				if w not in bow:
					bow[w] = i
					i += 1
				else:
					pass
			#print bow 
			#print f_s
	return bow, i+1


def train_vector(bow, len_bow):
	#print "inside vector_of_each_doc"
	#print bow
	f_d_train = {} #dictionary of all f_f vecctors for all classes.
	for d in list_of_classes:
		#print "inside d"
		list_of_files = []
		list_of_files = os.listdir(train + '/' +d)
		f_f_train = [] #list of vectors of each file in a class
		for f in list_of_files:
		#	print "inside f"
			f_s = open(train+ '/' + d + '/' + f, "r").read().replace('\n','') # a string storing the whole data in the file
			f_s = re.sub('<[^>]*>','',f_s)
			f_s = f_s.replace('  ', ' ')
			tmp_list = f_s.split(' ') #list of all the words in a given file
			tmp_count = [0] * len_bow
			for w in tmp_list:
				tmp_count[bow[w]] += 1 
			#print len(tmp_count), len_bow
			#print tmp_count
			f_f_train.append(tmp_count)
			#break
		f_d_train[d] = f_f_train
		#print f_d
		#break
	return f_d_train, f_f_train

def test_vector(bow,len_bow):
	list_of_classes = os.listdir(test)
	f_d_test = {}
	for d in list_of_classes:
		#print "inside d"
		list_of_files = []
		list_of_files = os.listdir(test + '/' +d)
		f_f_test = [] #list of vectors of each file in a class
		for f in list_of_files:
		#	print "inside f"
			f_s = open(test+ '/' + d + '/' + f, "r").read().replace('\n','') # a string storing the whole data in the file
			f_s = re.sub('<[^>]*>','',f_s)
			f_s = f_s.replace('  ', ' ')
			tmp_list = f_s.split(' ') #list of all the words in a given file
			tmp_count = [0] * len_bow
			for w in tmp_list:
				if w in bow:
					tmp_count[bow[w]] += 1
				else:
					pass 
			#print len(tmp_count), len_bow
			#print tmp_count
			f_f_test.append(tmp_count)
			#break
			 
		f_d_test[d] = f_f_test	
		#break
	return f_d_test, f_f_test



def distance():
	bow, len_bow = bag_of_words()
	f_d_train, f_f_train = train_vector(bow, len_bow)
	f_d_test, f_f_test = test_vector(bow, len_bow)
	k = 10; conf_mat = np.zeros((10,10))
	tp = 0; total = 0;
	for d in f_d_test:
		#print "orig dir " + d
		#print classes.index(d)
		k_list = []; k_dic = {};
		for a in f_d_test[d]:
			for d1 in f_d_train:
				for b in f_d_train[d1]:
					eu_dis = np.linalg.norm(np.asarray(a)-np.asarray(b))
					k_list.append(eu_dis)
					k_dic[eu_dis] = d1
	        
			tmp_dic = {};
			k_list = heapq.nsmallest(k, k_list)
			for i in range(0,k):
				#print k_dic[k_list[i]]
				if k_dic[k_list[i]] not in tmp_dic: 
					tmp_dic[k_dic[k_list[0]]] = 1
				else:
					tmp_dic[k_dic[k_list[0]]] += 1
			max_val = [(value, key) for key, value in tmp_dic.items()]
			#print max_val
			conf_mat[classes.index(d)][classes.index(max(max_val)[1])] += 1
			print max(max_val)[1]
	#print conf_mat
	for i in range(0,10):
		for j in range(0,10):
			if i==j:
				tp += conf_mat[i][j]
			total += conf_mat[i][j]
	
	#print tp/total




distance()