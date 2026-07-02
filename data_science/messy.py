import pandas as pd

data = {
  'username': [
    '@sonny',
    '@asiqur',
    '@jackieisonline',
    '@naomixlee',
    '@julien',
    '@asiqur',                  # duplicate test account
    '@gabtot',
    '@bot',
    '@bot'                      # duplicate
  ],    
  'location': [
    'Brooklyn, NY',
    'Brooklyn, NY',
    'Brooklyn',
    'brooklyn',                 # lowercase
    'Brooklyn, NY',       
    None,                       # missing
    'nyc 🗽 no longer :(',      # i don't even know
    'NEW YORK!!!',              # uppercase punctuation
    ''                          # empty string = missing
  ],
  'age': [
    35,
    24,
    None,                       # missing
    '24',                       # wrong data type
    30,                    
    0,                          # hmmm
    67,                         # troll number
    None,                       # missing
    None                        # missing
  ], 
  'instagram': [
    'sonnynomnom.io',
    'instagram.com/asiqur.dev', # inconsistent entry
    '',
    None,                       # missing
    None,                       # missing
    '',
    'bybanaag',
    '',
    None                        # missing
  ]
}

users = pd.DataFrame(data)


# Show data types and non-null counts for the original DataFrame
print('Original DataFrame:')
print(users)
print()
# The printed DataFrame contains nine rows with mixed types and missing values.
# Example: one location is None, one age is a string, and one Instagram handle is blank.

print('DataFrame info:')
users.info()
print()
# This summary shows column data types, non-null counts, and whether there are missing values.

# Remove rows with any missing values
cleaned_df = users.dropna()
print('Rows with no missing values (dropna):')
print(cleaned_df)
print()
# Result: only rows where every column is filled remain.
# In this dataset, rows with any None or blank entries are removed.

# Remove rows missing username or location only
cleaned_subset = users.dropna(subset=['username', 'location'])
print('Rows with username and location only:')
print(cleaned_subset)
print()
# Result: rows missing only the username or location are removed,
# but rows with missing age or instagram are retained.

# Find the most common location and fill missing missing locations with it
most_common_location = users['location'].mode()[0]
print('Most common location:', most_common_location)
users['location'] = users['location'].fillna(most_common_location)
print('After filling missing locations:')
print(users)
print()
# Result: the None value in location is replaced with the most frequent location.
# Note that empty strings remain unchanged and are not treated as missing by fillna.

# Show duplicate row flags
duplicate_flags = users.duplicated()
print('Duplicate row flags:')
print(duplicate_flags)
print()
# Result: a boolean Series marking duplicate rows based on all columns.

# Show the actual duplicate rows
print('Duplicate rows:')
print(users[duplicate_flags])
print()
# Result: rows flagged True are exact duplicates of earlier rows.

# Drop duplicate rows and show final cleaned data
no_dupes = users.drop_duplicates()
print('DataFrame after dropping duplicate rows:')
print(no_dupes)
# Result: the DataFrame no longer contains any duplicate rows.
