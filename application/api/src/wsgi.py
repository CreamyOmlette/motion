"""Web Server Gateway Interface"""

##################
# FOR PRODUCTION
####################
from app import app

if __name__ == "__main__":
    ####################
    # FOR DEVELOPMENT
    ####################
    app.run(host='0.0.0.0', debug=True, port=80)