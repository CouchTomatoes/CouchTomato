from couchtomato import app
import argparse

def cmd_couchtomato():
    """Commandline entry point."""
    # Make sure views are imported and registered.
    #import couchtomato.views
    app.run(debug=True)