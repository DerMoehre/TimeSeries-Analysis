#from dash import Input, Output, State, callback_context
#from dash import html
#
#def register_sidebar_callbacks(app):
#    @app.callback(
#        Output("upload-modal", "is_open"),
#        [
#            Input("open-upload-modal", "n_clicks"),
#            Input("close-upload-modal", "n_clicks"),
#        ],
#        State("upload-modal", "is_open"),
#    )
#    def toggle_modal(open_clicks, close_clicks, is_open):
#        ctx = callback_context
#        if not ctx.triggered:
#            return is_open
#        if ctx.triggered[0]["prop_id"].split(".")[0] in ["open-upload-modal", "close-upload-modal"]:
#            return not is_open
#        return is_open
#
#    @app.callback(
#        Output("upload-status", "children"),
#        Output("uploaded-data-store", "data"),
#        Input("delete-data-button", "n_clicks"),
#        State("uploaded-data-store", "data"),
#    )
#    def clear_uploaded_data(delete_clicks, stored_data):
#        if delete_clicks > 0:
#            return "Uploaded data deleted", None
#        return "", stored_data
