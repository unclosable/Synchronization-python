import consulCheck.consul_actions as ca
import configparser

if __name__ == "__main__":
    cf = configparser.ConfigParser()
    cf.read("consul.conf")
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
