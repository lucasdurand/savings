# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.4
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
import plotly.express as px
import datetime

from dash import Dash, dcc, html

app = Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)
app.title = "Savings"

# %% {"code_folding": [0]}
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
                    value=1,
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
                    id='hi-starting',
                    type="number",
                    placeholder="current balance",
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
            html.H4(
                "Unregistered",
                style={"padding-top":"15px"}
            ),
                html.P(
                    "Expected Return"
                ),
                dcc.Input(
                    id="unreg-interest",
                    type="number",
                    value=3,
                    placeholder="interest (%)",
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
                    id='tfsa-contrib-weight',
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
                    id='tfsa-starting',
                    type="number",
                    placeholder="current balance",
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
                    id='rrsp-starting',
                    type="number",
                    placeholder="current balance",
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

# %% {"code_folding": [0]}
main_view = dcc.Tabs(
    [
        dcc.Tab(label="Accounts", children=[
            acct_info
        ]),
        dcc.Tab(label="Savings", value="savings", children=[
            html.Div(
                [
                    dcc.Graph(
                        id='savings_graph',
                        figure=px.area(pd.DataFrame(), width=600)
                    )
                ],
                id="countGraphContainer",

                style={"minHeight":"600px"}
            )
        ])
    ],
    id="input-tabs",
)

# %% {"code_folding": [0]}
summary_stats = [
    html.Div(
        [
            html.P("Total Saved"),
            html.H6(
                id="total-saved",
                className="info_text"
            )
        ],
        className="mini_container",
        style={"flex":"4"}
    ),

    html.Div(
        [
            html.P("Avg Saved"),
            html.H6(
                id="avg-saved",
                className="info_text"
            )
        ],
        className="mini_container",
        style={"flex":"4"}
    ),
    html.Div(
        [
            html.P("Capital Gains Tax"),
            html.H6(
                id="total-tax",
                className="info_text"
            )
        ],
        className="mini_container",
        style={"flex":"4"}
    ),
    html.Div(
        [
            html.P("Rent"),
            html.H6(
                id="total-rent",
                className="info_text"
            )
        ],
        className="mini_container",
        style={"flex":"4"}
    ),
]

# %% {"code_folding": [24, 98, 103]}
# Create app layout
app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Img(
                                    src="assets/stonks.png",
                                    height=75,
                                    className="flex-display",
                                    style={"marginRight":"5px"}
                                ),
                                html.H2(
                                    'When can I buy that house?',
                                    className="flex-display",

                                ),                             
                            ],className="flex-display"),
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
                            id='biweekly_spend',
                            type="number",
                            placeholder="biweekly spend ($)",
                            className="dcc_control"
                        ),

                        html.P(
                            "What's rent every month?",
                            className="control_label"
                        ),
                        dcc.Input(
                            id='monthly_rent',
                            type="number",
                            placeholder="monthly rent ($)",
                            className="dcc_control"
                        ),
                        html.P(
                            "And how many years should be projected?",
                            className="control_label"
                        ),
                        dcc.Input(
                            id='projected_years',
                            type="number",
                            placeholder="years",
                            className="dcc_control"
                        ),
                        html.H6(

                            "We are going to invest all of your unspent money each month. Where it ends up depends on some limits and weights you define under 'Accounts'."
                        ),                 
                    ],
                    className="pretty_container four columns"
                ),
                html.Div(
                    [
                        html.Div(
                            summary_stats,
                            id="info-container",
                            className="row container-display"
                        ),
                        html.Div(className="pretty_container", children=
                             [
                                main_view
                             ]
                        )
                    ],
                    id="right-column",
                    className="eight columns"
                )
            ],
            className="row flex-display",
        )],
   id="mainContainer"
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

# %%
from dash import Output, Input, State

# %%
personal_info_inputs = [
    Input("biweekly_income","value"),
    Input("expected_raise_pct","value"),
    Input("salary_cap_pct","value"),
    Input("biweekly_spend","value"),
    Input("monthly_rent","value"),
    Input("projected_years","value")
]

# %%
acct_info_ids = [child.id for kid in acct_info.children for child in kid.children if type(child)==dcc.Input]

account_info_inputs = [ State(component_id,"value") for component_id in acct_info_ids]

