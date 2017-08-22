import requests

__health_checks_url__ = "/v1/health/checks/"
__deregister_service_url__ = "/v1/agent/service/deregister/"


def __initConsulUrl(consulHost, consulPort):
    return "http://" + str(consulHost) + ":" + str(consulPort)


def getServiceList(serviceName, consulHost, consulPort):
    url = __initConsulUrl(consulHost=consulHost, consulPort=consulPort) \
          + __health_checks_url__ + serviceName

    req = requests.get(url=url)
    return req.json()


def deregisterService(service_id, consulHost, consulPort):
    url = __initConsulUrl(consulHost=consulHost, consulPort=consulPort) \
          + __deregister_service_url__ + service_id
    requests.get(url=url)
