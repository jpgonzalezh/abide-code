# Instalación de Freesurfer 

Pasos a seguir para realizar la instalación de Freesurfer en PC con sistema operativo Fedora 32:

## **Descarga:**
 * Dirigirse a la página https://surfer.nmr.mgh.harvard.edu/fswiki/DownloadAndInstall e ir a la última versión no.7 
 * Descargar el archivo de freesurfer *freesurfer-linux-centos7_x86_64-7.1.0.tar.gz*

## **Instalación desde terminal:** 
 * Abrir una terminal desde la carpeta de Downloads
 * Descomprimir el archivo de freesurfer con el comando: **sudo tar -xzvf freesurfer-linux-centos7_x86_64-7.1.0.tar.gz -C /usr/local**
 * Regresar a la terminal de inicio con *cd* y modificar el bash con el comando: **gedit .bashrc**, agregando al final:  
    **# Freesurfer path**  
    **export FREESURFER_HOME=/usr/local/freesurfer**  
    **source $FREESURFER_HOME/SetUpFreeSurfer.sh**  
 * Guardar y cerrar el archivo bash
 * Para actualizar el bash se corre el comando: **source .bashrc**

## **Instalación de licencia Freesurfer:**
 * Abrir la terminal en una carpeta donde tenga un archivo .nii
 * Hacer una prueba con el comando: **mri_convert x.nii x.nii.gz**
 * Aparece un mensaje para registrarse en freesurfer a través del link: http://surfer.nmr.mgh.harvard.edu/registration.html
 * Al registrarse, abrir el archivo *license.txt*
 * Regresar a la terminal y correr el comando: **sudo gedit /usr/local/freesurfer/.license**
 * Agregar a la ventana los datos del archivo *license.txt*. Guardar y cerrar.
 * Volver a correr el comando: **mri_convert x.nii x.nii.gz**
 * Si funciona, ya puedes abrir el comando **freeview x.nii.gz**
 * Correr el comando: **sudo dnf install mesa-libGLU**
 * Abrir freesurfer con el comando: **freeview** :D
