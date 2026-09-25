from Login_Register import login_registration
from user_menu import user_menu
from admin_menu import admin_menu


while True:
    current_user = login_registration()
    if current_user.role == 'user':
        user_menu(current_user)
    else:
        admin_menu(current_user)
