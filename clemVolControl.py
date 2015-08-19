#!python

from __future__ import print_function
from builtins import input
import dbus
import time
import os

#Open session bus
session_bus=dbus.SessionBus()

#Clementine's player object
try:
    player = session_bus.get_object('org.mpris.clementine','/Player')
    iface = dbus.Interface(player, dbus_interface='org.freedesktop.MediaPlayer')
except:
    print('Clementine is not running.\nStart clementine and run script again!')
    exit(0)

try:
    metadata = iface.GetMetadata()
    print('\nSong: %s, Artist: %s\n' %(metadata['title'], metadata['artist']))
except:
    print('\nNo Song Playing currently.\n')

volume = iface.VolumeGet()
origVol = volume
print('Current volume is %s' %(volume))

print('Current time is -> %s' %(time.strftime('%H:%M:%S'),))

duration = int(input('Sleeping in ? minutes \n'))
print('Do you want to quit Clementine at the end?\n')
y_or_n = input('Y/N?\n')
if y_or_n is 'y' or 'Y' or 'Yes' or 'yes' or 'yeah' or 'Ja, Mein Fuhrer!':
    killClem = True
else:
    killClem = False

reduceBy = volume/duration
reduceBy = reduceBy/4

while volume >= 5:
    iface.VolumeSet(volume)
    volume = volume - reduceBy
    print('Current volume %s' %(iface.VolumeGet()))
    time.sleep(15)

iface.Stop()

#Set volume back to original level for greater pleasure
iface.VolumeSet(origVol)

try:
    if killClem:
        os.system('killall -9 clementine')
except:
    print('Somebody got a little excited and quit clementine at the exact time the volume reached zero.\n')

#TODO:Improve the filthy volume reduction algorithm
#TODO:Allow user to choose interval
#TODO:Qt Interface?
#TODO:Insert interrupt to stop qutting and set volume back to origVolume
#TODO:Option to quit sytem

exit(0)
