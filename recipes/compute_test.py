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
path_war = handle.get_path()

handleOld = dataiku.Folder("wearhouse_row_compning_ok_month")
pathOld = handleOld.get_path()

handleDis = dataiku.Folder("dis_row_data")
path_dis = handleDis.get_path()
resultsWerar = "NOT TEST IT YET!"

df = "NOT SET YET!"
tt = "NOT SET YET!"
tt2 = "NOT SET YET!"
disdf = "NOT SET YET!"
distt = "NOT SET YET!"
distt2 = "NOT SET YET!"

color = 'not set yet'

is_pass_open_balance = 1
isPassStatus = 1
isPassDis = 1

total_sum_of_closing_sum_for_old = 0
total_sum_of_open_balnce_for_now = 0

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# get list of email from INBOX folder for your hq.sarc email and it's to the right folder
#TO DO
#-hide email password as variable in dataiku..
def geting_email():
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
def old_check_build():
    project.get_dataset("Rural_Damascus___Warehouse__September_2020__2_").clear(partitions=None)
    project.get_dataset("Rural_Damascus___Warehouse__September_2020__2_").build()
    project.get_dataset("wearhouse_row_compning_ok_month_prepared").build()
    project.get_dataset("test_tarek_month").build()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def war_check_build():
    project.get_dataset("wearhouse_row_data").clear(partitions=None)
    project.get_dataset("wearhouse_row_data").build()
    project.get_dataset("wearhouse_row_data_prepared").build()
    project.get_dataset("wearhouse_row_data_prepared_grouping").build()
    project.get_dataset("wearhous_row_and_month_joined_to_check_openbalne").build()
    project.get_dataset("final_check").build()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def dis_check_build():
    project.get_dataset("dis_row_dataset").clear(partitions=None)
    project.get_dataset("dis_row_dataset").build()
    project.get_dataset("dis_row_dataset_prepared").build()
    project.get_dataset("dis_row_dataset_prepared_by_SubBranch").build()
    project.get_dataset("wearhouse_row_data_prepared_prepared_for_dis").build()
    project.get_dataset("wearhouse_row_data_for_check_wiht_dis").build()
    project.get_dataset("dis_row_dataset_prepared_by_SubBranch_joined").build()
    project.get_dataset("final_check_dis").build()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def color_style(val):
    color = 'white'
    if val == 'false':
        color = 'red'
    elif val == 'ok':
        color = 'grey'

    return 'border-width:2px; background-color :%s' % color

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def old_war_check():
    #geting the need df datafram
    war_to_check = dataiku.Dataset("final_check")
    old_war_df = war_to_check.get_dataframe()

    war_to_check_empty_value = dataiku.Dataset("wearhouse_row_data_prepared")
    empty_war_df = war_to_check_empty_value.get_dataframe()

    #set the variables
    counts_of_check_status_open_balnce = old_war_df['check_status_open_balnce'].value_counts()
    counts_of_check_status = old_war_df['check_status'].value_counts()
    total_sum_of_closing_sum_for_old = old_war_df['old_Closing_Balance_sum'].sum()
    total_sum_of_open_balnce_for_now = old_war_df['Open_Balance_sum'].sum()

    #check that all the items total from previous month is there
    if (total_sum_of_closing_sum_for_old == total_sum_of_open_balnce_for_now):
        is_pass_previosu_month = False
    else:
        is_pass_previosu_month = True

    #you need this for that is there no "ok" in any coulm will consding all the data as
    #bollen and when there is ok all the data type will be string
    if "ok" in counts_of_check_status_open_balnce:
        is_pass_open_balance = 'false' in counts_of_check_status_open_balnce
    else:
        is_pass_open_balance = 0 in counts_of_check_status_open_balnce

    #check for your empty value
    is_pass_war_empty_value = "EMPTY" in empty_war_df[{'Branch_Code','Sub_Branch_code'}]

    #write the results in excel after styling, sorting
    old_war_df.sort_values(by=['check_status_open_balnce','check_status'],ascending=False).style.applymap(color_style, subset=['check_status_open_balnce','check_status']).to_excel(r'%s/results.xlsx' % (path_war), index = False)
    results_war_excel = '%s/results.xlsx' % (path_war)

    return counts_of_check_status_open_balnce, counts_of_check_status, total_sum_of_closing_sum_for_old, total_sum_of_open_balnce_for_now,is_pass_previosu_month, is_pass_open_balance, is_pass_war_empty_value

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
old_war_check()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def dis_check():
    #geting the need df datafram
    dis_to_check = dataiku.Dataset("final_check_dis")
    dis_df = dis_to_check.get_dataframe()

    dis_to_check_empty_value = dataiku.Dataset("dis_row_dataset_prepared")
    empty_dis_df = dis_to_check_empty_value.get_dataframe()

    #set the variables
    counts_of_check_status_dis = dis_df['check_dis_and_total_out'].value_counts()

    #check is wearhouse outcom match with quantity
    is_Pass_Dis = 0 in counts_of_check_status_dis

    #check for your empty value
    is_pass_dis_empty_value = "EMPTY" in empty_dis_df[{'District','SubDistrict','Community','Location','Dis_type','Total Number of Beneficiaries','Beneficiary Condition','Beneficiary condition main','GovCode','DistrictCode','SubDistrictCode','Community Pcode'}]

    #write the results in excel after styling, sorting
    dis_df.sort_values(by='check_dis_and_total_out',ascending=False).style.applymap(color_style, subset='check_dis_and_total_out').to_excel(r'%s/results.xlsx' % (path_dis), index = False)
    results_war_excel = '%s/results.xlsx' % (path_dis)

    return counts_of_check_status_dis, is_Pass_Dis, is_pass_dis_empty_value

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
dis_check()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def sedning_email():
    msg = MIMEMultipart()
    # setup the parameters of the message
    password = "rrpexebvznphgxsp"
    msg['From'] = "hq.sarc.im.ca@gmail.com"
    msg['To'] = str(replyFor)
    msg['Subject'] = "SARC IM AUTO SYSTEM %s" % (subject)

    body = MIMEText("""<style>.email-style{direction: rtl;}</style>
<div class="email-style">
<h2>نتائج الأختبار الأخير: FAILD</h2>

<h3>حركة المستودع:</h3>
<table>
    <tr>
        <td>مجموع الرصيد الشهر الحالي مع الشهر الماضي:</td>
        <td>Faild</td>
    </tr>
    <tr>
        <td> مطابقة الرصيد الأفتتاحي مع الشهر الماضي: </td>
        <td>Faild</td>
    </tr>
    <tr>
        <td>الرصيد الختامي للشهر نفسه: </td>
        <td>Faild</td>
    </tr>
    <tr>
        <td>وجود خلايا فارغة في حركة المستودع:</td>
        <td>Faild</td>
    </tr>
</table>

<h3>إستمارة التوزيع</h3>
<table>
    <tr>
        <td>مطابقة الكمية مع المواد الصادرة:</td>
        <td>Faild</td>
    </tr>
    <tr>
        <td>وجود خلايا فارغة في استمارة التوزيع:</td>
        <td>Faild</td>
    </tr>
</table>


<h4>الخلايا التالية يجب أن لا تكون فارغة في حركة المستودع: </h4>
<ul>
    <li>xx</li>
    <li>xx</li>
</ul>

<h4>الخلايا التالية يجب أن لا تكون فارغة في استمارة التوزيع: </h4>
<ul>
    <li>xx</li>
    <li>xx</li>
    <li>xx</li>
    <li>xx</li>
    <li>xx</li>
</ul>
</div>""", 'html', 'utf-8')

    msg.attach(body)

    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)


    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
sedning_email()