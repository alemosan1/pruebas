	
if [[ "$1" == "cliente" ]]; then
	namefile="cliente$(date +%Y%m%d%H%M)error$2.log"
elif [[ "$1" == "server" ]]; then
	namefile="server$(date +%Y%m%d%H%M)error$2.log"
fi

#Line to get the host IP
echo " IP = " $(hostname -I) > logs/$namefile
while read -r line
do
  newline="[$(date +%Y-%m-%d\ %H:%M:%S:%3N)] $line"
  echo $newline >> logs/$namefile
done
