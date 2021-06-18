# Build

```bash
docker build . -t forarprov:latest
```

# Run

```bash
docker run -it -d \
  --name forarprov \
  --env PLACES='Farsta,Sollentuna,Tullinge,Nynäshamn,Södertälje' \
  --env SSN='<replace-with-your-ssn>' \
  --env START='2021-06-18' \
  --env END='2021-06-24' \
  --env TELEGRAM_TOKEN='<replace-with-telegram-bot-token>' \
  forarprov:latest
```
