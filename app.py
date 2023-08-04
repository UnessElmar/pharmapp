import dash
from dash import dcc, dash_table
from dash import html
from dash.dependencies import Input, Output, State, ClientsideFunction

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from dash_iconify import DashIconify

import os
import numpy as np
import pandas as pd
import datetime
from datetime import datetime as dt
import pathlib

from layout import start_layout

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    # external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]
)
app.title = "Pharmapp"

server = app.server
app.config.suppress_callback_exceptions = True





app.layout = start_layout

def df_to_table(df):
    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    table = [html.Thead(header), html.Tbody(rows)]
    disp_table = dmc.Table(
        striped=True,
        highlightOnHover=True,
        withBorder=True,
        withColumnBorders=True,
        children=table
    )
    return disp_table

@app.callback(
   [
    Output('vente_container', 'style'),
    Output('historique_container', 'style'),
    Output('statistics_container', 'style'),
    Output('achat_container', 'style'),
    Output('inventaire_container', 'style'),
   ],
   [
    Input('vente_bttn', 'n_clicks'),
    Input('historique_bttn', 'n_clicks'),
    Input('analyses_bttn', 'n_clicks'),
    Input('achat_bttn', 'n_clicks'),
    Input('inventaire_bttn', 'n_clicks'),
   ]
)
def show_hide_element(n1,n2,n3,n4,n5):
    if 'vente_bttn' in dash.callback_context.triggered[0]['prop_id']:
        return [{'display': 'block'},{'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'none'}]
    elif 'historique_bttn' in dash.callback_context.triggered[0]['prop_id']:
        return [{'display': 'none'},{'display': 'block'},{'display': 'none'},{'display': 'none'},{'display': 'none'}]
    elif 'analyses_bttn' in dash.callback_context.triggered[0]['prop_id']:
        return [{'display': 'none'},{'display': 'none'},{'display': 'block'},{'display': 'none'},{'display': 'none'}]
    elif 'achat_bttn' in dash.callback_context.triggered[0]['prop_id']:
        return [{'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'block'},{'display': 'none'}]
    elif 'inventaire_bttn' in dash.callback_context.triggered[0]['prop_id']:
        return [{'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'block'}]
    else:
        return [{'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'none'}]



@app.callback(
   [
    Output('bc_table', 'data'),
   ],
   [
    Input('bc_ajouter', 'n_clicks'),
   ],
   [
    State('bc_table', 'data'),
    State('bc_produit', 'value'),
    State('bc_fournisseur', 'value'),
    State('bc_number', 'value'),
   ]
)
def bc_table_update(n1,data, prod, fourn, nbre):
    if n1:
        data.append({'tab_produit':prod, 'tab_fournisseur':fourn, 'tab_qte':nbre})
        return [data]
    return [data]




@app.callback(
   [
    Output('fourn_table_div', 'children'),
    Output('fourn_nom', 'value'),
    Output('fourn_siret', 'value'),
   ],
   [
    Input('fourn_ajouter', 'n_clicks'),
    Input('fourn_nom_filter', 'value'),
    Input('fourn_siret_filter', 'value'),
   ],
   [
    State('fourn_nom', 'value'),
    State('fourn_siret', 'value'),
   ]
)
def product_table_update(n1, fourn_filter, siret_filter, fourn_id, siret_id):
    if not os.path.isfile('./data/fournisseurs_df.csv'):
        pd.DataFrame(columns=
                     ['Raison sociale', 'SIRET']
                     ).to_csv('./data/fournisseurs_df.csv', header=True, index=False)
        
    data = pd.read_csv('./data/fournisseurs_df.csv')
    
    if 'fourn_ajouter' in dash.callback_context.triggered[0]['prop_id']:
        data = pd.concat([
            data,
            pd.DataFrame([{'Raison sociale':fourn_id, 'SIRET':siret_id}])
        ], axis=0)
        data.to_csv('./data/fournisseurs_df.csv', header=True, index=False)
        return [df_to_table(data)]+['']*2
    elif fourn_filter:
        if fourn_filter=='':
            return [df_to_table(data)]\
                    + [fourn_id, siret_id]
        else:
            new_data = data[data['Raison sociale'].str.startswith(fourn_filter)]
            return [df_to_table(new_data)]\
                    + [fourn_id, siret_id]
    elif siret_filter:
        if siret_filter=='':
            return [df_to_table(data)]\
                    + [fourn_id, siret_id]
        else:
            new_data = data[data['SIRET'].str.startswith(siret_filter)]
            return [df_to_table(new_data)]\
                    + [fourn_id, siret_id]
        
    if data.shape[0]==0:
        return [[]] + [fourn_id, siret_id]
    return [df_to_table(data)]\
                    + [fourn_id, siret_id]




@app.callback(
   [
    Output('product_table_div', 'children'),
    Output('product_produit', 'value'),
    Output('product_code_barre', 'value'),
    Output('product_molecule', 'value'),
    Output('product_famille', 'value'),
    Output('product_ordonance', 'value'),
   ],
   [
    Input('ajouter_produit', 'n_clicks'),
    Input('product_produit_filter', 'value'),
    Input('product_code_barre_filter', 'value'),
   ],
   [
    State('product_produit', 'value'),
    State('product_code_barre', 'value'),
    State('product_molecule', 'value'),
    State('product_famille', 'value'),
    State('product_ordonance', 'value'),
   ]
)
def product_table_update(n1, prod_filter, cb_filter, prod, code_barre, molec, famille, ord):
    if not os.path.isfile('./data/products_df.csv'):
        pd.DataFrame(columns=
                     ['tab_produit', 'tab_code_barre', 'tab_molecule', 'tab_famille', 'tab_ordonance']
                     ).to_csv('./data/products_df.csv', header=True, index=False)
        
    data = pd.read_csv('./data/products_df.csv')
    
    if 'ajouter_produit' in dash.callback_context.triggered[0]['prop_id']:
        data = pd.concat([
            data,
            pd.DataFrame([{'tab_produit':prod, 'tab_code_barre':code_barre, 
                            'tab_molecule':molec, 'tab_famille':famille, 
                            'tab_ordonance':ord}])
        ], axis=0)
        data.to_csv('./data/products_df.csv', header=True, index=False)
        return [df_to_table(data)]+['']*5
    elif prod_filter:
        if prod_filter=='':
            return [df_to_table(data)]\
                    + [prod, code_barre, molec, famille, ord]
        else:
            new_data = data[data.tab_produit.str.startswith(prod_filter)]
            return [df_to_table(new_data)]\
                    + [prod, code_barre, molec, famille, ord]
    elif cb_filter:
        if cb_filter=='':
            return [df_to_table(data)]\
                    + [prod, code_barre, molec, famille, ord]
        else:
            new_data = data[data.tab_produit.str.startswith(cb_filter)]
            return [df_to_table(new_data)]\
                    + [prod, code_barre, molec, famille, ord]
        
    if data.shape[0]==0:
        return [[]] + [prod, code_barre, molec, famille, ord]
    return [df_to_table(data)]\
                    + [prod, code_barre, molec, famille, ord]



def create_list_achats(data):
    cards_list = []
    for idx, row in data.iterrows():
        cards_list.append(
            html.Div(
                className='course',
                children=[
                    html.Div(
                        className='course-preview',
                        children=[
                            html.H6('Sans ordonnance'),
                            html.H2(row.produit),
                            html.A(
                                href="#",
                                children=[
                                    'Fiche produit',
                                    html.I(className='fas fa-chevron-right')
                                ]
                            ),
                        ]
                    ),
                    html.Div(
                        className='course-info',
                        children=[
                            html.Div(
                                className='progress-container',
                                children=[
                                    html.Div(className='progress20'),
                                    html.Span(
                                        '20/100 en stock',
                                        className='progress-text',
                                    )
                                ]
                            ),
                            html.H6('Quantité: {}'.format(row.qte)),
                            html.H6('Prix unitaire: {} Dh'.format(row.prix)),
                            html.H2('Prix total: {} DH'.format(row.qte*row.prix)),
                            html.Div(
                                dmc.ButtonGroup(
                                    [
                                        dmc.Button("Modifier", color='green'),
                                        dmc.Button("Annuler", color='red'),
                                    ],
                                    
                                ),
                                className='buttons-container'
                            ) 
                        ]
                    ),
                        
                ]
            ),
        )
    return html.Div(cards_list)

def create_facture_achats(data):
    grids_list = []
    ['code', 'produit', 'qte', 'prix', 'tab_ordonance']
    for idx, row in data.iterrows():
        grids_list.append(
            html.Div(
                dmc.Grid(
                    children=[
                        dmc.Col(dmc.Text(row.produit), span=3),
                        dmc.Col(dmc.Text(row.qte), span=1),
                        dmc.Col(dmc.Text(row.prix), span=3),
                        dmc.Col(dmc.Text(row.qte*row.prix), span=3),
                        dmc.Col(dmc.Badge("-10%", color="red", variant="light"), span=2),
                    ]
                ),
            ),
        )

    all_grids = html.Div(
        [
            dmc.Group(
                [
                    dmc.Text("Facture", weight=500),
                    # dmc.Badge("On Sale", color="red", variant="light"),
                ],
                position="apart",
                mt="md",
                mb="xs",
            ),
            dmc.Divider(label="Détails"),
            html.Br(),
            dmc.Grid(
                children=[
                    dmc.Col(dmc.Text("Produit", weight=700), span=3),
                    dmc.Col(dmc.Text("Qté", weight=700), span=1),
                    dmc.Col(dmc.Text("PU", weight=700), span=3),
                    dmc.Col(dmc.Text("Prix", weight=700), span=3),
                    dmc.Col(dmc.Text("Promo", weight=700), span=2),
                ]
            ),
            html.Div(grids_list),
            html.Br(),
            dmc.Divider(label="Total"),
            dmc.Title('{} DH'.format((data.qte*data.prix).sum()), order=1, align='right'),
            dmc.Button(
                "Paiement",
                id='modal_paiement',
                variant="light",
                color="blue",
                fullWidth=True,
                mt="md",
                radius="md",
            ),
        ],
    )
    final_facture = dmc.Card(
                        children=[
                            all_grids
                        ],
                        withBorder=True,
                        shadow="sm",
                        radius="md",
                        
                        # style={"width": 350},
                    ),
    return final_facture


@app.callback(
   [
    Output('articles_pour_achat', 'children'),
    Output('facture_pour_achat', 'children'),
    Output('total_paiement_affich', 'children'),
    Output('total_paiement_affich_remise', 'children'),
   ],
   [
    Input('modal-submit-button', 'n_clicks'),
    Input('valider_paiement', 'n_clicks'),
   ],
   [
    State('cb_prod_achat', 'value'),
    State('nom_prod_achat', 'value'),
    State('qte_prod_achat', 'value'),
   ]
)
def ajout_prod_achat(n1, n2, cb_prod, nom_prod, qte_prod):
    
    if not os.path.isfile('./data/tmp_achats.csv'):
        pd.DataFrame(columns=
                     ['code', 'produit', 'qte', 'prix']
                     ).to_csv('./data/tmp_achats.csv', header=True, index=False)
    data = pd.read_csv('./data/tmp_achats.csv')
    if 'modal-submit-button' in dash.callback_context.triggered[0]['prop_id']:
        prod_df = pd.read_excel('./data/refs_medicaments.xlsx')
        prod_df["CODE"] = prod_df["CODE"].values.astype('str')
        prod_row = prod_df.loc[prod_df.CODE==cb_prod]
        if prod_row.shape[0]!=1 and prod_row.shape[0]!=0:
            prod_row = prod_row[0]
        data = pd.read_csv('./data/tmp_achats.csv')    
        data = pd.concat([
            data,
            pd.DataFrame([{'code':prod_row.CODE.values[0], 'produit':prod_row.NOM.values[0], 
                            'qte':qte_prod, 'prix':prod_row.PH.values[0]}])
                        ], axis=0)
        
        data.to_csv('./data/tmp_achats.csv', header=True, index=False)
        return create_list_achats(data), create_facture_achats(data), 'Total: {} DH'.format((data.qte*data.prix).sum()), 'Avec remise: {} DH'.format((data.qte*data.prix).sum())
    
    
    if 'valider_paiement' in dash.callback_context.triggered[0]['prop_id']:
        os.remove('./data/tmp_achats.csv')
        return None, None, '', ''
    if data.shape[0]==0:
        return [None, None, '', '']
    
    return [None, None, '', '']


@app.callback(
   [
    Output('cb_prod_achat', 'value'),
    Output('nom_prod_achat', 'value'),
    Output('qte_prod_achat', 'value'),
   ],
   [
    Input('cb_prod_achat', 'value'),
    Input('nom_prod_achat', 'value'),
    Input('modal-submit-button', 'n_clicks'),
    Input('modal-close-button', 'n_clicks'),
   ]
)
def update_product_values(cb_prod, nom_prod, n1, n2):
    prod_df = pd.read_excel('./data/refs_medicaments.xlsx')
    prod_df["CODE"] = prod_df["CODE"].values.astype('str')
    if 'modal-submit-button' in dash.callback_context.triggered[0]['prop_id'] or 'modal-close-button' in dash.callback_context.triggered[0]['prop_id']:
        return ['', '', 1]
    elif 'nom_prod_achat' in dash.callback_context.triggered[0]['prop_id']:
        if nom_prod=='':
            return '', '', 1
        elif nom_prod in prod_df.NOM.values:
            prod_row = prod_df.loc[prod_df.NOM==nom_prod]
            return prod_row.CODE.values[0], nom_prod, 1
        else:
            return '', nom_prod, 1
    elif 'cb_prod_achat' in dash.callback_context.triggered[0]['prop_id']:
        if cb_prod=='':
            return '', '', 1
        elif cb_prod in prod_df.CODE.values:
            prod_row = prod_df.loc[prod_df.CODE==cb_prod]
            return cb_prod, prod_row.NOM.values[0], 1
        else:
            return cb_prod, '', 1
    
    return ['', '', 1]



    


@app.callback(
    Output("modal-simple", "opened"),
    Input("modal-demo-button", "n_clicks"),
    Input("modal-close-button", "n_clicks"),
    Input("modal-submit-button", "n_clicks"),
    State("modal-simple", "opened"),
    prevent_initial_call=True,
)
def modal_demo(nc1, nc2, nc3, opened):
    return not opened

@app.callback(
    Output("modal-simple-bis", "opened"),
    Input("modal_paiement", "n_clicks"),
    Input("annuler_paiement", "n_clicks"),
    Input("valider_paiement", "n_clicks"),
    State("modal-simple-bis", "opened"),
    prevent_initial_call=True,
)
def modal_demo_bis(nc1, nc2, nc3, opened):
    if 'modal_paiement' in dash.callback_context.triggered[0]['prop_id'] and 'modal_paiement':
        if dash.callback_context.triggered[0]['value']:
            return True
    if 'annuler_paiement' in dash.callback_context.triggered[0]['prop_id'] or 'valider_paiement' in dash.callback_context.triggered[0]['prop_id']:
        return False
    return False

# @app.callback(
#     Output("notif_validation_paiement", "children"),
#     Input("valider_paiement", "n_clicks"),
#     prevent_initial_call=True,
# )
# def show(n_clicks):
#     if 'valider_paiement' in dash.callback_context.triggered[0]['prop_id']:
#         return dmc.Text('TEEEEEEEEEEEEEEEEEEXXXXXXXXXXXTTTTTTTTTTTT')

@app.callback(
    Output("notifications-container", "children"),
    Input("notify", "n_clicks"),
    prevent_initial_call=True,
)
def show(n_clicks):
    return dmc.Notification(
        title="Hey there!",
        id="simple-notify",
        action="show",
        message="Notifications in Dash, Awesome!",
        icon=DashIconify(icon="ic:round-celebration"),
    )

# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
    app.run_server(host='0.0.0.0', debug=True, port=8050)
