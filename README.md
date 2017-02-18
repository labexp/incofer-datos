# incofer-datos
Datos (Abiertos) para generar un GTFS del servicio de Incofer


Los datos que publica el Incofer son muy problemáticos, por ejemplo los horarios varían sin previo aviso. Además la información es compartida en imágenes lo que dificulta poder reutilizar la información en otras aplicaciones. (Nota: antes de las imágenes los horarios eran compartidos en archivos PDF...)

Este repositorio es para compartir scripts para convertir los horarios del servicio de Tren Urbano publicadas por el Incofer en su página web (http://www.incofer.go.cr) a un formato que pueda ser utilizado por el script osm2gtfs (https://github.com/grote/osm2gtfs).


La carpeta *pdf* incluye un script realizado para parsear los antiguos archivos en PDF publicados por el Incofer. Se mantiene en el repositorio por si acaso el Incofer vuelve a publicar horarios en PDF. 
