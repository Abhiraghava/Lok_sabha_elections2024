#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
from bs4 import BeautifulSoup

url = "https://results.eci.gov.in/PcResultGenJune2024/ConstituencywiseS069.htm"

page = requests.get(url)

soup = BeautifulSoup(page.content,"html.parser")

results = soup.find(div = "table-responsive")


# In[6]:


print("Classes of each table:")
for table in soup.find_all('table'):
    print(table.get('class'))


# In[7]:


table = soup.find('table', class_ = 'table')


# In[9]:


state_name = soup.find("strong")
state_name.text


# In[10]:


table


# In[11]:


for election_data in table.find_all('tbody'):
    rows = election_data.find_all('tr')
    print(rows)#all the rows in the table 


# In[12]:


import pandas as pd
sr_no = []
candidate_name = []
party_name = []
evm_votes = []
postal_votes = []
total_votes = []
percent_votes = []
for row in rows: 
    sr = row.find_all('td')[0].text
    sr_no.append(sr)
    can_name = row.find_all('td')[1].text
    candidate_name.append(can_name)
    party = row.find_all('td')[2].text
    party_name.append(party)
    e_votes = row.find_all('td')[3].text
    evm_votes.append(e_votes)
    p_votes = row.find_all('td')[4].text
    postal_votes.append(p_votes)
    t_votes = row.find_all('td')[5].text
    total_votes.append(t_votes)
    per_votes = row.find_all('td')[6].text
    percent_votes.append(per_votes)
    
    data_list = [sr_no,
candidate_name,
party_name,
evm_votes,
postal_votes,
total_votes,
percent_votes]


# In[13]:


df = pd.DataFrame(data_list)

print(df)


# In[14]:


PC = soup.find('h2').text


# In[15]:


df["Constituency"] = PC 


# In[16]:


df


# In[17]:


url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"
first_page = requests.get(url)
first_soup = BeautifulSoup(first_page.content,'html.parser')


# In[18]:


option_html = first_soup.find("select", id = "ctl00_ContentPlaceHolder1_Result1_ddlState")
option_html


# In[19]:


def finding_optionValue(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    dropdown_result = soup.find("select", id = "ctl00_ContentPlaceHolder1_Result1_ddlState")
    options = dropdown_result.find_all('option')
    option_value_list = []
    for option in options:
        option_value = option.get('value')
        option_value_list.append(option_value)
    return option_value_list


# In[20]:


states_and_ut = finding_optionValue("https://results.eci.gov.in/PcResultGenJune2024/index.htm")
states_and_ut


# In[21]:


for index,element in enumerate(states_and_ut[1:]):
       url = f"https://results.eci.gov.in/PcResultGenJune2024/partywiseresult-{element}.htm"
       page = requests.get(url)
       print(index,page.status_code)


# In[23]:


assam_try = finding_optionValue("https://results.eci.gov.in/PcResultGenJune2024/partywiseresult-S03.htm")


# In[24]:


for index,element in enumerate(assam_try[1:]):
       url = f"https://results.eci.gov.in/PcResultGenJune2024/Constituencywise{element}.htm"
       page = requests.get(url)
       print(index,page.status_code)


# In[25]:


master_list = []
state_code_list = []

for elements in states_and_ut[1:]:
        url = f"https://results.eci.gov.in/PcResultGenJune2024/partywiseresult-{elements}.htm"
        pc = finding_optionValue(url)
        master_list.append(pc)


# In[26]:


master_list #this is list of list lets flatten it and remove the empty string part 


# In[27]:


#Flatten the list
flat_master = sum(master_list, [])
flat_master


# In[28]:


#for removing blank spaces
for elements in flat_master:
    if (elements == ""):
        flat_master.remove("")
        


# In[29]:


len(flat_master)#Now that we know no. of constituency is equal to len of list.


# In[30]:


def table_scrapper(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    result_table = soup.find("table")
    for body in result_table.find_all('tbody'):
        rows = body.find_all('tr')
    sr_no = []
    candidate_name = []
    party_name = []
    evm_votes = []
    postal_votes = []
    total_votes = []
    percent_votes = []
    for row in rows: 
        sr = row.find_all('td')[0].text
        sr_no.append(sr)
        can_name = row.find_all('td')[1].text
        candidate_name.append(can_name)
        party = row.find_all('td')[2].text
        party_name.append(party)
        e_votes = row.find_all('td')[3].text
        evm_votes.append(e_votes)
        p_votes = row.find_all('td')[4].text
        postal_votes.append(p_votes)
        t_votes = row.find_all('td')[5].text
        total_votes.append(t_votes)
        per_votes = row.find_all('td')[6].text
        percent_votes.append(per_votes)
        pc = soup.find('h2').text
        state_name = soup.find('strong').text
        
        
        data = {
        "Sr No": sr_no,
        "Candidate Name": candidate_name,
        "Party Name": party_name,
        "EVM Votes": evm_votes,
        "Postal Votes": postal_votes,
        "Total Votes": total_votes,
        "Percent Votes": percent_votes,
        "Constiteuncy" : pc,
        "State" : state_name
    }
    
    df = pd.DataFrame(data)
    return df


# In[31]:


table_scrapper("https://results.eci.gov.in/PcResultGenJune2024/ConstituencywiseS072.htm") #test


# In[37]:


#Making empty Dataframe with columns
df_try = pd.DataFrame(columns = ["S.N.","Candidate","Party","EVM Votes","Postal Votes","Total Votes","% of Votes","Constituency"])


# In[38]:


import pandas as pd
final_df = pd.DataFrame()
for elements in flat_master:
    url = f"https://results.eci.gov.in/PcResultGenJune2024/Constituencywise{elements}.htm"
    loop_df = table_scrapper(url)
    final_df = pd.concat([final_df,loop_df],axis = 0, ignore_index = True)


# In[39]:


final_df


# In[ ]:


final_df.nunique()#proof that it worked as constiteuncy is 543


# In[ ]:


#State Name 
final_df['State'] = final_df['State'].str.extract(r"\((.*?)\)")
final_df


# In[ ]:


new_order = ["Sr No", "State", "Constiteuncy", "Candidate Name", "Party Name", "EVM Votes", "Postal Votes", "Total Votes", "Percent Votes"]
order_df = final_df[new_order]


# In[ ]:


order_df.rename(columns = {"Constiteuncy":"Constituency"},inplace = True)


# In[ ]:


order_df


# In[ ]:


final_df["State"].value_counts()


# In[ ]:


order_df.to_csv("C:\Users\ASUS\Desktop\web_scrap.csv",index = False)


# In[ ]:




