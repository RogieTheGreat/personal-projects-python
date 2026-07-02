import pandas as pd

data = {
  'street': [
    '5230 Newell Road',
    '1381 9th Avenue',
    '1709 Broderick St',
    '2640 Steiner St',
    '2601 Lyon St',
    '1600 Amphitheatre Parkway',
    '7500 N Glenoaks Boulevard',
    '4501 Glencoe Avenue',
    '232 Santa Margarita Ave',
    '471 Emerson Street'
  ],
  'city': [
    'Palo Alto',
    'San Francisco',
    'San Francisco',
    'San Francisco',
    'San Francisco',
    'Mountain View',
    'Burbank',
    'Marina del Rey',
    'Menlo Park',
    None
  ],
  'state': [
    'CA',
    'CA',
    'CA',
    'CA',
    'CA',
    'CA',
    'CA',
    'CA',
    None,
    None
  ],
  'zip_code': [
    94303,
    94122,
    94115,
    94123,
    94123,
    94043,
    91504,
    90292,
    94025,
    None
  ],
  'delivery_type': [
    'First Class',
    'Standard',
    'Priority',
    'Standard',
    None,
    'Expresss',
    'Standard',
    'Standard',
    None,
    None
  ]
}

addresses = pd.DataFrame(data)

addresses.info()
