
import dash
from dash import dcc, dash_table
from dash import html
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, ClientsideFunction
import dash_mantine_components as dmc
from dash_iconify import DashIconify

import numpy as np
import pandas as pd
import datetime
from datetime import datetime as dt
import pathlib

noms_medocs = pd.read_csv('./data/refs_medicaments.csv', usecols = ['NOM'])[:50].values.reshape(-1)

vente_layout = html.Div(
    children=[
        html.H5('Veuillez scanner votre produit'),
        html.Div(
            className='anim-box center spacer',
            children=[
                html.Div(),
                html.Div(className='scanner'),
                html.Div(className='anim-item anim-item-sm'),
                html.Div(className='anim-item anim-item-lg'),
                html.Div(className='anim-item anim-item-sm'),
                html.Div(className='anim-item anim-item-sm'),
                html.Div(className='anim-item anim-item-md'),
                html.Div(className='anim-item anim-item-sm'),
                html.Div(className='anim-item anim-item-lg'),
                html.Div(className='anim-item anim-item-md'),
                html.Div(className='anim-item anim-item-lg'),
                html.Div(className='anim-item anim-item-sm'),
                html.Div(className='anim-item anim-item-sm'),
                html.Div(className='anim-item anim-item-sm'),
                html.Div(className='anim-item anim-item-lg'),
                html.Div(className='anim-item anim-item-lg'),
                html.Div(className='anim-item anim-item-md'),
                html.Div(className='anim-item anim-item-sm'),
                html.Div(className='anim-item anim-item-sm'),
                html.Div(className='anim-item anim-item-md'),
                html.Div(className='anim-item anim-item-md'),
                html.Div(className='anim-item anim-item-sm'),
                html.Div(className='anim-item anim-item-lg'),
                html.Div(className='anim-item anim-item-md'),
                html.Div(className='anim-item anim-item-lg'),
                html.Div(className='anim-item anim-item-sm'),
            ]
        ),
        dmc.Button('Scan produit', id="modal-demo-button", style={"display":'block', 'margin-left':'auto', 'margin-right':'auto'}),
        html.Br(),
        dmc.Divider(label="Vue d'ensemble", labelPosition="center"),
        html.Br(),
        dmc.Modal(
            title="Détails du produit",
            id="modal-simple",
            zIndex=10000,
            children=[
                dmc.Group(
                    [
                        dmc.TextInput(label="Code produit:", id='cb_prod_achat', placeholder='Scan code barre'),
                        dmc.Select(label="Nom produit:", id='nom_prod_achat', data=noms_medocs, searchable=True, clearable=True, nothingFound="Aucun produit trouvé", placeholder='Tapez le nom du produit'),
                        dmc.NumberInput(label='Quantité:', id='qte_prod_achat', value=1, min=1, step=1),
                        # dmc.Select(
                        #     label="Remise",
                        #     placeholder="Choix de remise",
                        #     value="aucune",
                        #     data=[
                        #         {"value": "aucune", "label": "Aucune"},
                        #         {"value": "10%", "label": "10%"},
                        #         {"value": "15%", "label": "15%"},
                        #     ],
                        # ),                        
                    ],
                    position="left",
                ),
                dmc.Group(
                    [
                        dmc.Button("Valider", id="modal-submit-button"),
                        dmc.Button(
                            "Annuler",
                            color="red",
                            variant="outline",
                            id="modal-close-button",
                        ),
                    ],
                    position="right",
                ),
            ],
        ),
        dmc.Grid(
            children=[
                dmc.Col(
                    children=[
                        html.Div(
                            id='articles_pour_achat',
                            
                        ),
                        
                    ],
                span=6),
                dmc.Col(
                    children=[
                        html.Div(
                            id='facture_pour_achat',
                        ),
                        html.Div(
                            id='facture_pour_achat_modal',
                        ),

                        dmc.Modal(
                            title="Modalité de paiement",
                            id="modal-simple-bis",
                            centered=True,
                            zIndex=10000,
                            children=[
                                dmc.Text("Mode de paiement", weight=500),
                                dmc.SegmentedControl(
                                    orientation="horizontal",
                                    fullWidth=True,
                                    color='blue',
                                    data=["CB", "Cash", "Crédit"]
                                ),
                                dmc.Space(h=20),
                                dmc.Grid(
                                    children=[
                                        dmc.Col(dmc.Select(
                                            label='Client',
                                            data=["Momo", "Abdel", "Joe"],
                                            clearable=True,
                                            style={"width": '90%'},
                                        ), span=9),
                                        dmc.Col(dmc.Select(
                                            label='Remise',
                                            data=["10%", "20%", "30%"],
                                            clearable=True,
                                            style={"width": '90%'},
                                        ), span=3),
                                    ]
                                ),
                                dmc.Space(h=20),
                                dmc.Divider(variant="dashed"),
                                dmc.Text(id='total_paiement_affich', size="lg", weight=700, align="right"),
                                dmc.Text(id='total_paiement_affich_remise', size="xl", weight=700, align="right"),
                                dmc.Space(h=20),
                                dmc.Grid(
                                    children=[
                                        dmc.Col(
                                            children=[
                                                dmc.Button(
                                                    "Imprimer la facture",
                                                    leftIcon=DashIconify(icon="basil:invoice-outline"),
                                                    color='green',
                                                ),
                                            ],
                                            span=9
                                        ),
                                        dmc.Col(
                                            children=[
                                                dmc.Group(
                                                    [
                                                        dmc.Button("Valider", id="valider_paiement"),
                                                        dmc.Button(
                                                            "Annuler",
                                                            color="red",
                                                            variant="outline",
                                                            id="annuler_paiement",
                                                        ),
                                                    ],
                                                    position="right",
                                                ),
                                            ],
                                            span=3
                                        ),
                                    ]
                                ),
                                
                            ],
                            size='50%'
                        ),
                            
                    ],
                span=6),
            ],
            gutter="xl",
        ),
        html.Div(id="notifications-container"),
        dmc.Button("Show Notification", id="notify"),
    ]
)

