# ParsingApp-Web
[TR]
* Localinizde projemin çalışması için öncelikle bilgisayarınızda bazı işlemler yapmanız gerekmektedir. 
* Öncelikle Docker Desktop'un bilgisayarınızda kurulu olduğundan emin olun. 
  * Eğer kurulu değilse "https://www.docker.com/products/docker-desktop/" adresi üzerinden gerekli adımlar ile kurulumu tamamlayın. 
  * Windows veya MacOS cihazlarda Docker-Compose Docker Desktop ile beraber geldiği için işlem yapmanıza gerek yoktur. Ancak Linux cihazlarda `sudo apt update` ve `sudo apt install docker.io` komutlarını terminale girerek Docker kurulumunu gerçekleştirip, sonrasında `sudo apt install docker-compose` komudu ile beraber Docker-Compose kurulumunu tamamlıyoruz. 
* Docker kurulumu tamamlandıktan sonra ihtiyacımız olan "docker-compose.yml" dosyasını `wget https://raw.githubusercontent.com/hsynurak/ParsingApp-Web/refs/heads/main/docker-compose.yml` komudu ile beraber çalışma dizinimize indiriyoruz. 
  * İndirme işlemi tamamlandıktan sonra terminal üzerinden `ls` komudu ile beraber kontrol sağlayabilirsiniz.
* Docker-Compose dosyasını indirildikten sonra son adım olarak `docker-compose up` komudu ile beraber ayağa kaldırma işlemini gerçekleştiririz. 
* Ayağa kaldırma işleminin sonucunda tarayıcımızdan "localhost:8000" portu ile projemize ulaşabiliriz. 

[EN]
* In order to run my project locally, you need to do some steps on your computer.
* First, check that Docker Desktop is installed on your computer. If it is not installed, you can install it by following the steps from the link: https://www.docker.com/products/docker-desktop.
  * On Windows or macOS devices, Docker-Compose comes with Docker Desktop, so you don't need to do any things.
  * But on Linux devices, you can install Docker by entering the following commands in the terminal: `sudo apt update` and `sudo apt install docker.io`, and then complete the Docker-Compose installation with the  `sudo apt install docker-compose` command.
* If Docker is installed, download the required docker-compose.yml file to your working directory by running the command `wget https://raw.githubusercontent.com/hsynurak/ParsingApp-Web/refs/heads/main/docker-compose.yml`.
  * After the download is complete, you can check it by running the `ls` command in the terminal.
* Once the Docker-Compose file is downloaded, as the final step, run `docker-compose up` command to start the application.
* After the application is successfully started, you can see the project via the browser at "localhost:8000".
