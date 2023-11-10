# Setup your python virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
```

# Install the dependencies

```sh
pip install -r requirements.txt
```

# Train with

```sh
./run-train.sh
```

# Deploy

```sh
oc login ...
```

```sh
cd deploy
./deploy.sh
```