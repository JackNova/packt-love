#Usage

- edit you configuration variables in app_config.py
- create a project on google-app-engine and ensure to update the deployment script with your application id (replace your-app-id)

chmod 755 deploy.sh

#launch the application locally

    ./deploy.sh serve

#publish the app

    ./deploy.sh production