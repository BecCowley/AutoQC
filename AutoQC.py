from wodpy import wod
import glob, time
import numpy as np
import sys, os, json
import util.main as main
import pandas

def run(test, profiles):
  '''
  run <test> on a list of <profiles>, return an array summarizing when exceptions were raised
  '''
  qcResults = []
  verbose = []
  exec('from qctests import ' + test)
  for profile in profiles:
    exec('result = ' + test + '.test(profile)')

    #demand tests returned bools:
    for i in result:
      assert isinstance(i, np.bool_), str(i) + ' in test result list is of type ' + str(type(i))

    qcResults.append(np.any(result))
    verbose.append(result)
  return [qcResults, verbose]

def processFile(fName):
  # run each test on each profile, and record its summary & verbose performance
  testResults  = []
  testVerbose  = []
  trueResults  = []
  trueVerbose  = []
  profileIDs   = []
  firstProfile = True
  currentFile  = ''
  f = None
  for iprofile, pinfo in enumerate(profiles):
    # Load the profile data.
    p, currentFile, f = main.profileData(pinfo, currentFile, f)
    # Check that there are temperature data in the profile, otherwise skip.
    if p.var_index() is None:
      continue
    if np.sum(p.t().mask == False) == 0:
      continue
    # Run each test.    
    for itest, test in enumerate(testNames):
      result = run(test, [p])
      if firstProfile:
        testResults.append(result[0])
        testVerbose.append(result[1])
      else:
        testResults[itest].append(result[0][0])
        testVerbose[itest].append(result[1][0])
    firstProfile = False
    # Read the reference result.
    truth = main.referenceResults([p])
    trueResults.append(truth[0][0])
    trueVerbose.append(truth[1][0])
    profileIDs.append(p.uid())
    # Update user on progress.
    sys.stdout.write('QC of profiles is {:5.1f}% complete\r'.format((iprofile+1)*100.0/len(profiles)))
    sys.stdout.flush()
  # testResults[i][j] now contains a flag indicating the exception raised by test i on profile j

  return trueResults, testResults, profileIDs


########################################
# main
########################################

# identify and import tests
testNames = main.importQC('qctests')
testNames.sort()
print('{} quality control checks have been found'.format(len(testNames)))
testNames = main.checkQCTestRequirements(testNames)
print('{} quality control checks are able to be run:'.format(len(testNames)))
for testName in testNames:
  print('  {}'.format(testName))

# identify data files and extract profile information into an array - this
# information is used by some quality control checks; the profile data are
# read later.
filenames = main.readInput('datafiles.json')
profiles  = main.extractProfiles(filenames)
print('\n{} profiles will be read\n'.format(len(profiles)))

if len(sys.argv)>2:
  nProcessed = 0
  processFile.parallel = main.parallel_function(processFile, sys.argv[2])
  parallel_result = processFile.parallel(filenames)
  #recombine results
  truth = parallel_result[0][0]
  results = parallel_result[0][1]
  profileIDs = parallel_result[0][2]
  for pr in parallel_result[1:]:
    truth      += pr[0]
    for itr, tr in enumerate(pr[1]):
      results[itr] += tr
    profileIDs += pr[2]

  # Print summary statistics and write output file.
  main.printSummary(truth, results, testNames)
  main.generateCSV(truth, results, testNames, profileIDs, sys.argv[1])
else:
  print 'Please add command line arguments to name your output file and set parallelization:'
  print 'python AutoQC myFile 4'
  print 'will result in output written to results-myFile.csv, and will run the calculation parallelized across 4 cores.'
