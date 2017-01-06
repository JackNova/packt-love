cron:
- description: daily check for new ebooks
  url: /
  schedule: every day 09:00
  timezone: Europe/Rome

- description: Daily exception report
  url: /_ereporter?sender={{administrator.email}}&to={{notification.email}}
  schedule: every day 00:00