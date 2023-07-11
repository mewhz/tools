import re
import datetime
import os
import sys

content = open('HostReport.html', encoding='utf8').read()

args = sys.argv

current_year_month_day = ''
current_hour_minuter_second = ''

if len(args) != 3:
    current_year_month_day = datetime.datetime.now().strftime('%Y-%m-%d')
    current_hour_minuter_second = datetime.datetime.now().strftime('%H:%M:%S')

    print("使用系统当前时间: " + current_year_month_day + " " + current_hour_minuter_second)

else:
    try:
        current_year_month_day = datetime.datetime.strptime(args[1], '%Y-%m-%d').strftime('%Y-%m-%d')
        current_hour_minuter_second = datetime.datetime.strptime(args[2], '%H:%M:%S').strftime('%H:%M:%S')
        print("使用自定义时间：" + current_year_month_day + " " + current_hour_minuter_second)
    except ValueError:
        current_year_month_day = datetime.datetime.now().strftime('%Y-%m-%d')
        current_hour_minuter_second = datetime.datetime.now().strftime('%H:%M:%S')
        print("输入的时间格式有误, 改为使用系统当前时间：" + current_year_month_day + " " + current_hour_minuter_second)

scan_time = ()

start_scan_time_string = datetime.datetime.strptime(current_year_month_day + " " + current_hour_minuter_second,
                                                    '%Y-%m-%d %H:%M:%S')
end_scan_time_string = datetime.datetime.strptime(current_year_month_day + " " + current_hour_minuter_second,
                                                  '%Y-%m-%d %H:%M:%S')

scan_time_regex = "<tr><th style='width:20%' class='text-center header-font'>扫描时间</th><td class='text-left " \
                  "text-font'>(.*?)</td></tr>"

scan_hour_minuter_second_regex = "(.*?)小时(.*?)分(.*?)秒"

scan_day_hour_minuter_second_regex = "(.*?)天(.*?)小时(.*?)分(.*?)秒"

evaluate_time_regex = "<td class='text-right'>评估时间：</td><td class='text-left'>(.*?)</td></tr>"

task_name_regex = "<tr><th style='width:20%' class='text-center header-font'>任务名称</th><td class='text-left " \
                  "text-font'>(.*?)</td></tr>"

start_scan_time_regex = "<tr><th style='width:20%' class='text-center header-font'>开始扫描时间</th><td class='text-left " \
                        "text-font'>(.*?)</td></tr>"

end_scan_time_regex = "<tr><th style='width:20%' class='text-center header-font'>结束扫描时间</th><td class='text-left " \
                      "text-font'>(.*?)</td></tr><tr>"


def init():
    global scan_time, start_scan_time_string

    scan_time_string = re.findall(scan_time_regex, content)[0]

    if scan_time_string.find("天") != -1:
        scan_time = re.findall(scan_day_hour_minuter_second_regex, scan_time_string)[0]
    else:
        scan_time = re.findall(scan_hour_minuter_second_regex, scan_time_string)[0]

    if len(scan_time) == 3:
        scan_time_timedelta = datetime.timedelta(hours=int(scan_time[0]), minutes=int(scan_time[1]),
                                                 seconds=int(scan_time[2]))
    else:
        scan_time_timedelta = datetime.timedelta(days=int(scan_time[0]), hours=int(scan_time[1]),
                                                 minutes=int(scan_time[2]), seconds=int(scan_time[3]))

    start_scan_time_string = start_scan_time_string - scan_time_timedelta


def update_scan_time(contents):
    start_scan_time = re.findall(start_scan_time_regex, contents)[0]
    start_scan_time_old_string = "<tr><th style='width:20%' class='text-center header-font'>开始扫描时间</th><td " \
                                 "class='text-left text-font'>" + start_scan_time + "</td></tr>"
    start_scan_time_new_string = "<tr><th style='width:20%' class='text-center header-font'>开始扫描时间</th><td " \
                                 "class='text-left text-font'>" + str(start_scan_time_string) + "</td></tr>"

    contents = contents.replace(start_scan_time_old_string, start_scan_time_new_string)

    end_scan_time = re.findall(end_scan_time_regex, contents)[0]
    end_scan_time_old_string = "<tr><th style='width:20%' class='text-center header-font'>结束扫描时间</th><td " \
                               "class='text-left text-font'>" + end_scan_time + "</td></tr><tr>"
    end_scan_time_new_string = "<tr><th style='width:20%' class='text-center header-font'>结束扫描时间</th><td " \
                               "class='text-left text-font'>" + str(end_scan_time_string) + "</td></tr><tr>"

    contents = contents.replace(end_scan_time_old_string, end_scan_time_new_string)

    return contents


init()


evaluate_time = re.findall(evaluate_time_regex, content)[0]
evaluate_time_old_string = "<td class='text-right'>评估时间：</td><td class='text-left'>" + evaluate_time + "</td></tr>"
evaluate_time_new_string = "<td class='text-right'>评估时间：</td><td class='text-left'>" + current_year_month_day + "</td></tr>"

content = content.replace(evaluate_time_old_string, evaluate_time_new_string)

task_name = re.findall(task_name_regex, content)[0]
task_name_time = task_name[0:(len(task_name) - 19)] + str(start_scan_time_string)
task_name_old_string = "<tr><th style='width:20%' class='text-center header-font'>任务名称</th><td class='text-left " \
                       "text-font'>" + task_name + "</td></tr>"
task_name_new_string = "<tr><th style='width:20%' class='text-center header-font'>任务名称</th><td class='text-left " \
                       "text-font'>" + task_name_time + "</td></tr>"

title_name_old_string = "<TITLE>" + task_name + "</TITLE>"
title_name_new_string = "<TITLE>" + task_name_time + "</TITLE>"

content = content.replace(task_name_old_string, task_name_new_string)
content = content.replace(title_name_old_string, title_name_new_string)

content = update_scan_time(content)

open('HostReport.html', 'w', encoding='utf-8').write(content)


def update_targets(file_name):
    target_content = open(file_name, encoding='utf=8').read()

    target_content = target_content.replace(evaluate_time_old_string, evaluate_time_new_string)

    target_content = update_scan_time(target_content)

    open(file_name, 'w', encoding='utf-8').write(target_content)


def read_file_list():
    path = "targets"

    for file_name in os.listdir(path):
        if file_name.find('.html') != -1:
            update_targets(path + "/" + file_name)


read_file_list()
