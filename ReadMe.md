1.Запустить serv.py

2.Скопировать адрес локального хоста и запустить в браузере

3.Выбрать тип картинки

Как все работает?

Каждый переход на ссылку лисичек, кошек, собак обрабатывается одинаково, сначала парсится html, 
берется из кода элемента картинки url самой картинки, сохраняется, после этого обрабатывается 
с помощью pillow фильтром L (черно-белый) и возвращается пользователю готовый результат, одновременно
создается новая строка в базе данных, с помощью которой мы выводим истоию запросов, по ссылке /history
в новой html странице. У бд помимо полей что в условии я добавил еще одно поле url_adr, в которое записывается
url ссылка только что обработанной картинки, это нужно для того чтобы можно было смотреть уже просмотренные 
картинки по этой ссылке