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

# %%
import pandas as pd
import plotly.express as px
import datetime


# %%
me = { 
    'biweekly_income': 2500,
    'expected_raise_pct': 0.05,
    'salary_cap_pct': 0.30,
    'biweekly_spend': 1500,
    'monthly_rent': 1627
}

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

unregistered = {
        'name':'unregistered',
        'rate': 3*0.01,
        'starting_balance': 0,
    }

BW = 3 * 26 # years in 2-week chunks 

## Income

#Pure salary income, with option for it to grow annualy

income = pd.np.ones(BW)*me.get("biweekly_income")
for year in range(BW//26):
    if me.get("salary_cap_pct") and (1 + me.get("salary_cap_pct")) * me.get("biweekly_income") < income[year*26]:
        break
    else:
        income[year*26:]*= 1 + me.get("expected_raise_pct",0)

unregistered_balance = pd.np.ones(BW)*unregistered.get('starting_balance',0)

spending = pd.np.ones(BW) * me.get("biweekly_spend",0)
rent = pd.np.ones(BW) * me.get("monthly_rent",0) * 12/26 # biweekly rent?

income -= spending + rent # this is our takehome

invest = sum(acct.get("biweekly_contribution", 0) for acct in accounts_definition)# amount invested biweekly

for account in accounts_definition:
    amount = account.get("biweekly_contribution",0)/invest
    account['ratio'] = amount

### Rules for distribution
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

### Do the unregistered account

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

cfs = pd.concat(accts, sort=False)

import dateutil
def add_weeks(save_df):
    save_df.index.name = 'biweek'
    save_df['date'] = [datetime.date.today() + dateutil.relativedelta.relativedelta(weeks=int(2*m)) for m in save_df.index.values]

add_weeks(cfs)

#total = cfs.groupby("date", as_index=False)['balance'].sum()
#total['acct'] = "total"
#cfs = pd.concat([cfs,total], sort=False)

import plotly.express as px
graph = px.area(cfs, x="date", y="balance", color="acct", title = "Your Savings At Work!")
graph

# %% [markdown]
# # Dynamic Allocation
#
# We really don't save money this way (defined amounts every month). In reality we would be better to set up a budget and allocate any leftover money to savings that is above and beyond our spending habits.

# %%
import pandas as pd
import plotly.express as px
import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)
app.title = "Savings"

# %% {"code_folding": [116]}
acct_info = html.Div(
    [
        html.Div([
            html.H4(
                "Savings"
            ),
                html.P(
                    "Contribution Weight",
                    className="control_label"
                ),
                dcc.Input(
                    id='hi-contrib',
                    type="number",
                    placeholder="contribution weight",
                    className="dcc_control"
                ),
                html.P(
                    "Expected Return",
                    className="control_label"
                ),
                dcc.Input(
                    id="hi-interest",
                    type="number",
                    value=2,
                    placeholder="interest (%)",
                    className="dcc_control"
                ),
                html.P(
                    "Starting Value",
                    className="control_label"
                ),
                dcc.Input(
                    id='hi-contrib-weight',
                    type="number",
                    placeholder="contribution weight",
                    className="dcc_control"
                ),                 
                html.P(
                    "End Value",
                    className="control_label"
                ),
                dcc.Input(
                    id='hi-limit',
                    type="number",
                    placeholder="hold the value here",
                    className="dcc_control"
                ),
        ], className="one-third column"),
        html.Div([

            html.H4(
                "TFSA"
            ),
                html.P(
                    "Contribution Weight",
                    className="control_label"
                ),
                dcc.Input(
                    id='tfsa-contrib',
                    type="number",
                    placeholder="contribution weight",
                    className="dcc_control"
                ),
                html.P(
                    "Expected Return",
                    className="control_label"
                ),
                dcc.Input(
                    id="tfsa-interest",
                    type="number",
                    placeholder="interest (%)",
                    className="dcc_control"
                ),
                html.P(
                    "Starting Value",
                    className="control_label"
                ),
                dcc.Input(
                    id='tfsa-contrib-weight',
                    type="number",
                    placeholder="contribution weight",
                    className="dcc_control"
                ),                 
                html.P(
                    "End Value",
                    className="control_label"
                ),
                dcc.Input(
                    id="tfsa-limit",
                    type="number",
                    placeholder="hold the value here",
                    className="dcc_control"
                ),
                html.P(
                    "Contribution Room",
                    className="control_label"
                ),
                dcc.Input(
                    id="tfsa-contrib-room",
                    type="number",
                    placeholder="current room",
                    className="dcc_control"
                ),
                html.P(
                    "Contribution Reset",
                    className="control_label"
                ),
                dcc.Input(
                    id="tfsa-contrib-reset",
                    type="number",
                    value=5000,
                    placeholder="added room each year",
                    className="dcc_control"
                ),

        ], className="one-third column"),
        html.Div(children=[

            html.H4(
                "RRSP"
            ),
                html.P(
                    "Contribution Weight",
                    className="control_label"
                ),
                dcc.Input(
                    id='rrsp-contrib',
                    type="number",
                    placeholder="contribution weight",
                    className="dcc_control"
                ),
                html.P(
                    "Expected Return",
                    className="control_label"
                ),
                dcc.Input(
                    id="rrsp-interest",
                    type="number",
                    placeholder="interest (%)",
                    className="dcc_control"
                ),                                    
                html.P(
                    "Starting Value",
                    className="control_label"
                ),
                dcc.Input(
                    id='rrsp-contrib-weight',
                    type="number",
                    placeholder="contribution weight",
                    className="dcc_control"
                ),                 
                html.P(
                    "End Value",
                    className="control_label"
                ),
                dcc.Input(
                    id="rrsp-limit",
                    type="number",
                    value=35000,
                    placeholder="hold the value here",
                    className="dcc_control"
                ),
                html.P(
                    "Contribution Room",
                    className="control_label"
                ),
                dcc.Input(
                    id="rrsp-contrib-room",
                    type="number",
                    value=26500,
                    placeholder="current room",
                    className="dcc_control"
                ),
                html.P(
                    "Contribution Reset",
                    className="control_label"
                ),
                dcc.Input(
                    id="rrsp-contrib-reset",
                    type="number",
                    value=26500,
                    placeholder="added room each year",
                    className="dcc_control"
                ),
        ], className="one-third column"),
    ],
    style={"padding-top":"20px"}
)

