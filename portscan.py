import telnetlib
import argparse
import threading

portlist = [8, 21, 22, 23, 53, 80, 111, 139, 161, 389, 443, 445, 1025, 1433, 1521, 3128, 3306, 3311, 3312, 3389,
            5432, 5900, 7001, 7002, 8000, 8080, 8081, 8090, 9000, 9090,9091, 8888, 9200, 9300, 10000, 921,9210]
lock=threading.Lock()


def scan(ip, portlist):
    lock.acquire()
    print(ip)
    print('PORT     STATE')
    for port in portlist:
        s = telnetlib.Telnet()
        try:
            s.open(ip, port, timeout=2)
            print('%-8s open' % (port))
        except Exception as err:
            pass
        finally:
            s.close()
    lock.release()

if __name__ == '__main__':
    print(r'''
                  _
 _ __   ___  _ __| |_ ___  ___ __ _ _ __
| '_ \ / _ \| '__| __/ __|/ __/ _` | '_ \
| |_) | (_) | |  | |_\__ \ (_| (_| | | | |
| .__/ \___/|_|   \__|___/\___\__,_|_| |_|
|_|                        by:zjun
                        www.zjun.info
          ''')
    parser = argparse.ArgumentParser(description='The script is portscan')
    parser.add_argument('-i', '--ip', required=False, help='target ip')
    parser.add_argument('-f', '--file', required=False, help='target ipfile')
    parser.add_argument('-p', '--port', required=False, help='target port')
    args = parser.parse_args()
    ip = args.ip
    file = args.file
    port = args.port
    if port == None:
        portlist = portlist
    else:
        if port:
            if ',' in port:
                portlist = port.split(',')
            elif '-' in port:
                portlist = port.split('-')
            tmpportlist = []
            [tmpportlist.append(i) for i in range(int(portlist[0]), int(portlist[1]) + 1)]
            portlist = tmpportlist
    if file == None and ip != None:
        threading.Thread(target=scan,args=(ip,portlist)).start()
    elif file != None and ip==None:
        with open (file,'r') as f:
            for ip in f.readlines():
                ip =ip.strip('\n')
                threading.Thread(target=scan,args=(ip,portlist)).start()
    else:
      print('usage: portscan.py [-h] [-i IP] [-f FILE]')