import pprint
import random

from flask import Flask, render_template, jsonify
from paramiko import SSHClient, AutoAddPolicy
from netmiko import ConnectHandler
import time

hostname = "yy.yy.yy.yy"
app = Flask(__name__)

cisco_nx = {
    'device_type': 'cisco_nxos',
    'ip': 'xx.xx.xx.xx',
    'username': 'admin',
    'password': 'admin',
    'port': 22,  # optional, defaults to 22
    'secret': 'secret',  # optional, defaults to ''
    'verbose': False,  # optional, defaults to False/print
}

net_connect = ConnectHandler(**cisco_nx)

#output = net_connect.send_command('show interface ethernet 1/1-3 | i rate')
output = net_connect.send_command('show interface ethernet 1/49-52 | i rate')
splitted_stats = output.split('\n')


@app.route('/')
def index_nx():
    return render_template('nx-template.html')

#@app.route('/')
#def hello_world():
#    return 'Hello, World!'




@app.route('/get_status')
def add_numbers():
    cmd_pre = "ping -c 1 " + hostname
    status = 'checking'
    lbl_class = 'label label-success'
    btn_class = 'btn btn-warning btn-circle btn-xl'

    s = SSHClient()
    s.set_missing_host_key_policy(AutoAddPolicy())
    s.connect('xx.xx.xx.xx', port=22, username='virl', password='VIRL')
    stdin, stdout, stderr = s.exec_command(cmd_pre)

    k = stdout.read()
    if 'min/' in k:
        status = 'is up!'
        print(hostname, 'is up!')
        lbl_class = 'label label-success'
        min_ping = k[k.find('min/'):]
        min_ping = min_ping[min_ping.find('=') + 2:]
        min_ping = min_ping[:min_ping.find('/')]
        print('Minimal ping is : {0}'.format(min_ping))
        btn_class = 'btn btn-success btn-circle btn-xl'
    else:
        status = 'is down!'
        print(hostname, 'is down!')
        lbl_class = 'label label-warning'
        min_ping = '0'
        btn_class = 'btn btn-warning btn-circle btn-xl'

    return jsonify(status=status, lbl_class=lbl_class, ping=min_ping, btn_class=btn_class)


@app.route('/get_pps')
def connect_to_nx():
    print(random.uniform(1.5, 1.9))
    output = net_connect.send_command('show interface ethernet 1/49-52 | i rate')
    splitted_stats = output.split('\n')
    try:
        print(output)
        st49 = splitted_stats[1].lstrip().split()
        st50 = splitted_stats[4].lstrip().split()
        st51 = splitted_stats[7].lstrip().split()
        st52 = splitted_stats[10].lstrip().split()
        stats = {'49': [st49[-2], st49[-1]],
                 '50': [st50[-2], st50[-1]],
                 '51': [st51[-2], st51[-1]],
                 '52': [st52[-2], st52[-1]]
                 }
        return jsonify(status='works', stats=stats)

    except:
        return jsonify(status="N/A")


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("7979"),
        debug=True
    )

    # while True:
    #     output = net_connect.send_command('show interface ethernet 1/49-52 | i rate')
    #     splitted_stats = output.split('\n')
    #     print '*'*20
    #     print splitted_stats
    #     try:
    #         stats = {'49': splitted_stats[2].lstrip(),
    #                  '50': splitted_stats[5].lstrip(),
    #                  '51': splitted_stats[8].lstrip(),
    #                  '52': splitted_stats[11].lstrip()}
    #     except:
    #         continue
    #     pprint.pprint(stats)
    #     time.sleep(5)
