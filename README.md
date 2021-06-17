# Build

```bash
docker build . -t forarprov:latest
```

# Run

```bash
docker run -it \
  --env PLACES='Farsta,Sollentuna,Tullinge,Nynäshamn,Södertälje' \
  --env SSN='19900921XXXX' \
  --env START='2021-06-18' \
  --env END='2021-12-30' \
  forarprov:latest 
```
