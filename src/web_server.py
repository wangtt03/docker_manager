#Encoding=UTF8

import tornado.ioloop
import tornado.web
import registry_handler
import projects_handler
import status_handler
import deploy_handler
import github_handler
import vm_handler
import my_registry_handler

application = tornado.web.Application([
    (r"/registry", registry_handler.RegistryHandler),
    (r"/project", projects_handler.ProjectsHandler),
    (r"/status", status_handler.StatusHandler),
    (r"/github", github_handler.GitHubHandler),
    (r"/deploy", deploy_handler.DeployHandler),
    (r"/myregistry", my_registry_handler.MyRegistryHandler),
    (r"/vm", vm_handler.VMHandler)
    ])


if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
