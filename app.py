from dash import html, dcc, Dash, Input, Output, State, callback, register_page, ALL
import dash
import dash_bootstrap_components as dbc

from flask import Flask

EXTERNAL_BOOTSTRAP = 'https://cdn.jsdelivr.net/npm/bootswatch@5.3.0/dist/lumen/bootstrap.min.css'

server = Flask(__name__)
app = Dash (
    server=server, 
    external_stylesheets = [
        EXTERNAL_BOOTSTRAP,
        'https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Source+Serif+4:wght@400;500&display=swap'
    ],
    use_pages = True
)

options_in_navbar = dbc.Nav (children = [
                            dbc.NavItem (dbc.NavLink ('SDG Information', id = {'type' : 'link-navbar', 'index' : ''}, href = '/')),
                            dbc.NavItem (dbc.NavLink ('SDG-Focused Tab', id = {'type' : 'link-navbar', 'index' : 'sdg-focused-tab'}, href = '/sdg-focused-tab')), 
                            dbc.NavItem (dbc.NavLink ('Region-Focused Tab', id = {'type' : 'link-navbar', 'index' : 'region-focused-tab'}, href = '/region-focused-tab')),   
                        ],
                        navbar = True,
                        pills = True,
                        fill = True,
                        justified = True,
                        className = "me-2"
                    )

navbar = dbc.Navbar(
    children = [
        # Icon source: https://www.flaticon.com/free-icon/growth_2889137
        dbc.Container (children = [
            html.Img(src=dash.get_asset_url('growth.png'), height="24px", className = "ms-2"),
            dbc.NavbarBrand ("The Progress of the Philippines in the SDG", 
                                className = "ms-2 h-100 me-auto",
                                style = {
                                    'font-weight' : 'bold',
                                    'vertical-align' : 'middle'
                                },
                            ), 
        ]),
        dbc.NavbarToggler (id = "navbar-toggler", n_clicks = 0),
        dbc.Collapse (
                options_in_navbar,
                id = "navbar-collapse",
                is_open = False,
                navbar = True,
                className = "ms-auto"
        ),
    ],
    color = 'primary',
    dark = True,
    sticky = 'top'
)

app.layout = dbc.Container(id = 'main-container',
                           children = [
                               dcc.Location(id="url"),
                               navbar, 
                               dash.page_container
                            ],
                            style = {
                                'margin-right': '0 !important',
                                'max-width': '100%',
                                'padding' : '0px',
                                'height' : '100vh'
                            }, 
)

# For collapsing navbar for small screens
@callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
        Output({"type":"link-navbar", "index": ALL}, "className"), 
        [Input("url", "pathname"), 
         Input({"type":"link-navbar", "index": ALL}, "id")]
)
def callback_func(pathname, link_elements):
    pathname = pathname [1:]
    temp_list = ["nav-active" if val["index"] == pathname else "nav-not-active" for val in link_elements]

    if 'nav-active' not in temp_list:
        temp_list [0] = 'nav-active'

    return temp_list


if __name__ == '__main__':
    server.run(host='0.0.0.0', port='8080')


register_page (
    __name__, 
    path = '/'
)