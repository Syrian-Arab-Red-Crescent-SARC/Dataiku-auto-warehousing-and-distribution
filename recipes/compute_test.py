# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def rdSystem():
    # get list of email subjects from INBOX folder
    with MailBox('imap.gmail.com').login('hq.sarc.im.ca@gmail.com', 'rrpexebvznphgxsp') as mailbox:
        for msg in mailbox.fetch(A(seen=False)):
            #print(msg)
            #print(msg.from_)
            replyFor= msg.from_
            subject = msg.subject
            for att in msg.attachments:
                #print(att.filename, att.content_type)
                #chcek old wearhouse data
                if "old" in att.filename.lower() :
                    with open('{}/{}'.format(pathOld, att.filename.replace(att.filename, "old_data.xlsx")), 'wb') as f:
                        f.write(bytearray(att.payload))
                        #JobBuildCode()
                        dataset_old1 = project.get_dataset("Rural_Damascus___Warehouse__September_2020__2_").clear(partitions=None)
                        dataset_old1 = project.get_dataset("Rural_Damascus___Warehouse__September_2020__2_").build()
                        dataset_old2 = project.get_dataset("wearhouse_row_compning_ok_month_prepared").build()
                        dataset_old4 = project.get_dataset("test_tarek_month").build()


                elif  "war" in att.filename.lower():

                    #check wearhous
                    with open('{}/{}'.format(path, att.filename.replace(att.filename, "warehouse15.xlsx")), 'wb') as f:
                        f.write(bytearray(att.payload))
                        #JobBuildCode()
                        dataset1 = project.get_dataset("wearhouse_row_data").clear(partitions=None)
                        dataset1 = project.get_dataset("wearhouse_row_data").build()
                        dataset2 = project.get_dataset("wearhouse_row_data_prepared").build()
                        dataset3 = project.get_dataset("wearhouse_row_data_prepared_grouping").build()
                        #dataset4 = project.get_dataset("test_tarek_month").build()
                        dataset5 = project.get_dataset("wearhous_row_and_month_joined_to_check_openbalne").build()
                        dataset6 = project.get_dataset("final_check").build()

                        #doen build for wearhuse and old wearhouse dataset
                        #check_data_for_final_check
                        dataset_to_check = dataiku.Dataset("final_check")
                        df = dataset_to_check.get_dataframe()
                        #df.head(1000)


                        #write to excel
                        df.to_excel(r'%s/results.xlsx' % (path), index = False)
                        file = '%s/results.xlsx' % (path)




                        tt = df['check_status_open_balnce'].value_counts()
                        total_sum_of_Closing_sum_for_old = df['old_Closing_Balance_sum'].sum()
                        total_sum_of_open_balnce_for_now = df['Open_Balance_sum'].sum()
                        tt2 = df.to_html()
                        ttForStusts = df['check_status'].value_counts()

                        if "ok" in tt:
                            isPassOpenBalnce = "False" in tt
                        else:
                            isPassOpenBalnce = 0 in tt

                        isPassStatus = 0 in ttForStusts
                        #check dis files
                elif  "dis" in att.filename.lower() :

                    #check dis
                    with open('{}/{}'.format(pathDis, att.filename.replace(att.filename, "dis.xlsx")), 'wb') as f:
                        f.write(bytearray(att.payload))
                        #JobBuildCode()
                        datasetDis1 = project.get_dataset("dis_row_dataset").clear(partitions=None)
                        datasetDis1 = project.get_dataset("dis_row_dataset").build()
                        datasetDis2 = project.get_dataset("dis_row_dataset_prepared").build()
                        datasetDis3 = project.get_dataset("dis_row_dataset_prepared_by_SubBranch").build()
                        datasetDis5 = project.get_dataset("wearhouse_row_data_prepared_prepared_for_dis").build()
                        datasetDis6 = project.get_dataset("wearhouse_row_data_for_check_wiht_dis").build()
                        datasetDis7 = project.get_dataset("dis_row_dataset_prepared_by_SubBranch_joined").build()
                        datasetDis8 = project.get_dataset("final_check_dis").build()

                        #doen build for wearhuse and old wearhouse dataset

                        #check_data_for_final_check
                        dataset_to_check_for_dis = dataiku.Dataset("final_check_dis")
                        disdf = dataset_to_check_for_dis.get_dataframe()
                        #df.head(1000)

                        distt = disdf['check_dis_and_total_out'].value_counts()
                        distt2 = disdf.to_html()

                        isPassDis = 0 in distt

                        disdf.to_excel(r'%s/results.xlsx' % (pathDis), index = False)
                        file2 = '%s/results.xlsx' % (pathDis)

            else:
                print("nothing to show here")



                        #check if resulewaere faild or susceed
            if isPassOpenBalnce or isPassStatus  :
                resultsWerar = "FAILED"

                            #print("\nThis value exists in Dataframe")

            elif isPassStatus or isPassDis:
                resultsWerar = "FAILED"

            elif total_sum_of_Closing_sum_for_old != total_sum_of_open_balnce_for_now:
                resultsWerar = "FAILED"

            else:
                resultsWerar = "SUCCEED"
                finalBuild = project.get_dataset("wearhouse_row_data_prepared_check_ok").build()
                finalBuild = project.get_dataset("dis_row_dataset_prepared_to_ready_to_collect").build()


                  #print("\nThis value does not exists in Dataframe")

            msg = MIMEMultipart()


            # setup the parameters of the message
            password = "rrpexebvznphgxsp"
            msg['From'] = "hq.sarc.im.ca@gmail.com"
            msg['To'] = str(replyFor)
            #msg['To'] = "hq.sarc.im.ca@gmail.com"
            msg['Cc'] = "tarepsh@gmail.com"
            msg['Subject'] = "SARC RD IM AUTO SYSTEM %s" % (subject)


            body = MIMEText("<h3>your last test is: </h3>" + str(resultsWerar) + "<br>" +
                                str(tt) + "<br> your total sum of closing balacne is:" + str(total_sum_of_Closing_sum_for_old) + "</br> </br>"
                                "And you total  sum of open balcnce is: " + str( total_sum_of_open_balnce_for_now) + "<br> your dis data is" + str(distt)
                                 + "<br>", 'html', 'utf-8')
            msg.attach(body)
            # attach image to message body
            fp = open(file, 'rb')
            part = MIMEBase('application','vnd.ms-excel')
            part.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename='results_w.xlsx')

            fp2 = open(file2, 'rb')
            part2 = MIMEBase('application','vnd.ms-excel')
            part2.set_payload(fp2.read())
            fp2.close()
            encoders.encode_base64(part2)
            part2.add_header('Content-Disposition', 'attachment', filename='results_d.xlsx')

            msg.attach(part)
            msg.attach(part2)
            # create server
            server = smtplib.SMTP('smtp.gmail.com: 587')

            server.starttls()

            # Login Credentials for sending the mail
            server.login(msg['From'], password)


            # send the message via the server.
            server.sendmail(msg['From'], msg['To'], msg.as_string())

            server.quit()



