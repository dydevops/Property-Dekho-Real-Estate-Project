from django.core.exceptions import PermissionDenied


def check_role_myadmin(user):
    if user.role == 'MyAdmin':
        return True
    else:
        raise PermissionDenied

# Restrict the customer from accessing the vendor page
def check_role_vendor(user):
    if user.role == 'Vendor':
        return True
    else:
        raise PermissionDenied
    
def check_role_customer(user):
    if user.role == 'Customer':
        return True
    else:
        raise PermissionDenied