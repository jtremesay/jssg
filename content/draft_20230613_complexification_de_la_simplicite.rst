La complexité de la simplicité
##############################

:date: 2023-06-13 21:00
:status: draft

Je sais, le titre est pas super clair. Je vais essayer d'expliquer.

Quand j'ai commencé à m'intéresser au monde du développement web au début des années 2000, c'était simple. Je pouvais faire un truc moche sous `Dreamweaver <https://en.wikipedia.org/wiki/Adobe_Dreamweaver>`_ à d'iframes, l'uploader via FTP chez un hébergeur gratuit de sites persos, et tadam! c'était accesible au monde entier.

C'était facile de créer un nouveau projet. C'était facile de le déployer.

.. code-block:: shell

    $ mkdir mysuperwebsite
    $ cd mysuperwebsite
    $ nvim index.html
    $ ncftpput -R -v -u "jojo" ftp.website.com /mysuperwebsite * 

4 commandes, et mon contenu est crée et en ligne. J'avais 13 ans, et il ne m'en fallait pas plus pour être le maître du monde. (bon, ok, j'étais sous windows. et j'utilisais un Dreamweaver tipiak et filezella. Mais quand même, l'idée est là).

Alors oui, c'était aussi pas très efficace ni très sûr. Nombreuses furent les fois où j'eu oublié de synchroniser un dossier, ou eu supprimé le mauvais fichier par accident. Ficher dont je n'avais naturellement aucune copie ou sauvegarde :) 

Nous voila 20 ans plus tard.

Au cours des années, j'ai continué à m'intéresser à l'ordinateur, à l'informatique, à la programmation et autres trucs associés.

Vers 15 ans, j'ai commencé à apprendre PHP sur le `site du zero <http://web.archive.org/web/20050204031653/http://siteduzero.org/php/>`_.

Là aussi c'était facile de s'y mettre. Il suffisait d'écrire son index.php, de le tester en local avec EasyPHP, et de l'envoyer par ftp.

.. code-block:: shell

    $ mkdir mysuperwebsite
    $ cd mysuperwebsite
    $ nvim index.php
    $ n/cftpput -R -v -u "jojo" ftp.website.com /mysuperwebsite * 

Fast forward. 2010. J'ai 20 ans, j'ai mon DUT Info mention gros branleur en poche, je viens de décrocher mon premier job d'été, un CDD de 2 mois dans une micro agence de Montpellier.

Au menu, notamment du dev web. 

Le code est géré par svn. On utilise notre micro framework PHP maison, jquery, et on envoi sur la prod en ftp avec `BeyondCompare <https://www.scootersoftware.com/>_` (buggé au possible mais je n'ai pas trouvé mieux pour comparer/synchroniser/merger des arborescences/des fichiers). Les migrations de la db sont appliqués en tapant à la main des requêtes SQL sur le serveur de prod.

Aujourd'hui, ce mode de fonctionnement passerait pour hérétique. Mais à l'époque, pour notre petite équipe de 2 à 5 dev, et pour les petites commandes que l'on recevait, ça suffisait amplement.

En 2011, après l'obtention de ma licence pro mention gros branleur, je suis allé retourné bossé dans cette boite 2 ou 3 ans. Durant cette période, on a continuait à fonctionner de la même manière. 

Créer et déployer un nouveau projet était simple.

.. code-block:: shell

    $ svn co svn://blablabla.org/projects/mysuperwebsite mysuperwebsite
    $ cd mysuperwebsite
    $ nvim index.php
    $ svn commit
    $ BeyondCompare

Le coût d'entrée pour un nouveau développeur était très bas. Il lui suffisait juste de connaître un peu PHP et il pouvait être directement productif. (Erf, je commence à parler comme un mec de droite :-/) 

Fast forward. 2014. Je rentre dans une start-up de la micro-électronique. Pas vraiment de web ici. On conçoit une architecture FPGA, et les outils pour la programmer ou la concevoir (les clients pouvant créer eux même le FPGA le plus adapté à leurs besoin avec). 

Le fonctionnement était encore une fois assez simple. Une fois les outils pour developer avec Qt installés, Un dev qui connaissait un peu C++/Qt pouvait directement bosser. On récupère le code, on le modifie et on le commit.

.. code-block:: shell

    $ svn co svn://blablabla.org/projects/superfpga superfpga
    $ cd superfpga
    $ nvim main.cpp
    $ qmake && make && ./bin/superfpga-programmer --script scripts/mes_tests.tcl
    $ svn commit

Sauf que derrière, il ne faut pas juste envoyer 3 fichiers `.php` sur un FTP. Il faut :

- build les composants du système de licence flexera le bien relou
- build une demi-douzaine de libs avec des interdépendances dans tous les sens parce que c'était architecturé avec le postérieur
- build quelques applications c++/qt
- lancer les tests
- génrer les installeurs
- le tout * 4 parce qu'il faut le faire pour RHEL 5 à 7 + Suse
- générer la doc
- générer l'installeur des trucs os indépendant
- générer les installeurs des addons spécifiques à chaque client
- générer les licenses pour le serveur flexera
- collecter ce bordel d'artifacts
- l'organiser dans une arborescence avec un dossier par client puis par OS pour que le client afin que chaque client puisse facilement récupérer son zbeul sans pouvoir accéder au zbeul des autres clients (usage créatif des liens symboliques et de ``make``)
- rsync vers le serveur nfs d'archivage
- rsync vers le serveur ftp si release

Et le tout de manière reproductible, fiable et rapide, et surtout simple parce qu'on veut garder les choses le plus simple possible pour nos juniors.

Comment faire ? Avec de la magie, beaucoup de magie. 

    "3. Any sufficiently advanced technology is indistinguishable from magic."

    -- Clarke's three laws, Arthur C. Clarke

En l'occurrence, cette magie s'appelle Jenkins. Il avait était mis place par mon prédécesseur. Et il avait fait de la magie avec. Beaucoup de magie. J'héritais d'un puisant artefact dont j'ignorais tout.

Les débuts furent rudes. Puis je pris la confiance. Au cours des années, j'ai du passer des centaines d'heures à peaufiner aux petits oignons et vin blanc sec le flow Jenkins parfait pour faire tourner cette CI monstre tout en gardant les choses le plus braindead possible pour mes juniors.

2020, je rentre dans une startup de l'éolien. On a un boîtie à installer sur tes éolienne. On fait plein de mesures et on remonte les données on da claoud/. Là, des algorithmes (mais des vrais, pas de l'IA) on da containers on da claoud font de la magie dans les données pour détecter les problèmes et sous performances de tes éoliennes, les corrections à apporter, et le fric de fou que tu perds à ne pas agir, et aussi le fait que `WTG-07` ne respecte pas son plan de bridage pour limiter les nuisances sonores envers le village à l'Est parce que elle a perdu le nord (littéralement). Le tout présenté par une web app django, toujours on da container on da claoud.

J'vais pas te mentir que cette fois, si ton junior ne connait que vaguement python, ben il va en chier.

D'abord, il faut qu'il prépare son MacBookPro pour le rendre work-compatible. 

.. code-block:: shell

    $ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    $ brew install --cask firefox thunderbird slack vscodium …
    $ brew install postgresql@15 redis python@3.11 awscli …
    $ brew services enable redis postgresql
    $ ssh-keygen …
    $ aws configure …
    $ …
    $ createdb …

(J'ai fait un chouette README.md)

ça y est, il peut récupérer le code et commencer à bosser.

.. code-block:: shell

    $ git clone ssh://github.com/… webfit
    $ cd webfit
    $ git checkout -b feature/1234_bla
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -Ur pip setuptools wheel && pip install -Ur requirements.dev.txt
    $ ./manage.py migrate
    $ ./manage.py createcachetables
    $ ./manage.py loadfixtures
    $ ./manage.py createsuperuser
    $ ./manage.py customize
    $ ./manage.py runtasks &
    $ ./manage.py rundevserver &
    $ nvim bla/blo.py
    $ git commit
    $ git push origin feature/1234_bla

(Le README.md est vraiment chouette)

J'ai pas encore de manière satisfaisante de rendre ça plus simple. Certains me disent que Docker pourraient être une solution. C'est sur que 

.. code-block:: shell

    $ make 

et pouf, des containers gérés par docker compose avec auto reload du code apparaissent est très séduisant. Mais ça rajoute aussi une sacrée couche de magie pour que ça juste marche en toutes circonstances avec mes juniors data-scientists qui à la base sont là pour faire du numpy, pas déboguer des erreurs docker ou GNU Make.

La CI, *Basmala* est plutôt saine. On lance les tests d'un côté et on build l'image docker de l'autre. Et en cas de succès des deux, on push l'image et on redéploy les containeurs.

Le redeploy lui même est un brin créatif vu qu'il faut s'assurer que les migrations de la bases de données soient appliqués avant de lancer les nouveau containeurs sans pour autant casser les anciens containeurs afin d'assurer la continuité de service durant le redeploy.

Dans le monde entier, des armées de magiciens anonymes se sont attelés à la tâches afin que vos migrations soient appliqués sans risquer de tout casser. Payer leur une bière. 

L'infrastructure est géré par terraform. Il commence à y avoir beaucoup de magie dans ce truc afin que les choses soient simples. 

À un moment, on s'est dit que ça serait bien d'avoir un env de preprod en plus de la prod. Pis tant qu'à faire, la preprod tournerait sur AWS ECS Fargate afin de l'évaluer parce que notre stack actuel propulsé par AWS EC2 + notre docker swarm nous demandait trop d'interventions manuelles pour ajouter et supprimer des serveurs à la grappe en fonction de la charge. 

Il m'aura fallu 2 mois à pleurer ma mère et bouffer de la doc terraform et aws pour que la preprod tourne enfin. Ainsi que une semaine pour migrer la prod de EC2 vers ECS. Les ajustements de la CI on étés triviaux.

Maintenant, il ne me faut que 15 minutes pour sortir un nouvel env de staging, entre la modification du terraform, le déployement initial de la db, des redis, du cluster ecs, de l'import manuel du jeu de données initial, création de mon compte utilisateur via la console, création des comptes des juniors depuis l'appli.

Je vais prochainement investir des dizaines d'heures afin que cette opération ne me prenne plus que une minute :

.. code-block:: shell

    $ git clone ssh://github.con/bla/terraform-config
    $ cd terraform-config
    $ terraform init
    $ nvim config.tf
    $ terrform plan
    $ git commit
    $ git push

Et dans un futur plus lointain, je vait encore passer des dizaines d'heures afin que tout cela soit entièrement géré par la CI : on push une nouvelle branche du genre ``stagginq/bla`` et ça crée automagiquement toute l'infra pour `bla.tljieqj.mycompany.com`, ça importe les données initials, crées les comptes dev, envoit une notif slack pour indiquer l'url de cet env et roulez jeunesse.

C'est complexe d'avoir des trucs simples.

Mon bon vieux

.. code-block:: shell

    $ mkdir mysuperwebsite
    $ cd mysuperwebsite
    $ nvim index.html
    $ ncftpput -R -v -u "jojo" ftp.website.com /mysuperwebsite * 

me manque.