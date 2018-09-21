	
if [[ "$1" == "cliente0" ]]; then
	namefile="cliente$(date +%Y%m%d%H%M)error0.log"
elif [[ "$1" == "cliente1" ]]; then
	namefile="cliente$(date +%Y%m%d%H%M)error1.log"
elif [[ "$1" == "cliente2" ]]; then
	namefile="cliente$(date +%Y%m%d%H%M)error2.log"
elif [[ "$1" == "cliente3" ]]; then
	namefile="cliente$(date +%Y%m%d%H%M)error3.log"
elif [[ "$1" == "cliente4" ]]; then
	namefile="cliente$(date +%Y%m%d%H%M)error4.log"			
elif [[ "$1" == "server0" ]]; then
	namefile="server$(date +%Y%m%d%H%M)error0.log"
elif [[ "$1" == "server1" ]]; then
	namefile="server$(date +%Y%m%d%H%M)error1.log"
elif [[ "$1" == "server2" ]]; then
	namefile="server$(date +%Y%m%d%H%M)error2.log"
elif [[ "$1" == "server3" ]]; then
	namefile="server$(date +%Y%m%d%H%M)error3.log"
elif [[ "$1" == "server4" ]]; then
	namefile="server$(date +%Y%m%d%H%M)error4.log"	
fi

while read -r line
do
  newline="[$(date +%Y-%m-%d\ %H:%M:%S:%3N)] $line"
  echo $newline >> logs/$namefile
done
