# posto

Post something, I will store it somewhere for sure!.

# Clone Repo

```console
$ git clone git@github.com:tefra/posto.git
$ cd posto
```

# Docker installation

This step requires to have docker installed.

```console
$ docker-compose up --build
```

Only include the `--build` on the first run or if we have made changes in the requirements.

# Virtualenv installation

This step also requires docker in order to start the elastic search engine and the kibana services.


```console
$ docker-compose up elasticsearch kibana

```

This step requires to setup a virtual environment manually, personally I use [pyenv](https://github.com/pyenv/pyenv-installer)

```console
$ pyenv install 3.10-dev
$ pyenv virtualenv 3.10-dev posto
$ pyenv active posto
```

If you use zsh and enable the pyenv plugin, you can auto activate the environment every time you enter the project by defining the env like this

```console
$ pyenv local posto
```

Install the app like this

```console
$ pip install -e ".[test]"
```

Start the app

```console
$ make start
```

# Verify installation

After you start the app in any way visit http://localhost:8001 you should get a welcome message.

Open the kibana home page, you will need to create an index pattern, easier if you submit a few
events first

http://localhost:5601/app/management/kibana/indexPatterns

In the repo there is also a postman collection that you can also use.


# Run through pycharm

The default port of flask 5000 is already occupied in mac that's why we have switched to 8001, if
you are running the app through pycharm or any other ide add the following argument.

```console
--port=8001
```

# Running tests

```console
$ pytest tests/
```

# Integrate with the actual webhooks

Use [ngrok](https://ngrok.com/) to expose your local as a public url

```console
$ ngrok http 8001
Session Status                online
Session Expires               1 hour, 59 minutes
Version                       2.3.40
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://ebbf-188-4-52-202.ngrok.io -> http://localhost:8001
Forwarding                    https://ebbf-188-4-52-202.ngrok.io -> http://localhost:8001
```


Use the forwarding url and append the `/webhook/` endpoint of the app, **ending slash matters**
