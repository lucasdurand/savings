# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Saving for the future
#
# https://trello.com/b/kwOptFGf/home-savings-estimation-tool

# %% [markdown]
# ## Simple
#
# - Current savings
# - Goal
# - How long?

# %%
# annual rate, compounded monthly
annual_rate = 0.05*0.01 # assume TD Savings Account
monthly_rate = annual_rate/12 # assume TD Savings Account

# %% [markdown]
# Silly calculation

# %%
current_savings = 10000
savings = [current_savings]
goal = 1e5

interest = [0]
while savings[-1] < goal and len(interest)/12 < 1000:
    interest.append(savings[-1]*monthly_rate)
    savings += [savings[-1]+interest[-1]]

# %%
print(len(interest)/12, " years")

# %% [markdown]
# # Multiple Accounts

# %%
accounts_definition = [
    {
        'name':'basic',
        'rate': 0.05*0.01,
        'starting_balance': 2000,
        'monthly_contribution': 0,
        'max_value': 10000 #hold at this value
    },
    {
        'name':'tfsa',
        'rate': 3*0.01,
        'starting_balance': 20000,
        'monthly_contribution': 250,
        'contribution_room': 27000,
    },
    {
        'name':'rrsp',
        'rate': 3*0.01,
        'starting_balance': 0,
        'monthly_contribution': 50,
        'max_value': 35000 #for first-time home buy
    },
    {
        'name':'high_interest_savings',
        'rate': 1*0.01,
        'starting_balance': 5000,
        'max_value': 50000 #hold at this value
    }
]

# %%
unregistered = {
        'name':'unregistered',
        'rate': 3*0.01,
        'starting_balance': 0,
    }

# %%
M = 50 * 12 # 50 years in months

# %%
#initialize accounts
accounts = [{'name':account['name'] for account in accounts_definition}]

# %% [markdown]
# ## project cashflows

# %%
unregistered_balance = pd.np.ones(M)*unregistered.get('starting_balance',0)
unregsitered_rate = unregistered.get('rate',0)

# %%
accts = []
for account in accounts_definition:
    balance = pd.np.ones(M)*account['starting_balance']
    interest = pd.np.zeros(M)
    
    monthly_contrib = account.get('monthly_contribution',0)
    contrib_room = account.get('contribution_room',pd.np.inf)
    for m in range(M-1): # project forward
        # monthly contributions
        if balance[m] < account.get('max_value',pd.np.inf) and monthly_contrib*m < contrib_room :
            balance[m:] += monthly_contrib
        else: # add to another account (just unregistered for now)
            unregistered_balance[m:] += monthly_contrib
        interest[m] = balance[m] * account['rate']/12
        balance[m+1:] += interest[m]
    accts += [pd.DataFrame({'acct':account['name'],'interest':interest,'balance':balance,'month':pd.np.arange(len(interest))})]

# %% [markdown]
# ### Do the unregistered account

# %%
interest = pd.np.zeros(M)
balance = unregistered_balance
account = unregistered
for m in range(M-1): # project forward
    # monthly contributions
    interest[m] = balance[m] * unregistered['rate']/12
    balance[m+1:] += interest[m]
    if m and m%12 == 0: # TAXES
        balance[m+1] -= sum(interest[m-12:m]) * 0.3 # TODO: what's capital gains tax?
accts += [pd.DataFrame({'acct':account['name'],'interest':interest,'balance':balance,'month':pd.np.arange(len(interest))})]

# %%
cfs = pd.concat(accts)


# %%
def add_months(save_df):
    save_df.index.name = 'month'
    save_df['date'] = [datetime.date.today() + dateutil.relativedelta.relativedelta(months=m) for m in save_df.index.values]

add_months(cfs)

cfs_by_acct = cfs.pivot(index='date', columns='acct', values='balance')

# %%
#cfs_by_acct.iplot(title='Your Savings At Work!', kind='area', fill='tonexty')

# %%
cfs_by_acct.iplot(title='Your Savings At Work!')

# %% [markdown]
# # Visualize

# %%
import dateutil.relativedelta

import pandas as pd
import cufflinks as cf
cf.go_offline()

import datetime

# %%
dates = [datetime.date.today() + dateutil.relativedelta.relativedelta(months=m) for m in range(50*12)]

# %%
save_df = pd.DataFrame({'savings':savings,'interest':interest})
def add_months(save_df):
    save_df.index.name = 'month'
    save_df['date'] = [datetime.date.today() + dateutil.relativedelta.relativedelta(months=m) for m in save_df.index.values]


# %%
save_df.iplot(x='date',y='savings', secondary_y='interest', title='TD Savings Accounts Work!')

# %%
