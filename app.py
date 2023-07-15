import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State, ClientsideFunction

import dash_bootstrap_components as dbc

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
app.config.suppress_callback_exceptions = False





app.layout = start_layout



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
    if 'bc_ajouter' in dash.callback_context.triggered[0]['prop_id']:
        data.append({'tab_produit':prod, 'tab_fournisseur':fourn, 'tab_qte':nbre})
        return [data]
    return [data]


@app.callback(
   [
    Output('fourn_table', 'data'),
   ],
   [
    Input('fourn_ajouter', 'n_clicks'),
   ],
   [
    State('fourn_table', 'data'),
    State('fourn_nom', 'value'),
    State('fourn_siret', 'value'),
   ]
)
def bc_table_update(n1,data, nom, siret):
    if 'fourn_ajouter' in dash.callback_context.triggered[0]['prop_id']:
        data.append({'tab_fourn':nom, 'tab_code_siret':siret})
        return [data]
    return [data]


@app.callback(
   [
    Output('product_table', 'data'),
   ],
   [
    Input('product_ajouter', 'n_clicks'),
    Input('product_produit_filter', 'value'),
    Input('product_code_barre_filter', 'value'),
   ],
   [
    State('product_table', 'data'),
    State('product_produit', 'value'),
    State('product_code_barre', 'value'),
    State('product_molecule', 'value'),
    State('product_famille', 'value'),
    State('product_ordonance', 'value'),
   ]
)
def product_table_update(n1, prod_filter, cb_filter,data, prod, code_barre, molec, famille, ord):
    if 'product_ajouter' in dash.callback_context.triggered[0]['prop_id']:
        data.append({'tab_produit':prod, 'tab_code_barre':code_barre, 'tab_molecule':molec, 'tab_famille':famille, 'tab_ordonance':ord})
        return [data]
    elif prod_filter:
        if prod_filter=='':
            return [data]
        return [[ele for ele in data if ele['tab_produit'].startswith(prod_filter)]]
    return [data]

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



# Run the server
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=True, port=8050)
