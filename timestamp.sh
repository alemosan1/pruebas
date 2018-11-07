# TODO: En el nombre de los ficheros del sevidor, se puede dejar sólo el unique_id y quitar el date, 
# porque sólo se va a crear un log por sesion.
# Pero el del cliente, hay que ponerlo porque pueden haber varios clientes por sesion 
# Esto en nuestro ejemplo, porque los logs se crean en la misma máquina y se pueden machacar. 
# En un ejemplo real, no se machacan pues serían hosts diferentes.
# También puede ocurrir que el cliente se conecte a la misma sesión más de una vez. 
# Entonces se crearían los logs con el mismo nombre, si no ponemos el date.
if [[ "$1" == "cliente" ]]; then
	namefile="cliente$(date +%d%m%Y%H%M%S)_$3_Err$2.log" 
elif [[ "$1" == "server" ]]; then
	namefile="server$(date +%d%m%Y%H%M%S)_$3_Err$2.log" 
fi # Más adelante, quitaremos el núm error del nombre.

# Line to get the host IP
echo " IP = " $(hostname -I) > /home/bayes/Repositories/pruebas/logs/$namefile
while read -r line
do
  newline="[$(date +%Y-%m-%d\ %H:%M:%S:%3N)] $line"
  echo $newline >> /home/bayes/Repositories/pruebas/logs/$namefile
done