create_bc = html.Div(
    #className='courses-container',
    children=[
        html.Div(
            className='form-style-10',
            children=[
                html.H1(
                    children=[
                        'Formulaire de création du bon de commande',
                        html.Span('Veuillez renseigner les informations ci-dessous'),
                    ]
                ),
                html.Form(
                    [
                        html.Div(
                            className='section',
                            children=[
                                html.Span('1'),
                                'Produits',
                            ]
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        html.Div(
                                            children=[
                                                html.H6('Selection du produit'),
                                                dcc.Dropdown(
                                                    id='bc_produit',
                                                    options=[
                                                        {'label': 'Doliprane', 'value': 'NYC'},
                                                        {'label': 'Paracétamol', 'value': 'MTL'},
                                                        {'label': 'Pomade jaune', 'value': 'SF'},
                                                    ],
                                                    value='MTL'
                                                ),
                                            ],
                                        style={'width': '40%'}),
                                        html.Div(
                                            children=[
                                                html.H6('Fournisseur'),
                                                dcc.Dropdown(
                                                    id='bc_fournisseur',
                                                    options=[
                                                        {'label': 'Fournisseur 1', 'value': 'f1'},
                                                        {'label': '2', 'value': 'f2'},
                                                        {'label': '3', 'value': 'f3'},
                                                    ],
                                                    value='f3',
                                                    className='dropdown',
                                                ),
                                            ],
                                        style={'width': '20%'}),
                                        html.Div(
                                            children=[
                                                html.H6('Selection du nombre'),
                                                dcc.Input(id='bc_number', type='number'),
                                            ],
                                        style={'width': '20%'}),
                                        html.Div(
                                            children=[
                                                html.H6('Inventaire'),
                                                html.H5('10/20'),
                                            ],
                                        style={'width': '20%'}),
                                    ],
                                style={'width': '100%', 'display': 'flex'}),
                                html.Br(),
                                html.Button('Ajouter', id='bc_ajouter', className='button-valid'),
                                html.Br(),
                                html.Br(),
                            ]
                        ),
                        html.Div(
                            className='section',
                            children=[
                                html.Span('2'),
                                'Résumé',
                            ]
                        ),
                        html.Div(
                            className='inner-wrap',
                            children=[
                                html.Div(
                                    className='table-container',
                                    children=[
                                        html.Div(
                                            dash_table.DataTable(
                                                id='bc_table',
                                                columns=[
                                                    {'name': 'Produit', 'id': 'tab_produit'},
                                                    {'name': 'Fournisseur', 'id': 'tab_fournisseur'},
                                                    {'name': 'Quantité', 'id': 'tab_qte'},
                                                ],
                                                data=[
                                                    {'tab_produit':'Doliprane', 'tab_fournisseur':'f1', 'tab_qte':5}
                                                ],
                                                editable=True,
                                                row_deletable=True
                                            ),
                                            
                                        )
                                    ],
                                ),
                                html.Br(),
                                html.Button('Valider', id='bc_valider', className='button-valid'),
                            ]
                        ),
                    ]
                )
            ]
        )
    ]
)

