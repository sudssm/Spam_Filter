from Predictor import Predictor
import pickle
import glob
import sys
import os

usage = sys.argv[0] + " [load | train] [\"\" | test | testFileOrFolder]"

if len(sys.argv) < 2:
  print "Usage:", usage
  sys.exit()
if sys.argv[1] == "load":
  usePickle = True
elif sys.argv[1] == "train":
  usePickle = False
else:
  print "Usage:", usage
  sys.exit()

#create classifier
if usePickle:
  print "Importing Classifier"
  p = pickle.load(open('predictor.pickle', 'r'))
else:
  print "Training Classifier"
  p = Predictor("spam", "ham")
  print "Saving Pickle"
  pickle.dump(p, open('predictor.pickle', 'w'))

if len(sys.argv) > 2:
  if sys.argv[2] == "test":
    hsuccess=0
    htotal=0
    ssuccess=0
    stotal=0
    count =0 
    for line in open("SPAMTrain.label"):
      count += 1
      print "\rRunning on Test Data Set:",count,"of",4327,
      l= line.strip().split()
      if l[0] == '0':
        stotal += 1
        if p.predict("test/" + l[1]) == 1:
          ssuccess +=1
      else:
        htotal += 1
        if p.predict("test/" + l[1]) == 0:
          hsuccess +=1
    print ""
    print "Ham:"
    print hsuccess,"of",htotal,"-",100-(100*(hsuccess/float(htotal))),"% Error"
    print "Spam:"
    print ssuccess,"of",stotal,"-",100-(100*(ssuccess/float(stotal))),"% Error"
    print ""
    print "Total"
    print hsuccess+ssuccess,"of",htotal+stotal,"-",100-(100*((hsuccess+ssuccess)/float(htotal+stotal))),"% Error"


  elif os.path.isdir(sys.argv[2]):
      # predict all files in folder
      for f in glob.glob(sys.argv[2]+'/*'):
          print f, ':', p.predict(f)
  elif os.path.isfile(sys.argv[2]):
      # predict this file
      print sys.argv[2], ':', p.predict(sys.argv[2])
  else:
      print 'test file illegal'

else: 
  # test training data
  print "Testing Dev data"
  testDir = "ham-test"
  testfiles = glob.glob(testDir+"/*")
  print "Testing Ham:"
  hsuccess = 0
  htotal = len(testfiles)
  for testfile in testfiles:
      if not p.predict(testfile):
          hsuccess = hsuccess + 1
  print hsuccess,"of",htotal,"-",100-(100*(hsuccess/float(htotal))),"% Error"
  print "Testing Spam:"
  testDir = "spam-test"
  testfiles = glob.glob(testDir+"/*")
  ssuccess = 0
  stotal = len(testfiles)
  for testfile in testfiles:
      if p.predict(testfile):
          ssuccess = ssuccess + 1
  print ssuccess,"of",stotal,"-",100-(100*(ssuccess/float(stotal))),"% Error"
  print ""
  print "Total"
  print hsuccess+ssuccess,"of",htotal+stotal,"-",100-(100*((hsuccess+ssuccess)/float(htotal+stotal))),"% Error"
