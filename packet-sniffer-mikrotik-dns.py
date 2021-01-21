#!/usr/bin/python3
# packet-sniffer-mikrotik-dns.py
"""
CREATE TABLE dns_a (
A CHAR(255),
number_req BIGINT,
update_time TIME);
"""

# import library
import MySQLdb as mc
from scapy.all import *
from scapy.contrib.tzsp import TZSP

# decode TZSP encapsulation and add then into the real packet
def decodeTZSP(p):
    tzspEncapfrm = p[Raw].load
    tzspEncap = TZSP(tzspEncapfrm)
    p[UDP].remove_payload()
    p /= tzspEncap
    tzsp_lyr = p.getlayer(TZSP)
    assert(tzsp_lyr.type == TZSP.TYPE_RX_PACKET)
    return p

def Main(p):
    packet = decodeTZSP(p)
    dns = packet.getlayer(DNS)
    if dns.opcode == 0 and dns.qd.qtype == 1:
        cursor = connection.cursor()
        sql_check_cmd = "SELECT a FROM dns_a WHERE a='{0}'".format(bytes(dns.qd.qname).decode("ascii"))
        cursor.execute(sql_check_cmd)
        result_set = cursor.fetchall()
        if result_set:
            if result_set[0][0] == bytes(dns.qd.qname).decode("ascii"):
                sql_command = "UPDATE dns_a SET number_req=(number_req+1) WHERE `A` = '{0}';".format(bytes(dns.qd.qname).decode("ascii"))
                cursor.execute(sql_command)
                connection.commit()
                cursor.close()
        else:
            sql_command = "INSERT INTO dns_a (A, number_req) VALUES ('{0}', 1);".format(bytes(dns.qd.qname).decode("ascii"))
            cursor.execute(sql_command)
            connection.commit()
            cursor.close()

# start
if __name__ == "__main__":
    try:
        connection = mc.connect(host='localhost',
                                    db='dns_db',
                                    user='pyadmin',
                                    passwd='CHANGE_THIS')
    except mc.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)
    sniff(iface="eth0", filter="udp port 37008", prn=Main, store=0)
    connection.close()
