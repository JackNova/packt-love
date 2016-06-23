#Usage

- Clone this repo locally
- Install GoogleAppEngineLauncher for your environment: https://cloud.google.com/appengine/downloads?hl=en#Google_App_Engine_SDK_for_Python
- If you don't have it already, create an account on packtpub.com and take a note of your email and password
- complete the app_config.py file with your configurations

**Example**

    config = {
        "ALTERNATIVE_LOCAL_PYTHON_MODULES_PATH": "/Users/<YourUser>/anaconda/lib/python2.7/site-packages",
        "PACKT_EMAIL": "<your account email here>",
        "PACKT_PASSWORD": "<your account password here>",
        "USER_EMAIL": "<your account email for appengine here>"
    }

The **ALTERNATIVE_LOCAL_PYTHON_MODULES_PATH** field is used for local development.

The **USER_EMAIL** field is used to send you a daily email notification with details about the book you purchased; And to send health monitoring emails with eventual errors. Ensure that this email account is autorised to send email on google app engine platform.

- edit the cron.yaml file and set your own email for health monitoring

> _ereporter?sender=your_account_email@you.com&to=your_account_email@you.com

- create a project on google-app-engine and keep note of the id that your project is given, you'll need this for deployment
- set your account email in the Daily exception report section of the cron.yaml file

- publish the app by issuing following command

> appcfg.py -A your-project-id update /packt-love 


# Launch the local server for local development

> dev_appserver.py --port=9988 . --log_level=debug # --clear_datastore=yes
> 

# Run tests

```bash
python -m unittest functional_test
```