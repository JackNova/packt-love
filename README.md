#Usage

- install python, pip, google app engine sdk
- create a project on google-app-engine and ensure to update the deployment script with your application id (replace your-app-id)
- install [jinja2-cli](https://github.com/mattrobenolt/jinja2-cli)


- edit you configuration variables in secrets.json
- cat secrets.json | jinja2 app_config.py.tpl > app_config.py
- cat secrets.json | jinja2 cron.yaml.tpl > cron.yaml


# Development

dev_appserver.py --port=9999 .

# Deployment

gcloud app deploy app.yaml --project `[your-project-id]` --version 1