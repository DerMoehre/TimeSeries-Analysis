# from dash import Input, Output, State, callback_context
# from dash import html
#
# DUPLICATE USE OF UPLOADED-DATA_STORE AS OUTPUT IN UPLOAD.PY

# def register_callbacks(app):
#    # Combined callback for toggling modal and updating upload status
#    @app.callback(
#        [
#            Output("upload-modal", "is_open"),
#            Output("upload-status", "children"),
#            Output("uploaded-data-store", "data"),
#        ],
#        [
#            Input("open-upload-modal", "n_clicks"),
#            Input("close-upload-modal", "n_clicks"),
#            Input("delete-data-button", "n_clicks"),
#        ],
#        [
#            State("upload-modal", "is_open"),
#            State("uploaded-data-store", "data"),
#        ],
#    )
#    def handle_all_callbacks(
#        open_clicks, close_clicks, delete_clicks, is_open, stored_data
#    ):
#        ctx = callback_context
#        if not ctx.triggered:
#            # No input has triggered the callback yet; return current state
#            return is_open, "", stored_data
#
#        # Determine which input triggered the callback
#        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
#
#        if triggered_id in ["open-upload-modal", "close-upload-modal"]:
#            # Toggle the modal state
#            return not is_open, "", stored_data
#
#        if triggered_id == "delete-data-button" and delete_clicks > 0:
#            # Clear uploaded data
#            return is_open, "Uploaded data deleted", None
#
#        # Default fallback (return current state)
#        return is_open, "", stored_data
