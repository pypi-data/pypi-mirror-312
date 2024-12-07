![](https://raw.githubusercontent.com/turokg/yappa/master/docs/logo.png)

# Simple deploy of python web-apps @YandexCloud
Forget about setting up your own infrastructure, vps, network, orchestrators, etc... go **serverless**

![](https://raw.githubusercontent.com/turokg/yappa/master/docs/demo.gif)

* [Quickstart](#quickstart)
    * [Updates](#updates)
* [Deployment examples](#deployment-examples)
* [Django](#django)
    * [Management commands](#management-commands)
    * [Creating superuser](#creating-superuser)
* [Yandex Cloud authorization](#yandex-cloud-authorization)
* [Limitations](#limitations)
    * [Database connectivity](#database-connectivity)
    * [Headers and authorization](#headers-and-authorization)
* [Articles](#articles)
* [Roadmap](#roadmap)
    * [Next steps](#next-steps)
    * [Far-faraway plans](#far-faraway-plans)
* [Troubleshooting](#troubleshooting)
* [Support and contribution](#support-and-contribution)
* [Acknowledgements](#acknowledgements)

## Quickstart

1. setup virtual env, create your app
2. create account at Yandex Cloud
3. install Yappa

```shell
$ pip install yappa -U
$ pip freeze > requirements.txt
 ```

4. use Yappa:

```shell
$ yappa setup
$ yappa deploy
 ```

...that's it! Your application is deployed

### Updates

when your code is updated just run

```shell
$ yappa deploy
 ```

## Deployment examples

Both WSGI and ASGI applications are supported (as well as raw functions). So Django, Flask, FastAPI... etc could be
easily deployed.

Furthermore, not just regular json API could be deployed this way. Several types of applications could be launched with
Yappa:

- [raw serverless function](https://github.com/turokg/yappa/tree/master/examples/raw_function)
- [raw serverless function + Postgres](https://github.com/turokg/yappa/tree/master/examples/raw_function_postgres)
- json API ([Flask](https://github.com/turokg/yappa/tree/master/examples/flask),
  [FastAPI](https://github.com/turokg/yappa/tree/master/examples/fast_api),
  [Django rest framework](https://github.com/turokg/yappa/tree/master/examples/django/1_drf_base_managed_postges))
- single page application
- SPA + multiple API versions  
  ...   
  more examples will be added soon

## Django

please see examples:
- [Django Rest Framework basic](https://github.com/turokg/yappa/tree/master/examples/django/1_drf_base_managed_postges) - basic DRF app. To explore serverless and Yappa features, like management commands
- [Django Rest Framework + Postgres](https://github.com/turokg/yappa/tree/master/examples/django/1_drf_base_managed_postges) - 
- DRF app with managed Postgres connectivity

### Management commands

django manage.py commands are supported. just run

```shell
$ yappa manage migrate
```

In order to support management commands, for Django projects second cloud function is being created every deploy. It's
made only for handling management commands, and it's not public. Therefore, commands do not support user inputs: to
every command '--no-input' flag is added.

### Creating superuser

As of Django 3.0 env variables are supported for createsuperuser command. So you should deploy your app with
DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD environment variables. Then run

```shell
$ yappa manage createsuperuser
```

The other way around would be to implement custom management command (see
[StackOverflow topic](https://stackoverflow.com/questions/6244382/how-to-automate-createsuperuser-on-django))

## Yandex Cloud authorization

Command '$ yappa setup' prompts you for OAuth token. Then, Yappa creates 
service account "yappa-uploader-service" with
roles editor and serverless.functions.admin for the specified folder.
Key for this account is created and saved locally at .yc file.

Command '$ yappa deploy' supports two types of authorization

- service account key saved at .yc file (generated during '$ yappa setup')
- environment variables YC_OAUTH and YC_FOLDER

## Limitations

There are some limitations, however YandexCloud team is constantly 
releasing new features and services. Also, the team
of this project will try to keep up. So stay tuned :)

### Database connectivity

Managed Postgres and YandexDB is supported inside Yandex Cloud. 
In case any other DB - it has to have public IP address

For details on how te set up connection with managed postgres 
please refer to

- [YandexCloud docs](https://cloud.yandex.ru/docs/functions/operations/database-connection)
- [raw function + Postgres example](https://github.com/turokg/yappa/tree/master/examples/raw_function_postgres)
- [Django example](https://github.com/turokg/yappa/tree/master/examples/django/drf_base)

### Headers and authorization

Please note that some request headers (like Authorization) are
[deleted before function is invoked](https://cloud.yandex.ru/docs/functions/concepts/function-invoke)

## Articles
Habr:
- [Yappa: запускаем python web-приложения. Просто. Бессерверно. В Яндекс Облаке]( https://habr.com/ru/post/569674/ )

## Development and Contribution

Please see [project boards](https://github.com/turokg/yappa/projects)
and [issues](https://github.com/turokg/yappa/issues). With any questions and suggestions please visit
our  [telegram chat](https://t.me/yappa_chat)

In the near future we will be focused on documentation improvements (mainly deployment examples) and support of async
tasks (serverless workers and scheduler for celery).

## Troubleshooting

- installing grpcio on Apple M1: installing with anaconda may help. Also look
  at [stackoverflow](https://stackoverflow.com/questions/66640705/how-can-i-install-grpcio-on-an-apple-m1-silicon-laptop)
- versions of python 3.7 support yappa up to 0.3.12. You should use python 3.8 and above for new versions of yappa.

## Acknowledgements

- [Mikhail Novikov](https://github.com/kurtgn) for starting this project two years ago
- [httpx](https://github.com/encode/httpx) as a great tool for calling WSGI/ASGI apps offline
- [Zappa](https://github.com/Miserlou/Zappa) for inspiration  
