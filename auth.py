"""
This script authenticates a users request to view the dashboard
"""

def get_user(request):
    login_username = request.get_argument('username')
    login_password = request.get_argument('password')

    # check if username and password are correct
    if(login_username=='nyc'):
        if(login_password=='iheartnyc'):
            return 1
    else:
        return None

login_url='/login'
