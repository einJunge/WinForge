🏛️ WinForge Secure Builder
Entorno de compilación de ejecutables de Windows controlado

📌 Descripción general

WinForge Secure Builder es un entorno controlado y reproducible diseñado para compilar ejecutables de Windows ( .exe) desde sistemas Linux , utilizando una cadena de herramientas compatible con Windows basada en Wine y Python .

<img width="590" height="288" alt="image" src="https://github.com/user-attachments/assets/c08e3c72-431b-4a5e-b95a-fb7d5d7e098e" />

El proyecto elimina la necesidad de instalar herramientas de desarrollo directamente en máquinas Windows, lo que permite flujos de trabajo de generación de ejecutables seguros, aislados y escalables desde entornos basados ​​en Linux.

Esta herramienta es adecuada para:
Herramientas de seguridad defensiva
Entornos académicos y de laboratorio
Desarrollo de utilidades internas
Generación binaria controlada de Windows

🎯 Características principales
✔ Compilar scripts de Python ( .py) en ejecutables de Windows ( .exe)
✔ Entorno Windows completamente aislado usando Wine
✔ Configuración automatizada del entorno y gestión de dependencias
✔ No se requieren Python ni herramientas de compilación en los sistemas Windows de destino
✔ Proceso de construcción reproducible y portátil
✔ Diseñado para uso profesional e institucional

🧱 Arquitectura
  Linux Host (Kali / Debian / Ubuntu)
 └── Wine (64-bit, isolated prefix)
      └── Python 3.10.11 (Windows)
           ├── PyInstaller
           ├── requests
           ├── psutil
           └── pillow
Todos los procesos de compilación se ejecutan dentro del entorno Windows emulado , lo que garantiza la compatibilidad nativa con los sistemas Windows.

📦 Requisitos del sistema (Linux)

Las siguientes dependencias son necesarias y se instalan automáticamente:
    wine64
    wine32
    wget
    winbind
    cabextract
    unzip
⚠️ El Python nativo de Linux no se utiliza para la compilación.

⚙️ Configuración del entorno

WinForge incluye un script de arranque automatizado que prepara el entorno completo.
winforge_env_setup.sh

▶️ Ejecutar (configuración única)
chmod +x winforge_env_setup.sh
sudo ./winforge_env_setup.sh

🔧 Qué hace el script
    Instala dependencias de Linux
    Crea un prefijo Wine aislado
    Descargas Python 3.10.11 (Windows x64)
    Instala Python enC:\Python310
    Agrega Python a PATH
    Instala las bibliotecas de Python necesarias
    Valida la cadena de herramientas completa
    Genera un registro de configuración

1️⃣ Cargar código fuente

Despues de la instalacion ejecuta la herramienta

python3 winforge.py
<img width="986" height="697" alt="image" src="https://github.com/user-attachments/assets/39885f92-24a9-4878-b8f2-14a93d9212b9" />


Seleccione un archivo fuente de Python:
tool.py (codigo de la herramienta que se convertira en .exe) 
#toma en cuenta que la herramienta debe ser pensada para windows
    ejemplo en chatgpt (crear una herramienta de escaneo para windows en codigo python)
Toman en cuenta que debes de configurar el directorio a guardar el .exe solo si te genera un error

🧾 Autor

Marcos Hernandez
Alias: Einjunge
Analyst Soc, Ethical Hacker
