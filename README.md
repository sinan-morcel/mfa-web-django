# Introduction

This is a demo project that demonstrates how to integrate your account system (users) implemented in Django with Acceptto multi-factor authentication/authorization system.

# Requirements
1. [Singup](https://acceptto.com/users/sign_up) for a new Acceptto acount or [Login](https://acceptto.com/users/sign_in) to your Accpetto dashboard
1. Navigate to **Applications** through the side menu
1. Click on the **New Application** button to create a new application, and then
	1. Choose a **Name** for your application which you're going to enable the multi-factor authentication for
	1. Set the **Color** to whatever you like, this is the color band user will see next to your application name in Acceptto mobile app
1. Find the new create application in the list and click on **Details** button
2. Find the **UID** and **Secret** and store them in a file called credentials.json in the root or base directory of the project, as shown here:
```
{
  "uid": "1234567890123456789012334",
  "secret": "0987654321098765432109876"
}
```
6. Install this project's dependencies using the following command:
```
python3 -m pip install -r requirements.txt
```

# Run The Sample Project
1. Setup the project's sqlite schema using the following command:
```
python3 manage.py migrate
```
2. Create a superuser by following the prompts of this command:
```
python3 manage.py createsuperuser
```
3. Run the server:
```
python3 manage.py runserver
```
4. Go to http://127.0.0.1:8000/admin/login and sign in using the superuser's credentials created in step 2.
5. Click on the change button next to the Users row.
6. Click on admin.
7. Scroll to the bottom of the page until you see the ACCEPTTO CREDENTIALS section.
8. Enter your Acceptto-Account email obtained in the requirements section of this README.
9. Click on SAVE to persist your changes.
10. Go back to http://127.0.0.1:8000/admin/login and sign in using the superuser's credentials. This time, multi-factor authentication is enabled.
11. Use the It's Me™ app to accept or reject the signin notification. Once this step is done, the browser redirects to the admin dashboard.
12. The same steps work for non-staff or superusers.
 