suivi_bc = html.Div(
    children=[
        html.Div(
            className='form-style-10',
            children=[
                html.H1(
                    children=[
                        'Suivi de vos commandes',
                        html.Span('Sélectionner la commande à vérifier'),
                    ]
                ),
                html.Form(
                    [
                        html.Div(
                            className='section',
                            children=[
                                html.Span('1'),
                                'Demandes en cours',
                            ]
                        ),
                        html.Div(
                            [
                                dmc.Select(
                                    label="Choix de la commande",
                                    placeholder="Commande en cours",
                                    value='com1',
                                    data=[
                                        {"value": "com1", "label": "Commande 1"},
                                        {"value": "com2", "label": "Commande 2"},
                                        {"value": "com3", "label": "Commande 3"},
                                        {"value": "com4", "label": "Commande 4"},
                                    ],
                                    style={"width": "80%", "marginBottom": 10},
                                ),
                            ]
                        ),
                        html.Div(
                            className='section',
                            children=[
                                html.Span('2'),
                                'Suivi actuel',
                            ]
                        ),
                        html.Br(),
                        html.Div(
                            [
                                dmc.Timeline(
                                    active=1,
                                    bulletSize=15,
                                    lineWidth=2,
                                    children=[
                                        dmc.TimelineItem(
                                            title="Création de la commande",
                                            children=[
                                                dmc.Text(
                                                    ["01/01/2023"],
                                                    color="dimmed",
                                                    size="sm",
                                                ),
                                            ],
                                        ),
                                        dmc.TimelineItem(
                                            title="Commande validée",
                                            children=[
                                                dmc.Text(
                                                    ["02/01/2023"],
                                                    color="dimmed",
                                                    size="sm",
                                                ),
                                            ],
                                        ),
                                        dmc.TimelineItem(
                                            title="Commande en livraison",
                                            lineVariant="dashed",
                                            children=[
                                                dmc.Text(
                                                    ["03/01/2023"],
                                                    color="dimmed",
                                                    size="sm",
                                                ),
                                            ],
                                        ),
                                        dmc.TimelineItem(
                                            title="Commande livrée",
                                            children=[
                                                dmc.Text(
                                                    ["04/01/2023"],
                                                    color="dimmed",
                                                    size="sm",
                                                ),
                                            ],
                                        ),
                                    ],
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
    ]
)

create_product = html.Div(
    #className='courses-container',
    children=[
        html.Div(
            className='form-style-10',
            children=[
                html.H1(
                    children=[
                        'Formulaire de création d\'un nouveau produit',
                        html.Span('Veuillez renseigner les informations ci-dessous'),
                    ]
                ),
                html.Form(
                    [
                        html.Div(
                            className='section',
                            children=[
                                html.Span('1'),
                                'Informations produit',
                            ]
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        html.Div(
                                            children=[
                                                html.H6('Nom du produit'),
                                                dcc.Input(id='product_produit', type='text'),
                                            ],
                                        style={'width': '70%'}),
                                        html.Div(
                                            children=[
                                                html.H6('Code barre'),
                                                dcc.Input(id='product_code_barre', type='text'),
                                            ],
                                        style={'width': '30%'}),
                                    ],
                                    style={'width': '100%', 'display': 'flex'}
                                ),
                                html.Div(
                                    children=[
                                        html.Div(
                                            children=[
                                                html.H6('Molécule active'),
                                                dcc.Input(id='product_molecule', type='text'),
                                            ],
                                        style={'width': '40%'}),
                                        html.Div(
                                            children=[
                                                html.H6('Famille de produits'),
                                                dcc.Dropdown(
                                                    id='product_famille',
                                                    options=[
                                                        {'label': 'Famille 1', 'value': 'fam1'},
                                                        {'label': 'Famille 2', 'value': 'fam2'},
                                                        {'label': 'Famille 3', 'value': 'fam3'},
                                                    ],
                                                    value='fam3',
                                                    className='dropdown',
                                                ),
                                            ],
                                        style={'width': '40%'}),
                                        html.Div(
                                            children=[
                                                html.H6('Sous ordonance'),
                                                dcc.Dropdown(id='product_ordonance', options=[{'label':'Oui', 'value':'oui'}, {'label':'Non', 'value':'non'}]),
                                            ],
                                        style={'width': '20%'}),
                                    ],
                                style={'width': '100%', 'display': 'flex'}),
                            html.Br(),
                            dmc.Button("Ajouter", id='ajouter_produit'),
                            html.Br(),
                            html.Br(),
                            ]
                        ),
                        html.Div(
                            className='section',
                            children=[
                                html.Span('2'),
                                'Liste des produits',
                            ]
                        ),
                        html.Br(),
                        html.H5('Filtrer par:'),
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        html.H6('Nom du produit'),
                                        dcc.Input(id='product_produit_filter', type='text'),
                                    ],
                                style={'width': '70%'}),
                                html.Div(
                                    children=[
                                        html.H6('Code barre'),
                                        dcc.Input(id='product_code_barre_filter', type='text'),
                                    ],
                                style={'width': '30%'}),
                            ],
                            style={'width': '100%', 'display': 'flex'}
                        ),
                        html.Br(),
                        html.Div(
                            # className='inner-wrap',
                            children=[
                                html.Div(
                                    id='product_table_div',
                                    # className='table-container',
                                    # children=[
                                    #     html.Div(
                                    #         dash_table.DataTable(
                                    #             id='product_table',
                                    #             columns=[
                                    #                 {'name': 'Nom du produit', 'id': 'tab_produit'},
                                    #                 {'name': 'Code barre', 'id': 'tab_code_barre'},
                                    #                 {'name': 'Molécule', 'id': 'tab_molecule'},
                                    #                 {'name': 'Famille de produit', 'id': 'tab_famille'},
                                    #                 {'name': 'Ordonance', 'id': 'tab_ordonance'},
                                    #             ],
                                    #             data=[],
                                    #             editable=True,
                                    #             row_deletable=True,
                                    #             page_size=15
                                    #         ),
                                            
                                    #     )
                                    # ],
                                ),
                                html.Br(),
                            ]
                        ),
                    ]
                )
            ]
        )
    ]
)


