#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data=pd.read_csv('election_results_2024.csv')
data.head()

data['Margin'] = pd.to_numeric(data['Margin'], errors='coerce')

data = data.dropna(subset=['Margin'])


# In[3]:


bjp_data = data[data['Leading Party'] == 'Bharatiya Janata Party']
inc_data = data[data['Leading Party'] == 'Indian National Congress']


# In[4]:


def comparative_analysis(party_name, party_data):
    total_seats = party_data.shape[0]
    average_margin = party_data['Margin'].mean()
    median_margin = party_data['Margin'].median()
    close_contests = party_data[party_data['Margin'] < 5000].shape[0]
    highest_margins = party_data.nlargest(5, 'Margin')[['Constituency', 'Margin', 'Leading Candidate']]
    lowest_margins = party_data.nsmallest(5, 'Margin')[['Constituency', 'Margin', 'Leading Candidate']]
    
    return {
        'Party': party_name,
        'Total Seats': total_seats,
        'Average Margin': average_margin,
        'Median Margin': median_margin,
        'Close Contests': close_contests,
        'Top 5 Highest Margins': highest_margins,
        'Top 5 Lowest Margins': lowest_margins
    }

# Analysis for BJP
bjp_analysis = comparative_analysis('Bharatiya Janata Party', bjp_data)

# Analysis for INC
inc_analysis = comparative_analysis('Indian National Congress', inc_data)

comparison_df = pd.DataFrame({
    'Metric': ['Total Seats', 'Average Margin', 'Median Margin', 'Close Contests'],
    'BJP': [bjp_analysis['Total Seats'], bjp_analysis['Average Margin'], bjp_analysis['Median Margin'], bjp_analysis['Close Contests']],
    'INC': [inc_analysis['Total Seats'], inc_analysis['Average Margin'], inc_analysis['Median Margin'], inc_analysis['Close Contests']]
})


# In[6]:


# Plotting the comparisons
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
sns.barplot(x='Metric', y='BJP', data=comparison_df, label='BJP', color='b', alpha=0.6)
sns.barplot(x='Metric', y='INC', data=comparison_df, label='INC', color='r', alpha=0.6)
plt.title('Total Seats Won')
plt.ylabel('Number of Seats')
plt.legend()

plt.subplot(2, 2, 2)
sns.barplot(x='Metric', y='BJP', data=comparison_df, label='BJP', color='b', alpha=0.6)
sns.barplot(x='Metric', y='INC', data=comparison_df, label='INC', color='r', alpha=0.6)
plt.title('Average Margin')
plt.ylabel('Average Margin (Votes)')
plt.legend()

plt.subplot(2, 2, 3)
sns.barplot(x='Metric', y='BJP', data=comparison_df, label='BJP', color='b', alpha=0.6)
sns.barplot(x='Metric', y='INC', data=comparison_df, label='INC', color='r', alpha=0.6)
plt.title('Median Margin')
plt.ylabel('Median Margin (Votes)')
plt.legend()

plt.subplot(2, 2, 4)
sns.barplot(x='Metric', y='BJP', data=comparison_df, label='BJP', color='b', alpha=0.6)
sns.barplot(x='Metric', y='INC', data=comparison_df, label='INC', color='r', alpha=0.6)
plt.title('Close Contests (Margin < 5000)')
plt.ylabel('Number of Close Contests')
plt.legend()

plt.tight_layout()
plt.show()


# In[7]:


# Top 5 Constituencies with Highest Margins
fig, axes = plt.subplots(2, 1, figsize=(12, 10))

sns.barplot(x='Margin', y='Constituency', hue='Leading Candidate', data=bjp_analysis['Top 5 Highest Margins'], ax=axes[0])
axes[0].set_title('BJP - Top 5 Constituencies with Highest Margins')
axes[0].set_xlabel('Margin (Votes)')
axes[0].set_ylabel('Constituency')

sns.barplot(x='Margin', y='Constituency', hue='Leading Candidate', data=inc_analysis['Top 5 Highest Margins'], ax=axes[1])
axes[1].set_title('INC - Top 5 Constituencies with Highest Margins')
axes[1].set_xlabel('Margin (Votes)')
axes[1].set_ylabel('Constituency')

plt.tight_layout()
plt.show()


# In[8]:


# Top 5 Constituencies with Lowest Margins
fig, axes = plt.subplots(2, 1, figsize=(12, 10))

sns.barplot(x='Margin', y='Constituency', hue='Leading Candidate', data=bjp_analysis['Top 5 Lowest Margins'], ax=axes[0])
axes[0].set_title('BJP - Top 5 Constituencies with Lowest Margins')
axes[0].set_xlabel('Margin (Votes)')
axes[0].set_ylabel('Constituency')

sns.barplot(x='Margin', y='Constituency', hue='Leading Candidate', data=inc_analysis['Top 5 Lowest Margins'], ax=axes[1])
axes[1].set_title('INC - Top 5 Constituencies with Lowest Margins')
axes[1].set_xlabel('Margin (Votes)')
axes[1].set_ylabel('Constituency')

plt.tight_layout()
plt.show()


# In[ ]:




