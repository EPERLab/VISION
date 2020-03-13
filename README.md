

##### Universidad de Costa Rica
##### Escuela de Ingeniería Eléctrica
##### Laboratorio de Investigación en Potencia y Energía (EPER-Lab)
&nbsp;

# Plugin VISION
Este plugin tiene permite observar los resultados de las simulaciones realizadas con ayuda de los análisis realizados con QGIS2RunOpenDSS. Esta herramienta tiene como fin demostrarle al usuario el estado de la red de distribución, basándose en los niveles de tensión y flujos de potencia según los resultados de las simulaciones realizadas. De igual manera la herramienta presenta la factibilidad de poder analizar datos reales y no solo datos obtenidos a partir de simulaciones.

VISION posee cuatro medios de visualización para los correspondientes estudios y análisis de los componentes de la red de distribución. La herramienta dispone de clasificación individual de puntos (siendo estos símbolos barras o transformadores) según sea su nivel de tensión, analizando el mismo atributo de tensión la herramienta crea heatmaps con el fin de demostrar por zonas los niveles de tensión de la red, también posee un clasificador de líneas de BT y MT según sea su flujo de potencia y la ampacidad del conductor; por último, crea animaciones con base al comportamiento de la red durante un lapso de tiempo dentro de los análisis diarios.

Hay que recalcar la necesidad de que la capa a analizar sea previamente simulada por la herramienta QGIS2RunOpenDSS, esta es la encargada de generar los valores y atributos necesarios para la visualización del estado de la red. Agregar, que cada tipo de renderizado se va realizar solamente sobre la capa actualmente escogida por el usuario 

***