# %% {"code_folding": [0, 17, 26, 29, 37, 67]}
@app.callback(
    [
        Output(component_id="savings_graph", component_property="figure"),
        Output(component_id="total-saved", component_property="children"),
        Output(component_id="avg-saved", component_property="children"),
        Output(component_id="total-tax", component_property="children"),
        Output(component_id="total-rent", component_property="children"),
    ],
    [
        *personal_info_inputs,
        Input(component_id="input-tabs", component_property="value")
    ],
    [
        *account_info_inputs,
        State(component_id="savings_graph", component_property="figure")
    ]
)
def calculate_cashflows(
    biweekly_income,expected_raise_pct,salary_cap_pct,biweekly_spend,monthly_rent,projected_years,
    tab,
    hi_contrib,hi_interest,hi_starting,hi_limit, unreg_interest,
    tfsa_contrib,tfsa_interest,tfsa_starting,tfsa_limit,tfsa_contrib_room,tfsa_contrib_reset,
    rrsp_contrib,rrsp_interest,rrsp_starting,rrsp_limit,rrsp_contrib_room,rrsp_contrib_reset,
    figure
):
    
    #if tab != "savings": 
    #    return [figure, "$—", "$—", "$—", "$—"]
    
    me = { 
        'biweekly_income': (biweekly_income or 0),
        'expected_raise_pct': (expected_raise_pct or 0) * 0.01,
        'salary_cap_pct': (salary_cap_pct or 0) * 0.01,
        'biweekly_spend': (biweekly_spend or 0),
        'monthly_rent': (monthly_rent or 0)
    }
    
    accounts_definition = [
        {
            'name':'tfsa',
            'registered':True,
            'rate': (tfsa_interest or 0)*0.01,
            'starting_balance': (tfsa_starting or 0),
            'biweekly_contribution': (tfsa_contrib or 0),
            'contribution_room': (tfsa_contrib_room  or 0),
            'max_value': tfsa_limit or pd.np.inf,
            'yearly_contrib': tfsa_contrib_reset or 0 # contrib room added each year
        },
        {
            'name':'rrsp',
            'registered':True,
            'rate': (rrsp_interest or 0)*0.01,
            'starting_balance': rrsp_starting  or 0,
            'biweekly_contribution': rrsp_contrib  or 0,
            'max_value': rrsp_limit or pd.np.inf, #for first-time home buy
            'contribution_room': rrsp_contrib_room  or 0,
            'yearly_contrib':rrsp_contrib_reset or 0
        },
        {
            'name':'high_interest_savings',
            'rate': (hi_interest or 0)*0.01,
            'starting_balance': hi_starting or 0,
            'max_value': hi_limit or pd.np.inf, #hold at this value
            'biweekly_contribution':hi_contrib or 0
        }
    ]
    
    unregistered = {
            'name':'unregistered',
            'rate': (unreg_interest or 0)*0.01,
            'starting_balance': 0,
        }

    BW = projected_years * 26 if projected_years else 5 * 26 # years in 2-week chunks 

    ## Income

    #Pure salary income, with option for it to grow annualy

    income = pd.np.ones(BW)*me.get("biweekly_income", 0)
    for year in range(BW//26):
        if me.get("salary_cap_pct") and (1 + me.get("salary_cap_pct", 0)) * me.get("biweekly_income", 0) < income[year*26]:
            break
        else:
            income[year*26:]*= 1 + me.get("expected_raise_pct",0)

    unregistered_balance = pd.np.ones(BW)*unregistered.get('starting_balance',0)

    spending = pd.np.ones(BW) * me.get("biweekly_spend",0)
    rent = pd.np.ones(BW) * me.get("monthly_rent",0) * 12/26 # biweekly rent?

    income -= spending + rent # this is our takehome

    invest = sum([acct.get("biweekly_contribution") for acct in accounts_definition])# amount invested biweekly

    for account in accounts_definition:
        amount = account.get("biweekly_contribution",0)/invest if invest else 0
        account['ratio'] = amount

    ### Rules for distribution
    accts = []
    taxes = 0
    for account in accounts_definition:
        balance = pd.np.ones(BW)*account.get('starting_balance',0)
        contribution = pd.np.zeros(BW)
        interest = pd.np.zeros(BW)
        notes = [""]*BW

        contrib_room = account.get('contribution_room',pd.np.inf)

        for m in range(BW-1): # project forward
            amount = account.get("ratio", 0) * income[m]
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
                    tax = sum(interest[m-26:m]) * 0.5 * 0.53
                    taxes += tax
                    balance[m+1] -= tax # TODO: what's capital gains tax?
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
            tax = sum(interest[m-26:m]) * 0.5 * 0.53
            taxes += tax
            balance[m+1] -= tax # TODO: what's capital gains tax?
    accts += [pd.DataFrame({'acct':account['name'],'interest':interest,'balance':balance,'biweek':pd.np.arange(len(interest))})]

    cfs = pd.concat(accts, sort=False)

    import dateutil
    def add_weeks(save_df):
        save_df.index.name = 'biweek'
        save_df['date'] = [datetime.date.today() + dateutil.relativedelta.relativedelta(weeks=int(2*m)) for m in save_df.index.values]

    add_weeks(cfs)
    
    graph = px.area(cfs, x="date", y="balance", color="acct", title = "Your Savings At Work!")
    
    # other stats
    last = cfs[cfs.date == cfs.date.max()]
    total = last.balance.sum().astype(int)
    taxes = int(taxes)
    saved = int(income.mean())
    total_rent = rent.sum().astype(int)
    return graph, f"${total}", f"${saved}", f"${taxes}", f"${total_rent}"

server = app.server