"""
This module defines the `AppRoutes` class, responsible for configuring 
routes for a Flask application. Routes include user authentication endpoints 
and ZPL label generation/printing functionalities.

Classes:
    - AppRoutes: Manages the application's routes.
"""
class AppRoutes:
    """
    A class to configure and manage routes for a Flask application.

    Attributes:
        app (Flask): The Flask application instance.
        user_auth: An instance handling user authentication functionalities.
        zpl_label_designer: An instance for ZPL label generation and printing functionalities.
    """
    def __init__(self, app, user_auth, zpl_label_designer):
        """
        Initializes the `AppRoutes` class with the Flask app, user authentication handler, 
        and ZPL label designer.

        Args:
            app (Flask): The Flask application instance.
            user_auth: An object providing user authentication methods (e.g., sign_up, sign_in).
            zpl_label_designer: An object providing methods for ZPL label generation and printing.
        """
        self.app = app
        self.user_auth = user_auth
        self.zpl_label_designer = zpl_label_designer
        self.add_routes()

    def add_routes(self):
        """
        Configures the routes for the application. Each route is tied to a specific 
        view function provided by `user_auth` or `zpl_label_designer`.
        """
        self.app.add_url_rule("/sign_up", methods=["POST"], view_func=self.user_auth.sign_up)
        """Endpoint for user sign-up."""

        self.app.add_url_rule("/sign_in", methods=["POST"], view_func=self.user_auth.sign_in)
        """Endpoint for user sign-in."""

        self.app.add_url_rule("/sign_out", methods=["POST"], view_func=self.user_auth.sign_out)
        """Endpoint for user sign-out."""

        self.app.add_url_rule("/token_refresh", methods=["POST"], view_func=self.user_auth.token_refresh)
        """Endpoint for refreshing user authentication tokens."""

        self.app.add_url_rule("/all_users", methods=["POST"], view_func=self.user_auth.get_all_users)
        """Endpoint to retrieve a list of all users."""

        self.app.add_url_rule("/update_user", methods=["POST"], view_func=self.user_auth.update_user)
        """Endpoint to update user details."""

        self.app.add_url_rule("/delete_user", methods=["POST"], view_func=self.user_auth.delete_user)
        """Endpoint to delete a user."""
        
        # ZPL Label Design and Printing Routes
        self.app.add_url_rule("/generate_zpl", methods=["POST"], view_func=self.zpl_label_designer.generate_zpl)
        """Endpoint to generate a ZPL label based on input data."""

        self.app.add_url_rule("/print_thermal_label", methods=["POST"], view_func=self.zpl_label_designer.print_thermal_label)
        """Endpoint to print a thermal label on a specified printer."""