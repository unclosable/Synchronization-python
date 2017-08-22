import consulCheck.consul_actions as ca
import configparser
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
if __name__ == "__main__":
    print(project_dir)
    cf = configparser.ConfigParser()
    cf.read(project_dir + "/consul.conf")
    sections = cf.sections()
    for section in sections:
        print('check--' + section)
        host = cf[section]['server_host']
        port = cf[section]['server_port']
        names = cf[section]['server_name']
        for name in names.split(','):
            ca.reflush_service_status(name, host, port)
        removed = ca.remove_server(host, port)
        if removed:
            for rm in removed:
                print(rm)
