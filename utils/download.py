#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']


if __name__ == '__main__':
    # first two week train data
    for week in range(1, 3):
        mkdir_cmd = "mkdir -p ../../data/train/{}/".format("week{}".format(week))
        print(mkdir_cmd)
        os.system(mkdir_cmd)
        for day in range(0, 5):
            train_link = 'https://archive.ll.mit.edu/ideval/data/1998/training/week{}/{}.tar'.format(week, days[day])
            download_cmd = "wget {} -O ../../data/train/{}/{}.tar".format(train_link, "week{}".format(week), days[day])
            print(download_cmd)
            os.system(download_cmd)
            tar_cmd = "tar -C ../../data/train/{}/ -xvf ../../data/train/{}/{}.tar".format("week{}".format(week), "week{}".format(week), days[day])
            print(tar_cmd)
            os.system(tar_cmd)
            rm_cmd = "rm ../../data/train/week{}/{}.tar".format(week, days[day])
            print(rm_cmd)
            os.system(rm_cmd)

            gzip_cmd = "gzip -d ../../data/train/week{}/{}/tcpdump.gz".format(week, days[day])
            gzip_cmd2 = "gzip -d ../../data/train/week{}/{}/tcpdump.list.gz".format(week, days[day])
            print(gzip_cmd)
            os.system(gzip_cmd)
            print(gzip_cmd2)
            os.system(gzip_cmd2)
    # 3-7 week train data
    for week in range(3, 8):
        for day in range(0, 5):
            mkdir_cmd = "mkdir -p ../../data/train/{}/{}/".format("week{}".format(week), days[day])
            tcpdump_file = 'https://archive.ll.mit.edu/ideval/data/1998/training/week{}/{}/tcpdump.gz'.format(week, days[day])
            label_file = 'https://archive.ll.mit.edu/ideval/data/1998/training/week{}/{}/tcpdump.list.gz'.format(week, days[day])
            print(mkdir_cmd)
            os.system(mkdir_cmd)
            download_tcpdump_cmd = "wget {} -O ../../data/train/{}/{}/tcpdump.gz".format(tcpdump_file, "week{}".format(week), days[day])
            print(download_tcpdump_cmd)
            os.system(download_tcpdump_cmd)
            download_label_cmd = "wget {} -O ../../data/train/{}/{}/tcpdump.list.gz".format(label_file, "week{}".format(week), days[day])
            print(download_label_cmd)
            os.system(download_label_cmd)
            gzip_cmd = "gzip -d ../../data/train/week{}/{}/tcpdump.gz".format(week, days[day])
            print(gzip_cmd)
            os.system(gzip_cmd)
            gzip_cmd2 = "gzip -d ../../data/train/week{}/{}/tcpdump.list.gz".format(week, days[day])
            print(gzip_cmd2)
            os.system(gzip_cmd2)
    for week in range(1, 3):
        for day in range(0, 5):
            gzip_cmd = "gzip -d ../../data/test/week{}/{}/tcpdump.gz".format(week, days[day])
            print(gzip_cmd)
            os.system(gzip_cmd)
            gzip_cmd2 = "gzip -d ../../data/test/week{}/{}/tcpdump.list.gz".format(week, days[day])
            print(gzip_cmd2)
            os.system(gzip_cmd2)
            mkdir_cmd = "mkdir -p ../../data/test/{}/{}".format("week{}".format(week), days[day])
            print(mkdir_cmd)
            os.system(mkdir_cmd)
            # downlaod
            tcpdump_file = 'https://archive.ll.mit.edu/ideval/data/1998/testing/week{}/{}/tcpdump.gz'.format(week, days[day])
            label_file = 'https://archive.ll.mit.edu/ideval/data/1998/testing/week{}/{}/tcpdump.list.gz'.format(week, days[day])
            download_tcpdump_cmd = "wget {} -O ../../data/test/{}/{}/tcpdump.gz".format(tcpdump_file, "week{}".format(week), days[day])
            print(download_tcpdump_cmd)
            os.system(download_tcpdump_cmd)
            download_label_cmd = "wget {} -O ../../data/test/{}/{}/tcpdump.list.gz".format(label_file, "week{}".format(week), days[day])
            print(download_label_cmd)
            os.system(download_label_cmd)



