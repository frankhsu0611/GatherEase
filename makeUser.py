import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gte.settings")

# Initialize Django
django.setup()

from django.contrib.auth.models import User

users_data = [
    {
        'username': 'user1',
        'email': 'user1@example.com',
        'pass1': 'password1',
        'fname': 'John',
        'lname': 'Doe',
        'userCategory': 'Speaker',
        'conferenceCode': 'ICEASS2021',
        'userCountry': 'USA',
    },
    {
        'username': 'user2',
        'email': 'user2@example.com',
        'pass1': 'password2',
        'fname': 'Jane',
        'lname': 'Doe',
        'userCategory': 'Speaker',
        'conferenceCode': 'ICEASS2022',
        'userCountry': 'Canada',
    },
    {
        'username': 'user3',
        'email': 'user3@example.com',
        'pass1': 'password3',
        'fname': 'Bob',
        'lname': 'Smith',
        'userCategory': 'Attandee',
        'conferenceCode': 'ICEASS2022',
        'userCountry': 'UK',
    },
    {
        'username': 'user4',
        'email': 'user4@example.com',
        'pass1': 'password4',
        'fname': 'Alice',
        'lname': 'Johnson',
        'userCategory': 'Attandee',
        'conferenceCode': 'ICEASS2023',
        'userCountry': 'USA',
    },
    {
        'username': 'user5',
        'email': 'user5@example.com',
        'pass1': 'password5',
        'fname': 'Mike',
        'lname': 'Brown',
        'userCategory': 'Attandee',
        'conferenceCode': 'ICEASS2023',
        'userCountry': 'Australia',
    }
]

# Create the user instances
for user_data in users_data:
    username = user_data['username']
    email = user_data['email']
    pass1 = user_data['pass1']
    fname = user_data['fname']
    lname = user_data['lname']
    userCategory = user_data['userCategory']
    conferenceCode = user_data['conferenceCode']
    userCountry = user_data['userCountry']
    
    
    myuser = User.objects.create_user(username, email, pass1, userCategory, conferenceCode, userCountry)
    myuser.first_name = fname
    myuser.last_name = lname
    myuser.userCategory = userCategory
    myuser.conferenceCode = conferenceCode
    myuser.userCountry = userCountry
    myuser.save() # save to database after updating fields