# %%
main_view = dcc.Tabs(
    [
        dcc.Tab(label="Accounts", children=[
            acct_info
        ]),
        dcc.Tab(label="Savings", children=[
            html.Div(
                [
                    dcc.Graph(
                        id='savings_graph',
                        figure=graph                                
                    )
                ],
                id="countGraphContainer",

                style={"minHeight":"400px"}
            )
        ])
    ],
    id="input-tabs",
)

# %%
summary_stats = [
    html.Div(
        [
            html.P("Total Saved"),
            html.H6(
                id="total-saved",
                className="info_text",
                children=["$0"]
            )
        ],
        id="total-summary",
        className="pretty_container",
        style={"flex":"4"}
    ),

    html.Div(
        [
            html.P("Savings"),
            html.H6(
                id="total-hi-savings",
                className="info_text",
                children=["$0"]
            )
        ],
        id="hi-summary",
        className="pretty_container",
        style={"flex":"4"}
    ),
    html.Div(
        [
            html.P("TFSA"),
            html.H6(
                id="total-tfsa-savings",
                className="info_text",
                children=["$0"]
            )
        ],
        id="tfsa-summary",
        className="pretty_container",
        style={"flex":"4"}
    ),
    html.Div(
        [
            html.P("RRSP"),
            html.H6(
                id="total-rrsp-savings",
                className="info_text",
                children=["$0"]
            )
        ],
        id="rrsp-summary",
        className="pretty_container",
        style={"flex":"4"}
    ),
]

# %% {"code_folding": [3, 89, 102, 114, 126]}
# Create app layout
app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            'When can I buy that house?',

                        ),
                        html.H4(
                            'Investment Calculator',
                        )
                    ],

                    className='eight columns'
                ),
            ],
            id="header",
            className='row',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H3("A little about you:"),
                        html.P(
                            "How much is a paycheck?",
                            className="control_label"
                        ),
                        dcc.Input(
                            id='biweekly_income',
                            type="number",
                            placeholder="biweekly income",
                            className="dcc_control"
                        ),
                        html.P(
                            'How much will that grow each year(%)?',
                            className="control_label"
                        ),
                        dcc.Input(
                            id='expected_raise_pct',
                            type="number",
                            placeholder="percentage growth (%)",
                            className="dcc_control"
                        ),
                        html.P(
                            'Is there a max(%)?',
                            className="control_label"
                        ),
                        dcc.Input(
                            id='salary_cap_pct',
                            type="number",
                            placeholder="salary cap (%)",
                            className="dcc_control"
                        ),

                        html.P(
                            'How much do you spend per paycheck?',
                            className="control_label"
                        ),
                        dcc.Input(
                            id='biweekly_speed',
                            type="number",
                            placeholder="biweekly spend ($)",
                            className="dcc_control"
                        ),

                        html.P(
                            "And what's rent every month?",
                            className="control_label"
                        ),
                        dcc.Input(
                            id='monthly_rent',
                            type="number",
                            placeholder="monthly rent ($)",
                            className="dcc_control"
                        ),
                        html.H6(
                                "We are going to invest all of your unspent money each month. Where it ends up depends on some limits and weights you define below."
                        ),                 
                    ],
                    className="pretty_container four columns"
                ),
                html.Div(
                    [
                        html.Div(
                            summary_stats,
                            id="infoContainer",
                            className="row"
                        ),
                        html.Div(className="pretty_container", children=
                             [
                                main_view
                             ]
                        )
                    ],
                    id="rightCol",
                    className="eight columns"
                )
            ],
            className="row",
            style={"display":"flex","flex":3}
        )],
   id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
)

# %% [markdown]
# ## Callbacks
#
# We made the wireframe, but now here's the hard part.
#
# We want to update the graph whenever:
#
# - Value on the left is changed (personal info)
# - Clicked onto the "savings" tab
#
# We also want to make it easier(/obvious) to switch to the "Savings" tab to view the results. MAYBE IT SHOULD BE CALLED RESULTS?
