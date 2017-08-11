# lighttpd-parser

Intro: Parse a lighttpd access log.
Author: Linkai Qi
Reference: https://github.com/joepie91/lighttpdparse

### usage:
    $python parse-dotqoo.py [-h] [-a] [-m MINIMUM] logfile [logfile ...]
    eg. $python parse-dotqoo.py -a
        $python parse-dotqoo.py ./access_1.log ./access_2.log

### positional arguments:
    logfile     path(s) of the logfile(s)

### optional arguments:
    -h, --help  show this help message and exit
    -a, --auto  get the access.log file from default directory
              /var/log/lighttpd/access.log
    -m MINIMUM  the counting threshold that has to be exceeded to display the
              entry

### Output / Generated files:
- stdout: Top OS, Top browser base, Top manufacturer, Top 20 request hostname
    For more details please check 'hostname', 'info_table' and 'conn_timestamp' located in the same directory

- conn_timestamp.txt: 包含所有设备访问时间与时长
- hostname.txt: lighttpd AccessLog 所有请求过的hostname以及其请求次数，按从高到低排序
- info_table.txt: IP的地址（用户）的详细信息。包含OS系统版本，浏览器内核，设备品牌机型，与系统版本号build信息
- unparseable_log.txt: 储存parse-dotqoo.py程序无法识别的log

### Sample output:
```
Detected total 436 devices

Top OS:
87 Android 5.1     19.95 %
76 Android 6.0.1   17.43 %
65 Android 5.1.1   14.91 %
48 Android 4.4.4   11.01 %
44 Android 6.0     10.09 %
21 Android 5.0.2   4.82 %
20 Android 4.4.2   4.59 %
13 UNIDENTIFIED    2.98 %
12 Android 4.3     2.75 %
9 Android 7.0     2.06 %
5 Android 5.0     1.15 %
5 Android 4.2.2   1.15 %
4 iOS 6.0         0.92 %
3 iOS 7.1.2       0.69 %
2 iOS 10.2.1      0.46 %
2 Android 4.4     0.46 %
2 Android 4.1.2   0.46 %
2 iOS 10.3.2      0.46 %
2 Android 5.0.1   0.46 %
1 iOS 10.0.2      0.23 %
1 iOS 7.0         0.23 %
1 iOS 10.0        0.23 %
1 Android 2.3.6   0.23 %
1 iOS 9.2         0.23 %
1 iOS 9.1         0.23 %
1 iOS 8.3         0.23 %
1 iOS 8.1         0.23 %
1 iOS 10.3.1      0.23 %
1 iOS 9.3.1       0.23 %
1 iOS 9.3.2       0.23 %
1 Android 4.1.1   0.23 %
1 Android 4.0.4   0.23 %
1 Android 4.2.1   0.23 %

Top base:
261 Dalvik/2.1.0    59.86 %
79 Mozilla/5.0     18.12 %
73 Dalvik/1.6.0    16.74 %
17 UNIDENTIFIED    3.90 %
2 Mozilla/        0.46 %
2 Dalvik/v1.1.47  0.46 %
1 Dalvik/         0.23 %
1 Dalvik/1.4.0    0.23 %

Top manufacturer:
108 vivo            24.77 %
84 OPPO            19.27 %
21 Apple           4.82 %
19 UNIDENTIFIED    4.36 %
15 HUAWEI          3.44 %
12 Lenovo          2.75 %
10 Redmi           2.29 %
8 Coolpad         1.83 %
7 MI              1.61 %
6 A31             1.38 %
4 HM              0.92 %
4 ZTE             0.92 %
3 GN9012          0.69 %
3 TCL             0.69 %
3 GN5001S         0.69 %
3 CHM-TL00H       0.69 %
3 F100            0.69 %
3 m3              0.69 %
3 EVA-AL00        0.69 %
3 ALE-TL00        0.69 %
2 GN8003          0.46 %
2 2014813         0.46 %
2 CUN-TL00        0.46 %
2 M5              0.46 %
2 R831S           0.46 %
2 HTC             0.46 %
2 CAM-TL00        0.46 %
2 ATH-AL00        0.46 %
2 KIW-TL00        0.46 %
2 F103            0.46 %
2 BLN-AL10        0.46 %
2 m2              0.46 %
2 Nexus           0.46 %
2 Le              0.46 %
2 GN5001          0.46 %
2 A11             0.46 %
2 A31c            0.46 %
2 G621-TL00       0.46 %
2 F100S           0.46 %
2 NEM-AL10        0.46 %
1 SM-G3559        0.23 %
1 GN9010          0.23 %
...

Top 20 host:
80866 dc.51y5.net                        
36883 search.video.iqiyi.com             
36748 szextshort.weixin.qq.com           
33670 mtrace.qq.com                      
31040 short.weixin.qq.com                
28547 dns.weixin.qq.com                  
24103 msg.71.am                          
20847 btrace.qq.com                      
19732 c-adash.m.taobao.com               
18274 pdata.video.qiyi.com               
16964 dldir1.qq.com                      
13663 msg.iqiyi.com                      
13491 szshort.weixin.qq.com              
13374 -                                  
10609 hot.vrs.sohu.com:80                
9976 irs01.com                          
9235 cgicol.amap.com                    
8967 lepodownload.mediatek.com          
8847 g3.letv.com                        
8148 amdc.m.taobao.com                  

For more details please check 'hostname', 'info_table' and 'conn_timestamp' located in the current directory
```
**END OF FILE**
