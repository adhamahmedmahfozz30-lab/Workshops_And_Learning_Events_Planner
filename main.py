from Login_Register import login_registration

current_user = login_registration()

if current_user.role == 'user':
    # user menu()
else:
    # admin menu()