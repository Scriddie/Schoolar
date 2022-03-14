rm log.txt
sudo systemctl stop apache2;
sudo systemctl start apache2;
# apache2 -f /etc/apache2/apache2.conf -k stop;
# wait 10;
# apache2 -f /etc/apache2/apache2.conf -k start;
