# Random Phrase API

Generates random phrases from the phrases.txt file for the frontend_api.py app.

## Requirements

- create a docker network called `app-net`

```bash
docker network create app-net
```

## Docker Command

```bash
docker run -d --rm --name backend -p 7070:7070 -h backend --network app-net <container image>
```
