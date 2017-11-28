from __future__ import division
import csv
import sys
import numpy as np

fn = sys.argv[1]
f = np.array(list(csv.reader(open(fn, "rb"), delimiter=","))).astype("int")

#dividing data into train n validation

training_idx = np.random.randint(f.shape[0], size=int(f.shape[0] * 0.8))
test_idx = np.random.randint(f.shape[0], size=int(f.shape[0] * 0.2))
training, test = f[training_idx,:], f[test_idx,:]

#preprocessing
lab = np.asarray(training[:,0])
training[training[:,0] == 0] *= -1
lab[training[:,0]== 0] = -1

lab_t = np.asarray(test[:,0])
test[test[:,0] == 0] *= -1
lab_t[test[:,0]== 0] = -1

training = np.delete(training, 0, axis=1)
test = np.delete(test,0, axis=1)



def sim_per():
	w = np.random.rand(1,training.shape[1])
	const = 1000
	#looping over number of iterations
	while const!=0:
		#looping over the examples
		for i in range(0,training.shape[0]):
			x = training[i,:]
			prod = float(np.matmul(w, x))
			if (prod <0):
				w = np.add(w,x)  
			else:
				pass
		const -= 1
		#break
	return w

def with_margin():
	w = np.asmatrix(np.zeros((1,training.shape[1]), dtype=np.float))
	const = 1000
	b = 5
	#looping over number of iterations
	while const!=0:
		#looping over the examples
		for i in range(0,training.shape[0]):
			x = training[i,:]
			prod = float(np.matmul(w, x))
			if (prod <b):
				w = np.add(w,x)
				#break  
			else:
				pass
		const -= 1
		#break
	return w

def sim_batch():
	w = np.random.rand(1,training.shape[1])
	const = 1000
	while const!=0:
		batch = 68
		while batch<=training.shape[0]-1:
			sum_x = np.zeros((1,training.shape[1]))
			for i in range(0,batch):
				x = training[i,:]
				prod = float(np.matmul(w,x))
				if (prod <0):
					sum_x = np.add(sum_x,x)
				else:
					pass
				
			if(sum_x.all() != 0):
				prod = float(np.matmul(w,sum_x))
				w = np.add(w,x)
			else:
				pass
			batch += 68
		
		const -= 1

	#print sum_x

	return w

def batch_mar():
	w = np.random.rand(1,training.shape[1])
	const = 1000
	b = 5	
	while const!=0:
		batch = 68
		while batch<=training.shape[0]-1:
			sum_x = np.zeros((1,training.shape[1]))
			for i in range(0,batch):
				x = training[i,:]
				prod = float(np.matmul(w,x))
				if (prod <b):
					sum_x = np.add(sum_x,x)
				else:
					continue
				
			if(sum_x.all() != 0):
				prod = float(np.matmul(w,sum_x))
				w = np.add(w,x)
			else:
				pass
			batch += 68
		
		const -= 1

	#print sum_x

	return w


def validate():
	w = sys.argv[3] + ()
	fp=0 
	tp=0 
	tn=0 
	fn=0
	for i in range(0,test.shape[0]):
		x = test[i,:]
		prod = float(np.matmul(w, x))
		if (prod >=0 and lab_t[i] == -1):
			fp +=1
		elif (prod >=0 and lab_t[i]==1):
			tp +=1
		elif (prod <=0 and lab_t[i]== -1):
			tn +=1
		elif (prod <=0 and lab_t[i]==1):
			fn +=1

	print "Precision " + str(tp/(tp+fp)) , "Recall " + str(tp/(tp+fn)), "Accuracy " + str((tp + tn)/(tp + tn + fp + fn))



#validate()
def print_labels():
	f_1 = np.array(list(csv.reader(open(sys.argv[2], "rb"), delimiter=","))).astype("int")
	w = sim_per()
	rows = f_1.shape[0]
	for i in range(0,rows):
		x = f_1[i,:]
		prod = np.matmul(w, x)
		if prod >= 0:
			print "1"
		elif prod <0:
			print "0"
	w = with_margin()
	rows = f_1.shape[0]
	for i in range(0,rows):
		x = f_1[i,:]
		prod = float(np.matmul(w, x))
		#print prod
		if prod >= 0:
			print "1"
		elif prod <0:
			print "0"
	w = sim_batch()
	rows = f_1.shape[0]
	for i in range(0,rows):
		x = f_1[i,:]
		prod = float(np.matmul(w, x))
		if prod >= 0:
			print "1"
		elif prod <0:
			print "0"
	w = batch_mar()
	rows = f_1.shape[0]
	for i in range(0,rows):
		x = f_1[i,:]
		prod = float(np.matmul(w, x))
		if prod >= 0:
			print "1"
		elif prod <0:
			print "0"



print_labels()
#validate()
