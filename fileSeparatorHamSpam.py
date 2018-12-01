import os, csv

spampath = "spamemails/"
hampath = "hamemails/"
os.system("mkdir %s"%(spampath))
os.system("mkdir %s"%(hampath))
sindx = 1
hindx = 0
with open("rawdata.csv", 'rb') as csvfile:
	spamreader = csv.reader(csvfile)
	for i, row in enumerate(spamreader):
		if row[0] == "spam":
			fs = open("%semail%d.txt"%(spampath, sindx), "w")
			fs.write(row[1])
			fs.close()
			sindx += 1
		else:
			fh = open("%semail%d.txt"%(hampath, hindx), "w")
			fh.write(row[1])
			fh.close()
			hindx += 1
