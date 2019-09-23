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
# # Dynamic Allocation
#
# We really don't save money this way (defined amounts every month). In reality we would be better to set up a budget and allocate any leftover money to savings that is above and beyond our spending habits.

# %%
import pandas as pd
import datetime

# %%
me = { 
    'biweekly_income': 2500,
    'expected_raise_pct': 0.05,
    'salary_cap_pct': 0.30,
    'biweekly_spend': 1500,
    'monthly_rent': 1627
}

# %%
accounts_definition = [
    {
        'name':'chequing',
        'rate': 0.05*0.01,
        'starting_balance': 2000,
        'max_value': 5000, #hold at this value,
        'biweekly_contribution':50,
    },
    {
        'name':'tfsa',
        'registered':True,
        'rate': 5*0.01,
        'starting_balance': 20000,
        'biweekly_contribution': 300,
        'contribution_room': 27000,
        'yearly_contrib': 5000 # contrib room added each year
    },
    {
        'name':'rrsp',
        'registered':True,
        'rate': 5*0.01,
        'starting_balance': 0,
        'biweekly_contribution': 0,
        'max_value': 35000 #for first-time home buy
    },
    {
        'name':'high_interest_savings',
        'rate': 2*0.01,
        'starting_balance': 2000,
        'max_value': 20000, #hold at this value
        'biweekly_contribution':300
    }
]

# %%
unregistered = {
        'name':'unregistered',
        'rate': 3*0.01,
        'starting_balance': 0,
    }

# %%
BW = 3 * 26 # years in 2-week chunks 

# %%
#initialize accounts
accounts = {'name':account['name'] for account in accounts_definition}

# %% [markdown]
# ## Income
#
# Pure salary income, with option for it to grow annualy

# %%
income = pd.np.ones(BW)*me.get("biweekly_income")
for year in range(BW//26):
    if me.get("salary_cap_pct") and (1 + me.get("salary_cap_pct")) * me.get("biweekly_income") < income[year*26]:
        break
    else:
        income[year*26:]*= 1 + me.get("expected_raise_pct",0)

# %% [markdown]
# ## Distribution
#
# How is this distributed to the accounts

# %%
unregistered_balance = pd.np.ones(BW)*unregistered.get('starting_balance',0)
unregsitered_rate = unregistered.get('rate',0)

# %% [markdown]
# go through time, do all accounts each step

# %%
spending = pd.np.ones(BW) * me.get("biweekly_spend",0)
rent = pd.np.ones(BW) * me.get("monthly_rent",0) * 12/26 # biweekly rent?

income -= spending + rent # this is our takehome

invest = sum(acct.get("biweekly_contribution", 0) for acct in accounts_definition)# amount invested biweekly

for account in accounts_definition:
    amount = account.get("biweekly_contribution",0)/invest
    account['ratio'] = amount

# %% [markdown]
# ### Rules for distribution
#
# - Try to follow the user inputs, split up money based on ratio between monthly contribs
# - When all the *investment* accounts are full, fill up the *unregistered* account
# - Stop filling RRSP once it's above the 1st time homebuyer amount (would be better to stop before this happens, but ...)

# %%
accts = []
for account in accounts_definition:
    balance = pd.np.ones(BW)*account['starting_balance']
    contribution = pd.np.zeros(BW)
    interest = pd.np.zeros(BW)
    notes = [""]*BW
    
    contrib_room = account.get('contribution_room',pd.np.inf)
    
    for m in range(BW-1): # project forward
        amount = account.get("ratio") * income[m]
        # monthly contributions
        if balance[m] < account.get('max_value',pd.np.inf) and contribution.sum() < contrib_room :
            contribution[m] += amount
            balance[m:] += amount
        else: # add to another account (just unregistered for now)
            notes[m]= "Contrib Limit"
            unregistered_balance[m:] += amount
        interest[m] = balance[m] * account['rate']/26
        balance[m+1:] += interest[m]
        if m and m%26 == 0: # Yearly
            contrib_room += account.get('yearly_contrib', 0)
            if not account.get('registered'):
                notes[m+1] = "Taxes!"
                balance[m+1] -= sum(interest[m-26:m]) * 0.4 # TODO: what's capital gains tax?
    accts += [pd.DataFrame({'acct':account['name'],'note':notes,'interest':interest,'balance':balance,'biweek':pd.np.arange(len(interest))})]

# %% [markdown]
# ### Do the unregistered account

# %%
interest = pd.np.zeros(BW)
balance = unregistered_balance
account = unregistered
notes = [""]*BW
for m in range(BW-1): # project forward
    # monthly contributions
    interest[m] = balance[m] * unregistered['rate']/26
    balance[m+1:] += interest[m]
    if m and m%26 == 0: # TAXES
        notes[m+1] = "Taxes!"
        balance[m+1] -= sum(interest[m-26:m]) * 0.3 # TODO: what's capital gains tax?
accts += [pd.DataFrame({'acct':account['name'],'interest':interest,'balance':balance,'biweek':pd.np.arange(len(interest))})]

# %%
cfs = pd.concat(accts, sort=False)

import dateutil
def add_weeks(save_df):
    save_df.index.name = 'biweek'
    save_df['date'] = [datetime.date.today() + dateutil.relativedelta.relativedelta(weeks=int(2*m)) for m in save_df.index.values]

add_weeks(cfs)

total = cfs.groupby("date", as_index=False)['balance'].sum()
total['acct'] = "total"
cfs = pd.concat([cfs,total], sort=False)

# %%
import plotly.express as px
px.line(cfs, x="date", y="balance", color="acct", title = "Your Savings At Work!")