create_fournisseur = html.Div(
    #className='courses-container',
    children=[
        html.Div(
            className='form-style-10',
            children=[
                html.H1(
                    children=[
                        'Formulaire de création d\'un nouveau fournisseur',
                        html.Span('Veuillez renseigner les informations ci-dessous'),
                    ]
                ),
                html.Form(
                    [
                        html.Div(
                            className='section',
                            children=[
                                html.Span('1'),
                                'Informations fournisseur',
                            ]
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        html.Div(
                                            children=[
                                                html.H6('Raison sociale'),
                                                dcc.Input(id='fourn_nom', type='text'),
                                            ],
                                        style={'width': '70%'}),
                                        html.Div(
                                            children=[
                                                html.H6('Code SIRET'),
                                                dcc.Input(id='fourn_siret', type='text'),
                                            ],
                                        style={'width': '30%'}),
                                    ],
                                    style={'width': '100%', 'display': 'flex'}
                                ),
                                # html.Div(
                                #     children=[
                                #         html.Div(
                                #             children=[
                                #                 html.H6('Info fournisseur'),
                                #                 dcc.Input(id='product_molecule', type='text'),
                                #             ],
                                #         style={'width': '40%'}),
                                #         html.Div(
                                #             children=[
                                #                 html.H6('Famille de produits'),
                                #                 dcc.Dropdown(
                                #                     id='product_famille',
                                #                     options=[
                                #                         {'label': 'Famille 1', 'value': 'fam1'},
                                #                         {'label': 'Famille 2', 'value': 'fam2'},
                                #                         {'label': 'Famille 3', 'value': 'fam3'},
                                #                     ],
                                #                     value='fam3',
                                #                     className='dropdown',
                                #                 ),
                                #             ],
                                #         style={'width': '40%'}),
                                #         html.Div(
                                #             children=[
                                #                 html.H6('Sous ordonance'),
                                #                 dcc.Dropdown(id='product_ordonance', options=[{'label':'Oui', 'value':'oui'}, {'label':'Non', 'value':'non'}]),
                                #             ],
                                #         style={'width': '20%'}),
                                #     ],
                                # style={'width': '100%', 'display': 'flex'}),
                            html.Br(),
                            dmc.Button("Ajouter", id='fourn_ajouter'),
                            html.Br(),
                            html.Br(),
                            ]
                        ),
                        html.Div(
                            className='section',
                            children=[
                                html.Span('2'),
                                'Liste des fournisseurs',
                            ]
                        ),
                        html.Br(),
                        html.H5('Filtrer par:'),
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        html.H6('Raison sociale'),
                                        dcc.Input(id='fourn_nom_filter', type='text'),
                                    ],
                                style={'width': '70%'}),
                                html.Div(
                                    children=[
                                        html.H6('Code SIRET'),
                                        dcc.Input(id='fourn_siret_filter', type='text'),
                                    ],
                                style={'width': '30%'}),
                            ],
                            style={'width': '100%', 'display': 'flex'}
                        ),
                        html.Br(),
                        html.Div(
                            # className='inner-wrap',
                            children=[
                                html.Div(
                                    # className='table-container',
                                    id='fourn_table_div'
                                ),
                                html.Br(),
                            ]
                        ),
                    ]
                )
            ]
        )
    ]
)


