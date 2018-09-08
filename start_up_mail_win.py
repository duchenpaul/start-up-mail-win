#! /usr/bin/env python3
# -*- coding: utf-8 -*-   
import sys, os, configparser
import cam_cap
import smtplib, urllib.request
import time
import socket, platform

import multiprocessing

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage

# from email.MIMEMultipart import MIMEMultipart  # Python2 
# from email.MIMEText import MIMEText
# from email.MIMEBase import MIMEBase
from email import encoders
import getopt
from os.path import basename

def check_network():
    print("Checking internect connection...")
    while True:
        try:
            result=urllib.request.urlopen('http://baidu.com').read()
            # print(result)
            print("Network is Ready!")
            break
        except Exception as e:
           print(str(e))
           print("Network is not ready,Sleep 5s....")
           time.sleep(5)
    print("Connection is ok!")
    return 0

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def main():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
    except Exception as e:
        print("Error read config file, check config.ini")
        sys.exit(1)

    # check_network()
    p = multiprocessing.Process( target = check_network )
    p.start()
    

    timestamp = time.strftime("%Y-%m-%d %X", time.localtime())
    hostname = socket.gethostname()
    IP_addr=get_ip()

    SMTP_SERVER = config['mail']['SMTP_SERVER']
    fromaddr = config['mail']['fromAddr']
    PASSWORD = config['mail']['PASSWORD']
    toaddr = config['mail']['default_toAddr']

    msg = MIMEMultipart()
     
    # msg["Accept-Language"]="zh-CN"
    # msg["Accept-Charset"]="ISO-8859-1,utf-8"

    msg['Subject'] = 'PC: ' + hostname + ' just logged in'
    # body = ''.join(sys.argv[2]).encode('utf-8')
    body = "{} started at {}, \nIP is {}. \nOS: {} on {}".format(hostname, timestamp, IP_addr, platform.node(), platform.platform())
    body = body.replace('\n', '<br />')

    #msg['Subject'] = "SUBJECT OF THE EMAIL"
    #body = "TEXT YOU WANT TO SEND"

    msg.attach(MIMEText('<html><body>'+ body +'</body></html>','html','utf-8'))
    #msg.attach(MIMEText(body, 'plain'))

    opts, args = getopt.getopt(sys.argv[1:], "f:r:p:")
    # print(opts)
    for op, VALUE in opts:
        if op == '-f':
            FILE_PATH = VALUE
            filename =  basename(FILE_PATH)
            attachment = open(FILE_PATH, "rb")
            
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            
            msg.attach(part)

        elif op == '-p':
            ImgFileName = basename(VALUE)
            print("Attach picture: {}".format(VALUE))
            img_data = open(VALUE, 'rb').read()
            image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
            msg.attach(image)

        elif op == '-r':
            toaddr = VALUE

    VALUE = cam_cap.cam_cap()
    ImgFileName = basename(VALUE)
    print("Attach picture: {}".format(VALUE))
    img_data = open(VALUE, 'rb').read()
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)



    msg['From'] = fromaddr
    msg['To'] = toaddr

    print ("sending mail to: %s" % toaddr)
    print('Subject: {}'.format(msg['Subject']))

    p.join()
    try: 
        server = smtplib.SMTP(SMTP_SERVER)
        server.starttls()
        server.login(fromaddr, PASSWORD)
        text = msg.as_string()
        #print(text)
        server.sendmail(fromaddr, toaddr.split(','), text)
        server.quit()
        #print("Mail sent")
    except Exception as e:
        print('Failed to send mail: '+ str(e))
        sys.exit(1)
    else:
        print("Mail sent")
    finally:
        os.remove(VALUE)

if __name__ == '__main__':
    # https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Multiprocessing
    multiprocessing.freeze_support()
    main()