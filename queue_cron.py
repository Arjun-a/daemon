import os
import beanstalkc
import logging

FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

cd_dir = '/var/log/'
logging.basicConfig(
                format = FORMAT,
                filename = cd_dir + "daemon.log",
                level = logging.DEBUG
)


beanstalk = beanstalkc.Connection(host='localhost', port=11300)

fab_queues = {
'dev-send_fabric_patient_record' : 'fabric:0fabric_queue_send_patient_record',
'dev-diagnostic_test_csv_process_queue' : 'fabric:0diagnostic_test_csv_upload',
'dev-fabric_mail' : 'fabric:0fabric_appointment_communications',
'dev-push_practice_to_ray' : 'fabric:0fabric_queue_push_practice_to_ray',
'dev-vn_data_parse' : 'fabric:0vn_data_parse',
'dev-ray_update_listener' : 'fabric:0fabric_queue_raypushlistener',
'dev-mobile_verification_sms' : 'fabric:0fabric_sms_verification_queue',
'dev-vn_details_sms' : 'fabric:0fabric_vndetails_sendsms',
'dev-patients_userprofile_sync' : 'fabric:0sync_userprofile_and_patient',
'dev-fabric_notifications' : 'fabric:0fabric_notifications_sendemail',
'dev-doctor_image_resize_queue' : 'fabric:0core_doctor_image_resize',
'dev-practice_pusher' : 'fabric:0fabric_pushtopractics',
'dev-widget_email' : 'fabric:0fabric_widget_mailer',
'dev-qualification_cleanup' : 'fabric:0qualification_cleanup',
'dev-external_roi_dashboard' : 'fabric:0external_roi_generate'
}

for tube in beanstalk.tubes() :
        if fab_queues.has_key(tube) :
                logging.debug('Checking for queue : %s', tube)
                if beanstalk.stats_tube(tube)['total-jobs']==0 :
                        os.system('sudo supervisorctl stop ' + fab_queues[tube])
                        logging.warning('Stopping Worker : %s', fab_queues[tube])
                else:
                        os.system('sudo supervisorctl restart ' + fab_queues[tube])
                        logging.warning('Starting Worker : %s', fab_queues[tube])