achat_layout = html.Div(
    [
        dcc.Tabs(id="achat-tabs", value='tab-1-creation-BC', children=[
            dcc.Tab(label='Création du bon de commande', value='tab-1-creation-BC', children=create_bc),
            dcc.Tab(label='Suivi de commande', value='tab-1-suivi-BC', children=suivi_bc),
            dcc.Tab(label='Gestion des produits', value='tab-2-gestion-produit', children=create_product),
            dcc.Tab(label='Gestion des fournisseurs', value='tab-3-gestion-founisseur', children=create_fournisseur),
        ]),
    ],
    #className='container'
)


df = pd.DataFrame(
    {
        "Transaction": ["11111", "11112", "11113", "11114"],
        "Client": ["vzvas2zv5", "asdvav110v", "ascadv99a", "c4advaev20"],
        "Date & heure": ["Lundi 01/01/2023 08:00", "Lundi 01/01/2023 08:05", "Lundi 01/01/2023 08:07", "Lundi 01/01/2023 08:11"],
        "Nombre de produits": [5, 2, 1, 3],
        "N° de poste": [1, 2, 1, 1],
        "Options": [
            html.Div(
                [
                    dmc.Button("Détails", leftIcon=DashIconify(icon="ph:eye", width=20)), 
                    dmc.Button("Facture", leftIcon=DashIconify(icon="solar:bill-list-linear", width=20), color='red'),
                    dmc.Button("Editer", leftIcon=DashIconify(icon="tabler:edit", width=20), color='green')
                ]
            )]*4
    }
)

df1 = pd.DataFrame(
    {
        "Transaction": ["11111"]*10,
        "Fournisseur": ["vzvas2zv5"]*10,
        "Bon de commande": ["147527"]*10,
        "Date & heure de commande": ["Lundi 01/01/2023 08:00"]*10,
        "Bon de livraison": ["L147527"]*10,
        "Date & heure de livraison": ["Lundi 09/01/2023 08:00"]*10,
        "Nombre de produits": [5]*10,
        "Signataire": ["Respo 1"]*10,
        "Options": [
            html.Div(
                [
                    dmc.Button("Détails", leftIcon=DashIconify(icon="ph:eye", width=20)), 
                    dmc.Button("Facture", leftIcon=DashIconify(icon="solar:bill-list-linear", width=20), color='red'),
                    dmc.Button("Editer", leftIcon=DashIconify(icon="tabler:edit", width=20), color='green')
                ]
            )]*10
    }
)

hist_ventes = html.Div(
    className='form-style-10',
    children=[
        html.Div(
            dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, style={'width':'100%'}),
        )
    ] 
)

hist_achats = html.Div(
    className='form-style-10',
    children=[
        html.Div(
            dbc.Table.from_dataframe(df1, striped=True, bordered=True, hover=True, style={'width':'100%'}),
        )
    ] 
)

hitorique_layout = html.Div(
    [
        dcc.Tabs(id="historique-tabs", value='tab-1-hist-ventes', children=[
            dcc.Tab(label='Historique des ventes', value='tab-1-hist-ventes', children=hist_ventes),
            dcc.Tab(label='Historique des achats', value='tab-2-hist-achats', children=hist_achats),
        ]),
    ],
)

df_inventaire = pd.DataFrame(
    {
        "Produit": ["11111", "11111", "11111", "11111"],
        "Famille": ["vzvas2zv5", "vzvas2zv5","vzvas2zv5","vzvas2zv5"],
        "Quantité": [50, 25, 5, 0],
        "Quantité minmum": [20, 20, 20, 20],
        "Statut": [dmc.Badge("En stock", variant="filled", color='blue'), 
                   dmc.Badge("Quantité moyenne", variant="filled", color='grape'), 
                   dmc.Badge("A approvisioner", variant="filled", color='orange'), 
                   dmc.Badge("En rupture de stock", variant="filled", color='red')],
        "Options": [
            html.Div(
                [
                    dmc.Button("Détails", leftIcon=DashIconify(icon="ph:eye", width=20)), 
                    dmc.Button("Facture", leftIcon=DashIconify(icon="solar:bill-list-linear", width=20), color='red'),
                    dmc.Button("Editer", leftIcon=DashIconify(icon="tabler:edit", width=20), color='green')
                ]
            )]*4
    }
)

