import os
import cherrypy

# Configuring newrelic to track the performance of the service. `newrelic.ini` Will be download during the pod start.
if int(os.environ.get("IS_NEW_RELIC_ENABLED", 0)) and \
        os.path.exists(os.path.abspath(
            os.path.join(__file__, '..', 'app', 'newrelic.ini'))
        ):
    # if newrelic is enabled and config file is found, Enable NewRelic
    import newrelic.agent
    newrelic.agent.initialize(
        os.path.abspath(os.path.join(__file__, '..', 'app', 'newrelic.ini'))
    )

if __name__ == '__main__':
    """
    Configure cherrypy server to start the app. It will mount the application to `/` and using the below methods
    to run the app.
    
    - start(): Start all the services
    - block(): Wait for the EXITING state, KeyboardInterrupt or SystemExit
    - stop(): Stop all the services on keyboardInterrupt
    """

    try:
        from app import app
        # Mount the application
        cherrypy.tree.graft(app, "/")

        # Set the configuration of the web server
        cherrypy.config.update({
            'log.screen': True,
            'server.socket_port': app.config['PORT'],
            'server.socket_host': '::',
            'server.thread_pool': app.config['SERVER_THREAD_POOL'],
            'server.shutdown_timeout': app.config['SERVER_SHUTDOWN_TIMEOUT']
        })
        # Start App Initial Task
        cherrypy.engine.start()
        cherrypy.engine.block()

    except KeyboardInterrupt:
        cherrypy.engine.stop()