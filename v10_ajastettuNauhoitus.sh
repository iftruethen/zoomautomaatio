#!/bin/bash

ke="e"
while [ $ke != "k" ]
do
    echo "Anna nauhoituksen aloitusaika muodossa [HH:MM]:"
    read aloitusaika
    aloitusaika=$( date --date $aloitusaika +%s )
    # kysytään onko alkuajankohta oikein
    echo "Aloitetaanko nauhoitus $(date -d @$aloitusaika)? k/e"
    read ke
done

# kysytään meetinkitiedot
printf "\nAnna kokouskoodi:\n"
read kokousID
printf "\nAnna kokoussalasana:\n"
read kokousPW
printf "\nOK, nauhoitus ajastettu\n"

# näytön reso oikeaksi
xrandr -s 1360x768

# odotetaan alkua
while (($(date +%s)<$aloitusaika))
do
	sleep 5
done

# "join a meeting"
pkill -f zoom
zoom &
sleep 5
ikkunaId=$(wmctrl -l | grep -i "zoom")
ikkunaId=${ikkunaId:0:10}
xdotool windowactivate $ikkunaId
xdotool key Tab
xdotool key Return
sleep 1

#syötetään meetinkikoodi
ikkunaId=$(wmctrl -l | grep -i "zoom" | grep -iv "cloud")
ikkunaId=${ikkunaId:0:10}
ikkunaDec=${ikkunaId:2:10}
ikkunaDec=$((16#$ikkunaDec))
xdotool windowactivate $ikkunaDec; # aktivoi ikkunan
xdotool key Tab
xdotool key Tab
xdotool type --window $ikkunaDec --delay 5 $kokousID; # syöttää kokoustunnuksen
xdotool key Return;
sleep 3;
iserror=$(wmctrl -l | grep -i "leave mee")
if [ ${#iserror} != 0 ] # cathcaa mahdollisen "invalid meeting ID":n
then
	xdotool windowactivate ${iserror:0:10}
	xdotool key Tab
	xdotool key Tab
	xdotool key Tab
	xdotool key Return
fi
sleep 3;
if [ ${#kokousPW} != 0 ]
then
	xdotool type --window $ikkunaDec --delay 5 $kokousPW
	xdotool key --window $ikkunaDec Return
	sleep 2;
fi
xdotool key --window $ikkunaDec Return

nohup obs --startrecording &>/dev/null &
sleep 5
ikkunaId2=$(wmctrl -l | grep -i "obs")
ikkunaId2=${ikkunaId:0:10}
xdotool windowminimize $ikkunaId2
sleep 5
ikkunaId=$(wmctrl -l | grep -i "zoom meeting")
ikkunaId=${ikkunaId:0:10}
xdotool windowactivate $ikkunaId
xdotool windowsize $ikkunaId 95% 95%
xdotool windowmove $ikkunaId 0 0