inventaire_layout = html.Div(
    className='form-style-10',
    children=[
        dbc.Table.from_dataframe(df_inventaire, striped=True, bordered=True, hover=True, style={'width':'100%'}),
    ]
)


df = px.data.tips()

fig = px.box(df, x="day", y="total_bill", color="smoker")
fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default

df1 = px.data.stocks()
fig1 = px.line(df1, x='date', y="GOOG")

df2 = px.data.tips() # replace with your own data source
fig2 = px.pie(df2, values='total_bill', names='day', hole=.3)

fig3 = px.icicle(df, path=[px.Constant("all"), 'sex', 'day', 'time'],
                values='total_bill', color='day')
fig3.update_layout(margin = dict(t=50, l=25, r=25, b=25))
statistics_layout = html.Div(
    [
        dcc.Graph(figure=fig),
        dcc.Graph(figure=fig1),
        html.Div(
            [
                html.Div(dcc.Graph(figure=fig2), className='six columns'),
                html.Div(dcc.Graph(figure=fig3), className='six columns'),
            ],
            className="row"
        ),
    ]
)

start_layout = html.Div(
    id="app-container",
    children=[
        # Banner
        dmc.Group(
            [
                dmc.Image(src="assets/logo_app.jpg", width='25%'),
                dmc.Menu(
                    [
                        dmc.MenuTarget(dmc.ActionIcon(DashIconify(icon="tabler:user"))),
                        dmc.MenuDropdown(
                            [
                                dmc.MenuItem("Informations", icon=DashIconify(icon="tabler:search"), id="useless-button1", n_clicks=0),
                                dmc.MenuItem("Paramètres", icon=DashIconify(icon="tabler:settings"), id="useless-button2", n_clicks=0),
                                dmc.MenuDivider(),
                                dmc.MenuItem("Se déconnecter", color="red", id="useless-button3", n_clicks=0),
                            ]
                        ),
                    ],
                    style={'position':'absolute', 'right':'0'}
                ),
            ],
            className="banner",
            # position="right",
        ),
        html.Div(
            id="banner",
            children=[
                # html.Img(src="assets/logo_app.jpg"),
            ],
        ),
        # Sidebar
        # Left column
        html.Div(
            id="left-column",
            className="one columns",
            children=[
                html.Div([
                    html.Button(
                        [html.Span('Vente'),],
                        id='vente_bttn',
                        className='button-slot',
                    ),
                    html.Button(
                        [html.Span('Achat'),],
                        id='achat_bttn',
                        className='button-slot',
                    ),
                    html.Button(
                        [html.Span('Historique'),],
                        id='historique_bttn',
                        className='button-slot',
                    ),
                ], className='row align-items-right'),
                html.Div([
                    html.Button(
                        [html.Span('Inventaire'),],
                        id='inventaire_bttn',
                        className='button-slot',
                    ),
                    html.Button(
                        [html.Span('Analyses'),],
                        id='analyses_bttn',
                        className='button-slot',
                    ),
                ], className='row align-items-right'),
                html.Div([
                    html.Button(
                        [html.Span('Contacts'),],
                        id='contacts_bttn',
                        className='button-slot',
                    ),
                    html.Button(
                        [html.Span('Factures'),],
                        id='factures_bttn',
                        className='button-slot',
                    ),
                ], className='row align-items-right'),
            ]
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eleven columns",
            children=[
                # Patient Volume Heatmap
                html.Div(
                    id="corps_contenu",
                    children=[
                        html.Div(id='vente_container', children=vente_layout, style={'display': 'none'}),
                        html.Div(id='achat_container', children=achat_layout, style={'display': 'none'}),
                        html.Div(id='historique_container', children=hitorique_layout, style={'display': 'none'}),
                        html.Div(id='inventaire_container', children=inventaire_layout, style={'display': 'none'}),
                        html.Div(id='statistics_container', children=statistics_layout, style={'display': 'none'}),
                    ]
                )
            ],
        ),
    ],
)

