import os
import pysftp


def generateTime(keyList, startIndex, photoList, duration):
    maxSec = keyList[startIndex]
    minSec = keyList[startIndex] - duration
    needDownload = []
    breakPoint = 1000000000000
    for key in keyList:
        if key > minSec:
            needDownload.append(photoList[key])
            if breakPoint > key:
                breakPoint = key
    return needDownload, keyList.index(breakPoint)


today = '20210919'
caseName = 'DH15_V40_FALL'
fileExtendName = 'jpg'
timeDuration = 900

ip = '192.168.43.151'
port_ = 2222
username_ = 'admin'
password_ = 'admin'
mobilePath = 'SDCard/DCIM/Camera'


os.mkdir(caseName)
os.chdir(caseName)

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
with pysftp.Connection(ip, port=port_, username=username_, password=password_, private_key=".ppk", cnopts=cnopts) as sftp:
    with sftp.cd(mobilePath):
        photos = sftp.listdir()
        photoList = {}
        for photo in photos:
            if photo.split('.')[1] == fileExtendName:
                name = photo.split('.')[0]
                if name.split('_')[1] == today:
                    clock = name.split('_')[2]
                    second = int(clock[:2]) * 3600 + \
                        int(clock[2:4]) * 60 + int(clock[4:])
                    photoList[second] = photo

        keyList = photoList.keys()
        keyList = sorted(keyList, reverse=True)
        startIndex = 0
        needDownload, breakPointIndex = generateTime(
            keyList, startIndex, photoList, timeDuration)
        # print(breakPointIndex)

        count = 0
        for file in needDownload:
            print('Downloading...(%d / %d)' %
                  (count + 1, breakPointIndex + 1), end="\r")
            sftp.get(file)
            count += 1
