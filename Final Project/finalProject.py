from Perceptron import Perceptron as MyPerceptron
from finalProjectUtilityFunctions import *
from sklearn.linear_model import Perceptron as SkPerceptron
import pandas
import itertools

trainingSet, testingSet = getDataSets()

# create a data frame to hold the predictions
frame = pandas.DataFrame(columns=['state', 'label', 'features'])

for index, value in enumerate(testingSet):
    frame.loc[index] = [value['state'], value['label'], value['features']]

# get the unique features and their frequencies
features = pandas.Series(list(itertools.chain(*[t['features'] for t in trainingSet])))
features = features.value_counts()
print 'Number of Features: %i' % features.size

# filter out features that occur less than a given number of times to prevent memory issues
threshold = 6
features = features[features >= threshold]
print 'Number of Features after Filtering: %i' % features.size
print '\n'

# make features vectors
print 'Building training vectors...'
trainingVectors = makeFeaturesVectors([t['features'] for t in trainingSet], features.index)
print 'Training vectors complete.'
print 'Building testing vectors...'
testingVectors = makeFeaturesVectors([t['features'] for t in testingSet], features.index)
print 'Testing vectors complete.'
print '\n'

# train my implementaion of the Perceptron
print 'Training my perceptron...'
myPerceptron = MyPerceptron(numClasses=2, epochs=10, learningRate=1.5)
myPerceptron.train(trainingVectors, [t['label'] for t in trainingSet])
print 'My perceptron trained.'
print '\n'

# get the predictions for my Perceptron
print 'Predicting results for my Perceptron...'
frame['myPerceptron'] = pandas.Series(
    [myPerceptron.predict(testingVectors[i, :]) for i in xrange(testingVectors.shape[0])])

# display results for class 0 - liberal
print '\nResults for the implemented multinomial perceptron for class 0:\n'
printAccuracyPrecisionRecallF1(*computeAccuracyPrecisionRecallF1(
    *computeTrueFalsePostivesNegatives(frame['label'], frame['myPerceptron'], desiredClass=0)))

# display results for class 1 - conservative
print '\nResults for the implemented multinomial perceptron for class 1:\n'
printAccuracyPrecisionRecallF1(*computeAccuracyPrecisionRecallF1(
    *computeTrueFalsePostivesNegatives(frame['label'], frame['myPerceptron'], desiredClass=1)))

print '\n'

# now do the same thing, but with the sklearn Perceptron
skPerceptron = SkPerceptron()
print 'Training sklearn Perceptron...'
skPerceptron.fit(trainingVectors, [t['label'] for t in trainingSet])
print 'Sklearn Perceptron trained.'
print '\n'
print 'Predicting results for sklearn Perceptron...'
frame['skPerceptron'] = skPerceptron.predict(testingVectors)

# display results for class 0 - liberal
print '\nResults for the sklearn perceptron for class 0:\n'
printAccuracyPrecisionRecallF1(*computeAccuracyPrecisionRecallF1(
    *computeTrueFalsePostivesNegatives(frame['label'], frame['skPerceptron'], desiredClass=0)))

# display results for class 1 - conservative
print '\nResults for the sklearn perceptron for class 1:\n'
printAccuracyPrecisionRecallF1(*computeAccuracyPrecisionRecallF1(
    *computeTrueFalsePostivesNegatives(frame['label'], frame['skPerceptron'], desiredClass=1)))