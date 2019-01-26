# VUE-js aiohttp example

## Running

```bash
pip install -r requirements.txt

python main.py
```

## Run in docker

1. Clone the repo
2. `docker build -t calculator .`
3. `docker run -d -p 8080:8080 --log-opt max-size=10m calculator`
4. Open `http://localhost:8080/` in your browser
5. Enjoy

