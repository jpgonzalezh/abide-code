# Instalación de ANTs (Advance Normalization Tools) 

Pasos a seguir para realizar la instalación de ANTs en PC con sistema operativo Fedora 32:

## **Descarga:**
 * Crear una carpeta en la que guardará el archivo ANTs
 * Abrir una terminal desde la carpeta y descargar el archivo ANTS con el comando: **git clone git://github.com/stnava/ANTs.git**

## **Instalación desde terminal:** 
 * Crear una carpeta "antsbin" comando mkdir y entrar a esa carpeta con cd
 * Correr el comando: **ccmake ../ANTs**
 * Si sale error, instalar las dependencias que ANTs requiere, usando el comando:**sudo dnf install gcc-c++**
 * Volver a correr el comando: **ccmake ../ANTs**
 * Leer lo que está en la carpeta con ls e instalar ANTs usar el comando: **./installANTs.sh**
 * Regresar a la terminal de inicio con *cd* y modificar el bash con el comando: **gedit .bashrc**, agregando al final:  
    **# # ANTs PATH**
    **export ANTSPATH="/home/jpgonzalezh/Apps/install/bin/"**
    **export PATH="${ANTSPATH}:${PATH}"**
 * Guardar y cerrar el archivo bash
 * Para actualizar el bash se corre el comando: **source .bashrc**
 * Hacer una prueba para verificar instalación, usando el comando: **antsRegistrationSyN.sh**
 * Si muestra la documentación, ya está instalado ANTs:D

