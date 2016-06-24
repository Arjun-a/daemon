import os
import re

queue_ = []
workers_ = {}
mapping_ = {}

def fetch_fabric_queues(queue_list):
        file_loc = '/home/vagrant/www/fabric/src/Practo/PractoAppBundle/Queue/AbstractQueue.php'
        file_new = open(file_loc)

        for line in file_new :
                if 'const' in line :
                        xtract = re.findall(r'"(.*?)"', line)
                        print xtract
                        if xtract :
                                queue_list.append(xtract[0])

        for ob in queue_list :
                print ob
        file_new.close()

def fetch_fabric_workers(workers_dict) :
        loc = "/etc/supervisor/conf.d/fabric.conf"
        file_workers = open(loc)

        for line in file_workers :
                if "[program:" in line :
                        worker = re.findall(r"\:([A-Za-z0-9_]+)\]", line)
                        command = next(file_workers)
                        workers_dict[worker[0]] = command

        for keys, values in workers_dict.items() :
                 print (keys),":",(values)
        file_workers.close()

def queue_worker_mapper(queue_list, workers_dict, mapping) :

        i=0
        length = len(queue_list)
        unprocessd = []
        mapp = {}

        while i < length :
                os.chdir('/home/vagrant/www/fabric')
                loc = os.popen(" git grep -i " + queue_list[i] + " | awk -F: '/.php/ {print $1}'| xargs grep 'setName' | awk -F:'|' 'NR==1 {print $1;x=$1} NR>1 {if ($1 != x) {print $1;x=$1}}'").read()
                loc = loc.rstrip()
                print "Processing %s" % queue_list[i]
                try:
                        file_new = open(loc, "r")
                except:
                        print "Queue Unprocessed %s" % queue_list[i]
                        unprocessd.append(queue_list[i])
                        i = i + 1
                        print "--------------------"
                        print ""
                        continue
                for line in file_new :
                        if "setName" in line :
                                hit_line = line
                                hit_line = hit_line.rstrip()
                                extract = re.findall(r"'(.*?)'", hit_line, re.DOTALL)
                                if extract :
                                        print queue_list[i] ,":",extract[0]
                                        mapp[queue_list[i]] = extract[0]
                i = i + 1
                print "-------------------"
                print ""

                file_new.close()



        for a,b in mapp.items() :
                print a, ":", b


        for key,val in mapp.items() :
                for keys,values in workers_dict.items() :
                        if mapp[key] in values :
                                mapping['dev-' + key] = 'fabric:0' + keys

        print 'The mapping is as follows :'
        for k,v in mapping.items() :
                print k , ":", v, ","




fetch_fabric_queues(queue_)
fetch_fabric_workers(workers_)
queue_worker_mapper(queue_, workers_, mapping_)
