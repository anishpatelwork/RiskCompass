# RiskCompass
Repo for Risk Compass app

## Installation

To start, clone this project to a destination of your choice. After cloning with git, navigate to that folder and install 
PipEnv and PyEnv.

You need to have postgres installed and running on your computer.


## Pylint - Django

We are using Pylint to manage coding standards. The plugin Pylint-django is available to improve code analysis when 
analysing code using Django. To install use this command: pip install pylint-django.

After the plugin is installed you can use it with this command when positioned at the root of the project: pylint --load-plugins pylint_django ./compass.
This will give you a list of all warnings and errors for the compass folder and rate your code.