schedule.every(1).minutes.do(rdSystem)

while True:
    schedule.run_pending()
    time.sleep(1)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
# import necessary packages

import dataiku
import pandas as pd, numpy as np
import logging
import time
import os
import schedule
import time
import smtplib, ssl

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

from dataiku import pandasutils as pdu
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from imap_tools import MailBox, AND, A

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# define the variable

client = dataiku.api_client()
project = client.get_project("SARC_HQ2")
handle = dataiku.Folder("row_wearhouse_reports")
path = handle.get_path()

handleOld = dataiku.Folder("wearhouse_row_compning_ok_month")
pathOld = handleOld.get_path()

handleDis = dataiku.Folder("dis_row_data")
pathDis = handleDis.get_path()
resultsWerar = "NOT TEST IT YET!"

df = "NOT SET YET!"
tt = "NOT SET YET!"
tt2 = "NOT SET YET!"
disdf = "NOT SET YET!"
distt = "NOT SET YET!"
distt2 = "NOT SET YET!"

isPassOpenBalnce = 1
isPassStatus = 1
isPassDis = 1

total_sum_of_closing_sum_for_old = 0
total_sum_of_open_balnce_for_now = 0

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# get list of email from INBOX folder for your hq.sarc email and it's to the right folder
#TO DO
#-hide email password as variable in dataiku..
def getingEmail():
    with MailBox('imap.gmail.com').login('hq.sarc.im.ca@gmail.com', 'rrpexebvznphgxsp') as mailbox:
        if mailbox.fetch(A(seen=False)):
            for msg in mailbox.fetch(A(seen=False)):
                replyFor= msg.from_
                subject = msg.subject
                if msg.attachments:
                    for att in msg.attachments:
                        if "old-hq" in att.filename.lower():
                            with open('{}/{}'.format(pathOld, att.filename.replace(att.filename, "old_data.xlsx")), 'wb') as old:
                                old.write(bytearray(att.payload))
                        elif "war" in att.filename.lower():
                            with open('{}/{}'.format(path, att.filename.replace(att.filename, "warehouse15.xlsx")), 'wb') as war:
                                war.write(bytearray(att.payload))
                        elif  "dis" in att.filename.lower() :
                            with open('{}/{}'.format(pathDis, att.filename.replace(att.filename, "dis.xlsx")), 'wb') as dis:
                                dis.write(bytearray(att.payload))
                        else:
                            return "هنالك خطأ في الملفات المرفقة"
                return "لا يوجد مرفقات في الرسالة الإلكترونية الحالية"

        else:
            return "لا يوجد رسائل جديدة"

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def oldCheckBuild():
    project.get_dataset("Rural_Damascus___Warehouse__September_2020__2_").clear(partitions=None)
    project.get_dataset("Rural_Damascus___Warehouse__September_2020__2_").build()
    project.get_dataset("wearhouse_row_compning_ok_month_prepared").build()
    project.get_dataset("test_tarek_month").build()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def warCheckBuild():
    project.get_dataset("wearhouse_row_data").clear(partitions=None)
    project.get_dataset("wearhouse_row_data").build()
    project.get_dataset("wearhouse_row_data_prepared").build()
    project.get_dataset("wearhouse_row_data_prepared_grouping").build()
    project.get_dataset("wearhous_row_and_month_joined_to_check_openbalne").build()
    project.get_dataset("final_check").build()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def disCheckBuild():
    project.get_dataset("dis_row_dataset").clear(partitions=None)
    project.get_dataset("dis_row_dataset").build()
    project.get_dataset("dis_row_dataset_prepared").build()
    project.get_dataset("dis_row_dataset_prepared_by_SubBranch").build()
    project.get_dataset("wearhouse_row_data_prepared_prepared_for_dis").build()
    project.get_dataset("wearhouse_row_data_for_check_wiht_dis").build()
    project.get_dataset("dis_row_dataset_prepared_by_SubBranch_joined").build()
    project.get_dataset("final_check_dis").build()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def oldWarCheck():
    dataset_to_check = dataiku.Dataset("final_check")
    df = dataset_to_check.get_dataframe()
    #df2 = df.style.applymap(lambda v: 'color:white;background-color:darkblue;' if (df.chcek == "false") else None )
    return df

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def oldWarCheck():
    dataset_to_check = dataiku.Dataset("final_check")
    df = dataset_to_check.get_dataframe()
    def style_negative(v, props=''):
        return props if v < 0 else None
    s2 = df.style.applymap(style_negative, props='color:red;')\
                  .applymap(lambda v: 'opacity: 20%;' if (v <= 0.3) and (v >= -0.3) else None)
    return s2

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
oldWarCheck()