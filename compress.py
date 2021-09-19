import os

os.chdir('/run/media/smilemax/Data/lzx/image')
folders = os.listdir('/run/media/smilemax/Data/lzx/image')
for folder in folders:
    try:
        os.chdir(folder)
        os.chdir('/run/media/smilemax/Data/lzx/image')
    except NotADirectoryError:
        continue
    print('Compressing ' + str(folder) + '...')
    os.system('tar -zcPf ' + '/run/media/smilemax/Data/lzx/image_compress/' +
              folder + '.tar.gz' + ' ' + '/run/media/smilemax/Data/lzx/image/' + folder)
