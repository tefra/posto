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
$ pip install -e ".[dev]"
```

Start the app

```console
$ make start
```

# Verify installation

After you start the app in any way visit http://localhost:8001 you should get a welcome message.

# Run through pycharm

The default port of flask 5000 is already occupied in mac that's why we have switched to 8001, to
change it if you are running the app through pycharm or any other ide add the following argument.

```console
--port=8001
```


# Running tests

```console
$ pytest tests/
```
