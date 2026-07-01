import pandas as pd

# Popular mobile apps
app_data = {
  'app_name': [
    'YouTube', 'TikTok', 'Instagram', 'Spotify', 'Duolingo', 
    'Twitter', 'Headspace', 'Discord', 'Depop'
  ],
  'category': [
    'Video', 'Social Media', 'Social Media', 'Music', 'Education',
    'Social Media', 'Health', 'Communication', 'Shopping'
  ],
  'rating': [
    4.7, 4.6, 4.5, 4.6, 4.7,
    4.3, None, 4.7, 4.4
  ],
  'downloads_millions': [
    5000, 3000, 3500, 2000, None,
    1500, 500, 600, 200
  ]
}

# Create the DataFrame
apps = pd.DataFrame(app_data)


## View Rows with .head() and .tail()
# View the first 5 rows of the DataFrame    
"""
apps.head()     # Displays the first 5 rows
apps.tail()     # Displays the last 5 rows
"""

# apps.head(10)   # Displays the first 10 rows

# df.info() - quick summary of the DataFrame, including the number of non-null entries and data types for each column

# df.describe() - provides summary statistics for numerical columns, including count, mean, std, min, 25%, 50%, 75%, and max values

# df.describe(include='all') - includes summary statistics for non-numeric columns as well

"""
We've created a DataFrame named apps that contains (fictional) data about popular apps:

Call .head() or .tail() to see only the start or end of the DataFrame.
Call .info(). Are there any missing values?
Call .describe(). What is the average number of downloads?

"""


# Sorting DataFrames with .sort_values()
# Sort the DataFrame by the 'rating' column in descending order
apps.sort_values('rating', ascending=False)

# Rename columns with .rename()
# Rename the 'downloads_millions' column to 'downloads' 
apps_renamed = apps.rename(columns={'downloads_millions': 'downloads'})

# Adding Columns with .assign()
# Add a new column 'popularity' based on the number of downloads
apps_with_popularity = apps.assign(popularity=apps['downloads_millions'] / apps['downloads_millions'].max() * 100)