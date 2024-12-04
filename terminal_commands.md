
## windows

copy data from windows to remote server 
scp -i .\id_rsa -r ./data srv-cpllnijgbbvc738qha7g@ssh.oregon.render.com:/app

ssh -i .\id_rsa srv-cpllnijgbbvc738qha7g@ssh.oregon.render.com
ssh-keygen -t rsa -b 1024 -C "raulest50@gmail.com" -f ./id_rsa