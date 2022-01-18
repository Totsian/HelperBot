<h1> <b>Helper Bot</b> </h1>
Ссылка на бота https://t.me/MateForHelpBot (@MateForHelpBot)<BR>
(Т.к. бот залит на Heroku, который не дружит с SQLite, то по ссылке можно проверить его работоспособность, однако нет возможности просмотерть базу данных.
Так же, после каждого перезапуска сервера, изменения в БД не сохраняются. Для дальнейшего использования бота на Heroku, лучше поделючить PostgreSQL.)<BR><BR>

Данный бот предназначен для записей идей, фильмов, книг, ссылок, контактов, списка дел не выходя из Телеграма. При запуске <b>/start</b> пользователь автоматически записывается в базу данных.<BR>
Для того, чтобы выбрать, что записать, есть <b>меню</b>, в котором все описано, либо можно написать <b>/help</b>, где будут описаны команды:<BR>
<ul>
  <li><b>/help</b> - помощь (список команд)</li>
  <li><b>/idea</b> - действия над идеями</li>
  <li><b>/to_do</b> - действия над списком дел</li>
  <li><b>/contact</b> - действия над контактами</li>
  <li><b>/film</b> - действия над фильмами</li>
  <li><b>/book</b> - действия над книгами</li>
  <li><b>/link</b> - действия над ссылками</li>
 </ul>

После выбора команды, приходит сообщение с четырьмя кнопками. В самом сообщении описывается, что делает каждая кнопка. Для добавления новой записи используется кнопка - <b>"Записать"</b>. Для просмотра всех записей - <b>"Просмотреть"</b>. Если есть необходимость в удалении какой-либо записи или нескольких записей - <b>"Удалить"</b>. Если нажата кнопка "Записать" или "Удалить", но ничего записывать не будет, необходимо нажать кнопку <b>"Завершить"</b>.

<b>По проекту:</b><BR>
Для написания телеграмм бота использовалась библиотека aiogram.<BR>
В файле config.py - API TOKEN, который генерируется BotFather при создании нового бота.<BR>
В файле main.py находится основной код программы.<BR>
Все функции, начинающиейся на <b>set_</b>, предназначены для отображения списка записей.<BR>
Все функции, начинающиейся на <b>get_</b>, предназначены для записи текста сообщений в базу данных.<BR>
Все функции, начинающиейся на <b>delete_</b>, предназначены для удаления записей из базы данных.<BR>
В текстовых файлах хранится текст, который легко изменить и при этом не искать его в коде. Для чтения текста в <b>main.py</b> есть функция <b>read_txt()</b>, на вход которой приходит название файла, а на выходе возвращается его текст.
