## Setup

Create a new project with the [Google Cloud Platform console](https://console.cloud.google.com/).
Make a note of your project ID, which may be different than your project name.

Download the [Google Cloud SDK](https://cloud.google.com/sdk/docs/) to your
local machine.

Initialize the Google Cloud SDK:

    gcloud init

Create your App Engine application:

    gcloud app create

Set an environment variable for your project ID, replacing `[YOUR_PROJECT_ID]`
with your project ID:

    export PROJECT_ID=[YOUR_PROJECT_ID]


## Deploying to App Engine

Open `app.yaml` and property setup the required environment variables

Deploy your application to App Engine using `gcloud`. Please note that this may
take several minutes.

    gcloud app deploy