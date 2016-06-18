import os
import beanstalkc

beanstalk = beanstalkc.Connection(host='localhost', port=11300)

if beanstalk.stats_tube('dev-appointments_sms')['total-jobs']==0:
  os.system('sudo supervisorctl stop fabric:0fabric_appointment_sendsms')
else:
  os.system('sudo supervisorctl restart fabric:0fabric_appointment_sendsms')
