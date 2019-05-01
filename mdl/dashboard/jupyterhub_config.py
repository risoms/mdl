# Configuration file for jupyterhub.

#------------------------------------------------------------------------------
# Application(SingletonConfigurable) configuration
#------------------------------------------------------------------------------

## This is an application.

## The date format used by logging formatters for %(asctime)s
#c.Application.log_datefmt = '%Y-%m-%d %H:%M:%S'
#
### The Logging format template
#c.Application.log_format = '[%(name)s]%(highlevel)s %(message)s'
#

if __name__ == '__main__':
	## Set the log level by value or name.
	c.Application.log_level = 30
	#c.JupyterHub.redirect_to_server = False
	c.Spawner.default_url = '/lab'
	#c.JupyterHub.hub_ip = '0.0.0.0'