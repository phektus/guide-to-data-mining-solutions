# coding=utf-8
import math

def manhattan(rating1, rating2):
  """Computes the Manhattan distance. Both rating1 and rating2 are dictionaries
  of the form {'The Strokes': 3.0, 'Slightly Stoopid': 2.5}"""
  distance = 0
  total = 0
  for key in rating1:
    if key in rating2:
      distance += abs(rating1[key] - rating2[key])
      total += distance
    if total > 0:
      return distance / total
  else:
    return -1 #Indicates no ratings in common


def euclidean(rating1, rating2):
  """Computes the Euclidean distance, which is the straight
  line distance between two points on a plane. Both rating1 and rating2 are dictionaries
  of the form {'The Strokes': 3.0, 'Slightly Stoopid': 2.5}"""
  distance = 0
  commonRatings = False
  for key in rating1:
    if key in rating2:
      distance += (rating1[key]-rating2[key])**2
      commonRatings = True
    if commonRatings:
      return math.sqrt(distance)
  else:
    return -1 #Indicates no ratings in common


def minkowski(rating1, rating2, level=2):
  """Computes the Minkowski distance, which is a generalized form
  for the Manhattan (level 1) and Euclidean (level 2) distances.
  Both rating1 and rating2 are dictionaries
  of the form {'The Strokes': 3.0, 'Slightly Stoopid': 2.5}"""
  distances = []
  for key in rating1:
    if key in rating2:
      distance = math.pow(abs(rating1[key] - rating2[key]), level)
      distances.append(distance)
  if len(distances) > 0:
    return math.pow(sum(distances), 1/level)
  else:
    return -1 #Indicates no ratings in common


def computeNearestNeighbor(username, users):
  """creates a sorted list of users based on their distance to username"""
  distances = []
  for user in users:
    if user != username:
      distance = minkowski(users[user], users[username], 1)
      distances.append((distance, user))
  # sort based on distance -- closest first
  distances.sort()
  return distances


def recommend(username, users):
  """Give list of recommendations"""
  # first find nearest neighbor
  nearest = computeNearestNeighbor(username, users)[0][1]
  recommendations = []

  # now find bands neighbor rated that user didn't
  neighborRatings = users[nearest]
  userRatings = users[username]

  for artist in neighborRatings:
    if not artist in userRatings:
      recommendations.append((artist, neighborRatings[artist]))
      recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse = True)
  return recommendations


def pearson(rating1, rating2):
  """Determines the Pearson coefficient for two ratings"""
  n = sum([1.0 for key in rating1 if key in rating2])
  x_sum = sum([rating1[x] for x in rating1 if x in rating2])
  y_sum = sum([rating2[y] for y in rating2 if y in rating1])
  x_squares_sum = sum([math.pow(rating1[x],2.0) for x in rating1 if x in rating2])
  y_squares_sum = sum([math.pow(rating2[y],2.0) for y in rating2 if y in rating1])
  
  a = sum([(rating1[key] * rating2[key]) for key in rating1 if key in rating2])
  b = (x_sum * y_sum) / n
  c = math.sqrt(x_squares_sum - (math.pow(x_sum, 2.0) / n))
  d = math.sqrt(y_squares_sum - (math.pow(y_sum, 2.0) / n))

  if c*d == 0:
    total = 0
  else:
    total = (a - b) / (c * d)

  return total
  


def test():

  users = {
  "Angelica": {
    "Blues Traveler": 3.5, 
    "Broken Bells": 2.0,
    "Norah Jones": 4.5, 
    "Phoenix": 5.0, 
    "Slightly Stoopid": 1.5,
    "The Strokes": 2.5, 
    "Vampire Weekend": 2.0
  }, "Bill": {
    "Blues Traveler": 2.0, 
    "Broken Bells": 3.5, 
    "Deadmau5": 4.0,
    "Phoenix": 2.0, 
    "Slightly Stoopid": 3.5,
    "Vampire Weekend": 3.0
  }, "Chan": {
    "Blues Traveler": 5.0, 
    "Broken Bells": 1.0, 
    "Deadmau5": 1.0,
    "Norah Jones": 3.0, 
    "Phoenix": 5, 
    "Slightly Stoopid": 1.0
  }, "Dan":  {
    "Blues Traveler": 3.0, 
    "Broken Bells": 4.0, 
    "Deadmau5": 4.5,
    "Phoenix": 3.0, 
    "Slightly Stoopid": 4.5, 
    "The Strokes": 4.0,
    "Vampire Weekend": 2.0
  }, "Hailey": {
    "Broken Bells": 4.0, 
    "Deadmau5": 1.0, 
    "Norah Jones": 4.0,
    "The Strokes": 4.0, 
    "Vampire Weekend": 1.0
  }, "Jordyn": {
    "Broken Bells": 4.5, 
    "Deadmau5": 4.0, 
    "Norah Jones": 5.0,
    "Phoenix": 5.0, 
    "Slightly Stoopid": 4.5, 
    "The Strokes": 4.0,
    "Vampire Weekend": 4.0
  }, "Sam": {
    "Blues Traveler": 5.0, 
    "Broken Bells": 2.0,
    "Norah Jones": 3.0, 
    "Phoenix": 5.0, 
    "Slightly Stoopid": 4.0,
    "The Strokes": 5.0
  }, "Veronica": {
    "Blues Traveler": 3.0, 
    "Norah Jones": 5.0, 
    "Phoenix": 4.0,
    "Slightly Stoopid": 2.5, 
    "The Strokes": 3.0
  }}

  print 'Testing Manhattan'
  assert(manhattan(users['Hailey'], users['Veronica']) == 2.0)
  print 'Testing Pearson'
  assert(pearson(users['Angelica'], users['Bill']) == -0.90405349906826993)
  assert(pearson(users['Angelica'], users['Hailey']) == 0.42008402520840293)
  assert(pearson(users['Angelica'], users['Jordyn']) == 0.76397486054754316)
  print 'Testing Pearson: PASS'

if __name__ == '__main__':
  test()
