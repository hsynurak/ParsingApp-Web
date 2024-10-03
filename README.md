# ParsingApp-Web
* Localinizde projemin çalışması için öncelikle bilgisayarınızda bazı işlemler yapmanız gerekmektedir. 
* Öncelikle Docker Desktop'un bilgisayarınızda kurulu olduğundan emin olun. 
  * Eğer kurulu değilse "https://www.docker.com/products/docker-desktop/" adresi üzerinden gerekli adımlar ile kurulumu tamamlayın. 
  * Windows veya MacOS cihazlarda Docker-Compose Docker Desktop ile beraber geldiği için işlem yapmanıza gerek yoktur. Ancak Linux cihazlarda `sudo apt update` ve `sudo apt install docker.io` komutlarını terminale girerek Docker kurulumunu gerçekleştirip, sonrasında `sudo apt install docker-compose` komudu ile beraber Docker-Compose kurulumunu tamamlıyoruz. 
* Docker kurulumu tamamlandıktan sonra ihtiyacımız olan "docker-compose.yml" dosyasını `wget https://raw.githubusercontent.com/hsynurak/ParsingApp-Web/refs/heads/main/docker-compose.yml` komudu ile beraber çalışma dizinimize indiriyoruz. 
  * İndirme işlemi tamamlandıktan sonra terminal üzerinden `ls` komudu ile beraber kontrol sağlayabilirsiniz.
* Docker-Compose dosyasını indirildikten sonra son adım olarak `docker-compose up` komudu ile beraber ayağa kaldırma işlemini gerçekleştiririz. 
* Ayağa kaldırma işleminin sonucunda tarayıcımızdan "localhost:8000" portu ile projemize ulaşabiliriz. 
