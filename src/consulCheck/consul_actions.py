import sqlite3
import consulCheck.consul_utils as cus
import os

project_dir = os.path.dirname(os.path.abspath(__file__))


def reflush_service_status(serviceName, consulHost, consulPort):
    sList = cus.getServiceList(serviceName=serviceName, consulHost=consulHost, consulPort=consulPort)
    servicelist = filter(lambda o: o['Status'] != "passing", sList)
    sqllit = sqlite3.connect(project_dir + "/consul.db")
    cur = sqllit.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS consul_server_status(serverID varchar(64) primary key,check_time integer,"
                "service_name varchar(64),service_host varchar(64),service_port integer)")
    for item in servicelist:
        sID = item['ServiceID']
        cur.execute("SELECT serverID,check_time FROM consul_server_status WHERE serverID = ? "
                    "AND service_name=? AND service_host=? AND service_port=?",
                    (sID, serviceName, consulHost, consulPort))
        re = cur.fetchall()
        if re:
            cur.execute("UPDATE consul_server_status SET check_time=? WHERE  serverID = ?", (re[0][1] + 1, sID))
            sqllit.commit()
        else:
            cur.execute(
                "INSERT INTO consul_server_status(serverID,check_time,service_name,service_host,service_port)"
                " VALUES (?,?,?,?,?)",
                (sID, 1, serviceName, consulHost, consulPort))
            sqllit.commit()
    return [item for item in servicelist]


def remove_server(consulHost, consulPort):
    removed = []
    sqllit = sqlite3.connect(project_dir + "/consul.db")
    cur = sqllit.cursor()
    cur.execute("SELECT serverID,check_time,service_name FROM consul_server_status WHERE "
                " service_host=? AND service_port=? AND check_time>3",
                (consulHost, consulPort))
    re = cur.fetchall()
    if re:
        for item in re:
            cus.deregisterService(item[0], consulHost, consulPort)
            removed.append(consulHost + ':' + str(consulPort) + '--' + item[2] + '::' + item[0])
    cur.execute("DELETE FROM consul_server_status WHERE "
                " service_host=? AND service_port=? AND check_time>3",
                (consulHost, consulPort))
    sqllit.commit()
    return removed
