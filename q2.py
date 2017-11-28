from __future__ import division
import csv
import sys
import numpy as np

fn = sys.argv[1]
f = np.array(list(csv.reader(open(fn, "rb"), delimiter=","))).astype("int")
row, columns = f.shape
#dividing data into train n validation

training_idx = np.random.randint(f.shape[0], size=int(row*0.8))
test_idx = np.random.randint(f.shape[0], size=int(row*0.2))
training, test = f[training_idx,:], f[test_idx,:]
#print training

lab = np.asarray(training[:,10])
training[training[:,10] == 2] *= -1
lab[training[:,10]== -2] = -1
lab[training[:,10]== 4] = 1
#print lab

lab_t = np.asarray(test[:,10])
test[test[:,10] == 2] *= -1
lab_t[test[:,10]== -2] = -1
lab_t[test[:,10]== 4] = 1
#print training.shape[1]
training = np.delete(training, 10, axis=1)
#print training
test = np.delete(test,10, axis=1)

#preprocessing
#lab = np.asarray(f[:,10])
#f[f[:,10] == 2] *= -1
#lab[f[:,10]== -2] = -1
#lab[f[:,10]== 4] = 1

def rel_with_margin():
	w = np.random.rand(1,training.shape[1])
	#print w
	const = 1000
	b = 3
	#looping over number of iterations
	while const!=0:
		#looping over the examples
		for i in range(0,training.shape[0]):
			x = training[i,:]
			prod = float(np.matmul(w, x))
			#print prod, lab[i]
			if (prod <b):
				w = w - ((prod - b)/(np.linalg.norm(x))**2) * np.asmatrix(x)
				# w = w - (prod/(np.linalg.norm(x))**2 - b) * np.asmatrix(x)
		const -= 1

		#break
	return w

def mod_per():
	w = np.random.rand(1,training.shape[1])
	b = 3
	for const in range(1,1000):
		n = 0.1/ (1+ 0.50 * const)
		for i in range(0,training.shape[0]):
			x = training[i,:]
			prod = float(np.matmul(w, x))
			if (prod <b):
				w = w - ((prod - b)/(np.linalg.norm(x))**2) * np.asmatrix(x)
				# w = w - (prod/(np.linalg.norm(x))**2 - b) * np.asmatrix(x)
			else:
				pass
	#print w
	return w


def validate():
	w = mod_per()
	fp=0
	tp=0
	tn=0
	fn=0
	for i in range(0,test.shape[0]):
		x = test[i,:]
		prod = float(np.matmul(w, x))
		if (prod >=0 and lab_t[i] == 2):
			fp +=1
		elif (prod >=0 and lab_t[i]==4):
			tp +=1
		elif (prod <=0 and lab_t[i]== 2):
			tn +=1
		elif (prod <=0 and lab_t[i]==4):
			fn +=1

	print "Precision " + str(tp/(tp+fp)) , "Accuracy " + str(tp/(tp+fn)), "Recall " + str((tp + tn)/(tp + tn + fp + fn))



def print_labels():
	f_1 = np.array(list(csv.reader(open(sys.argv[2], "rb"), delimiter=","))).astype("int")
	w = rel_with_margin()
	rows, columns = f_1.shape; prod =0
	for i in range(0,rows):
		x = f_1[i,:]
		prod = np.matmul(w, x)
		#print prod
		if prod >= 0:
			print "4"
		elif prod <0:
			print "2"
	w = mod_per()
	for i in range(0,rows):
		x = f_1[i,:]
		prod = np.matmul(w, x)
		#print prod
		if prod >= 0:
			print "4"
		elif prod <0:
			print "2"

	#w = with_margin()

print_labels()

#validate()
#validate_test_file()
