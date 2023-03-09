# Coffee Shop Full Stack

## Project overview

This project was implemented for the Udacity FSND program. The application realizes a coffee shop menu application that allows public users to view drinks while baristas and managers can additionally view detailed recipes or make changes according to their roles in the system.

The frontend part of this application was already pre-built using the Ionic framework. Basically, it is an almost complete coffee shop menu mobile application. The main purpose of the project is to implement a secure Flask-based backend to serve the requests of the frontend. Consequently, both parts are secured by a third party authentication provider - Auth0.com.

### Authentication workflow

In simple terms, the frontend sends an authorization request to Auth0 servers. Auth0 validates this request, provides a login form to authenticate the end user, and sends back an access token upon success. This access token is then used by the frontend to access the Flask-based backend API. The backend validates the token and checks the available permissions according to Auth0 predefined procedures.

## Installation

* Git-clone this project (or download and extract a zip file) into a separate folder.

* Navigate to the `/backend` folder to install dependencies and launch the backend server.
The details can be found in the readme file inside the folder.

* Navigate to the `/frontend` folder to install dependencies and launch the Ionic
development server. The details can be found in the readme file inside the folder.

* Open http://localhost:8100/ in your browser to run the Coffee shop app.
