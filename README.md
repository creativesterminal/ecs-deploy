# Creatives Terminal ECS-Deploy

This script deploy some (or all) the Creatives Terminal Services to Amazon EC2 Container Service (ECS).

## How it works

Based on a .yaml file located in `./config/services.yaml` the script clone the repository of the service
container, the source code of the service, build the image for the service, push it to the Creatives
Terminal Registry and after this deploy it to the Amazon ECS.

## Dependencies

- Docker
- Python
- [PyYAML](http://pyyaml.org/)
- [GitPython](https://github.com/gitpython-developers/GitPython)

## How to use

> usage: deploy-images.py [-h] [-f FILE] [-s SERVICES [SERVICES ...]]
  optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Choose the yaml file of configuration (default:
                        ./config/services.yaml)
  -s SERVICES [SERVICES ...], --services SERVICES [SERVICES ...]
                        Define which services on yaml file will be configured
                        (default: all)

First of all, rename the file local.env.dist to local.env with `mv local.env.dist local.env`. After this,
edit local.env and put your credentials to AWS.

After this run the deploy-images.py script to deploy new version of all the services. If you need you can
specify where is your .yaml file with the parameter `-f` and also which services on the yaml file you want
to deploy with the `-s` parameter.

`./scripts/deploy-images.py`
`./scripts/deploy-images.py -f /path/to/file.yaml -s auth-service`

## TODO

* Rollback of deploy
* Rollback of deploy in case of error
* Specify deploy by tag (actually works by branch)
* Decrease the time needed to build images
