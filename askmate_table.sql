--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS pk_users_id CASCADE;


DROP TABLE IF EXISTS public.question;
DROP SEQUENCE IF EXISTS public.question_id_seq;
CREATE TABLE question (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    user_id integer
);

DROP TABLE IF EXISTS public.answer;
DROP SEQUENCE IF EXISTS public.answer_id_seq;
CREATE TABLE answer (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text,
    user_id integer
);

DROP TABLE IF EXISTS public.comment;
DROP SEQUENCE IF EXISTS public.comment_id_seq;
CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer,
    user_id integer
);


DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

DROP TABLE IF EXISTS public.tag;
DROP SEQUENCE IF EXISTS public.tag_id_seq;
CREATE TABLE tag (
    id serial NOT NULL,
    name text
);

DROP TABLE IF EXISTS public.users;
DROP SEQUENCE IF EXISTS public.users_id_seq;
CREATE TABLE users (
    id serial NOT NULL,
    username character varying(255) UNIQUE,
    password character varying(255),
    email character varying(255) UNIQUE,
    registration_time timestamp without time zone,
    role character varying(255) DEFAULT 'user',
    recovery_key character varying(255) DEFAULT '0'
);


ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY users
    ADD CONSTRAINT pk_users_id PRIMARY KEY (id);


ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id)
    ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id)
    ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id)
    ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id)
    ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id)
    ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id)
    ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id)
    ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY question
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id)
    ON UPDATE CASCADE ON DELETE CASCADE;


INSERT INTO users VALUES (1, 'username', 'password', 'test@testing.co.uk', '2017-06-07 14:01:00');
INSERT INTO users VALUES (2, 'aladar_istvan', 'shorthand', 'aladar@testing.co.uk', '2017-01-07 11:30:00');
INSERT INTO users VALUES (3, 'egyip_Tomi', 'jukasssss', 'nemlyukas@jukasing.co.uk', '2017-06-02 23:59:00');
INSERT INTO users VALUES (4, 'Ormai_Petya', 'dzsasztinbibor', 'peter@jukasing.uk', '2011-01-02 21:29:00');
INSERT INTO users VALUES (5, 'Barney', 'kualalumpur', 'egyiptom@pakisztan.co.uk', '2017-03-23 11:59:00');
INSERT INTO users VALUES (6, 'helike', 'kaliczka', 'helgaszeret@se.nem', '2018-06-02 15:15:00');
INSERT INTO users VALUES (7, 'pudingzsarnok', 'citromsav', 'kalapos@jukasing.co.uk', '2017-06-02 23:59:00');
INSERT INTO users VALUES (8, 'kalapos', 'szeretemjucit', 'julius@cezar.com', '2017-06-08 08:43:00');
INSERT INTO users VALUES (9, 'jancsika', 'nemertem', 'nemertem@jukasing.co.uk', '2017-04-11 19:01:00');
INSERT INTO users VALUES (10, 'azisten', 'envagyokcsaken', 'iamthegod@jukasing.co.uk', '2017-02-26 23:59:00');
SELECT pg_catalog.setval('users_id_seq', 10, true);


INSERT INTO question VALUES (0, '2017-04-28 08:29:00', 29, 7, 'How to make lists in Python?', 'I am totally new to this, any hints?', NULL, 1);
INSERT INTO question VALUES (1, '2017-04-29 09:19:00', 15, 9, 'Wordpress loading multiple jQuery Versions', 'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)', 'images/image1.png', 2);
INSERT INTO question VALUES (2, '2017-05-01 10:41:00', 1364, 57, 'Drawing canvas with an image picked with Cordova Camera Plugin', 'I''m getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I''m on IOS, it throws errors such as cross origin issue, or that I''m trying to use an unknown format.', NULL, 3);
INSERT INTO question VALUES (3, '2017-05-18 10:29:00', 0, 0, 'Mi kellene egy görög teknőshöz?', 'Van egy ismerősöm. Nekem akarja adni a 10 éves görög teknősét. Milyen dolgokat kellene venni neki? Egyébként akkor mint egy zsömle.', NULL, 9);
INSERT INTO question VALUES (4, '2017-05-18 10:29:00', 0, 0, 'Bőrkeményedés nő állandóan a lábamon. Mit tegyek?', 'Akár egy pár óra tevékenység, 1-2 km gyaloglás után is bőrkeményedés lesz a talpam, mit lehetne tenni hogy ne legyen ennyire?', NULL, 5);
INSERT INTO question VALUES (5, '2017-05-18 10:29:00', 0, 0, 'Starbucksba hány éves kortól lehet kávét vagy bármi ilyet venni?', 'csak mert nem tudom és örülnék ha holnapig lenne válasz', NULL, 4);
INSERT INTO question VALUES (6, '2017-05-18 10:29:00', 0, 0, 'Mikor kezdtetek tápszert adni? Szoptatni szeretném a babám, de mi az a pont, amikor muszáj tápszerezni?', '4 kg-val született,visszaesett a korházba 3,85-re,de 3.95-tel jöttünk haza. Hnapután lesz 3 hetes,és alig 4.15 kg. Solszor alig eszik 50-60-akat,pedig ilyenkor szerintem talán már többet "illene",igy félek, h nem is termelödik viszont nyugodt, türelmes baba, végig alussza az éjszakát, ami megint ritka ennyi idősen.nagylányomat 1.5 éves koráig szoptattam 6 éve. Bizonytalan vagyok.Ki mit tenne a helyemben?', NULL, 10);
INSERT INTO question VALUES (7, '2017-05-18 10:29:00', 0, 0, 'Van egy srác aki még négy napja azt mondta, hogy nem tud nélkülem élni. Erre most összejön egy csajjal. Szerintetek ezt most miért csinálta?', 'Tanácstalan vagyok', NULL, 7);
INSERT INTO question VALUES (8, '2017-05-18 10:29:00', 0, 0, '13 évesen csók?', '13 éves lány vagyok. Nagyon hosszú történet,de a lényege,hogy megismeetem egy fiút.Már egy hónapja beszélek vele,találkoztunk is és most is fogunk.Az első csók még nem túl korai?', NULL, 6);
INSERT INTO question VALUES (9, '2017-05-18 10:29:00', 0, 0, 'Lányok! Titeket zavarna, ha a barátotok saját magáról meztelen képeket oszt meg az interneten?', 'Eléggé exhibicionista vagyok, és szeretek magamról pucér képeket felrakni, de a barátnőm ennek nem nagyon örül.', NULL, 8);
INSERT INTO question VALUES (10, '2017-05-18 10:29:00', 0, 0, 'Hogyan lehetne késleltetni a menstruációm?', 'Tudom, hogy hülyeségnek hangzik. De mégis felteszem a kérdést, hátha tud segíteni valamit. Sajnos idén is úgy sikerült a nyaralást tervezni, hogy épp meg lesz a menzeszem. Szedek fogamzásgátlót, és ez miatt kérdezném, hogy lehetne valahogy egy pár napot elhalasztani?', NULL, 5);
INSERT INTO question VALUES (11, '2017-05-18 10:29:00', 0, 0, 'Van olyan progi, amivel tudok videót vágni?', 'Ha van, nevet is kérek!', NULL, 2);
SELECT pg_catalog.setval('question_id_seq', 11, true);

INSERT INTO answer VALUES (1, '2017-04-28 16:49:00', 4, 1, 'You need to use brackets: my_list = []', NULL, 1);
INSERT INTO answer VALUES (2, '2017-04-25 14:42:00', 35, 1, 'Look it up in the Python docs', 'images/image2.jpg', 2);
INSERT INTO answer VALUES (3, '2017-04-28 16:49:00', 0, 3, 'Egy akvárium, egy teknős, kis víz és kis homok', NULL, 9);
INSERT INTO answer VALUES (4, '2017-04-28 16:49:00', 0, 4, 'A lábhoz rosszul illeszkedő cipő is gyakran okoz bőrkeményedést.', NULL, 4);
INSERT INTO answer VALUES (5, '2017-04-28 16:49:00', 0, 4, 'Vágd le a talpad', NULL, 1);
INSERT INTO answer VALUES (6, '2017-04-28 16:49:00', 0, 4, 'Normális cipőt/betétet kell venni legközelebb.', NULL, 10);
INSERT INTO answer VALUES (7, '2017-04-28 16:49:00', 0, 5, 'Nem korhatáros, csak nem ajánlott fejlődő szervezetnek a koffein. De ha 14-15 alatt vagy, akkor kérj valami koffeinmenteset inkább. Nem most kéne kisérletezni vele, lehet nagyon megdobogtatná a szíved és rosszul lennél.', NULL, 1);
INSERT INTO answer VALUES (8, '2017-04-28 16:49:00', 0, 6, 'kb 2 hét alatt hízott tehát 200 grammot (gondolom 3-4 napos volt mikor kijöttetek és még van 2 nap a betöltött 3. hétig így számoltam a 2 hetet)? az még szerintem a normális kategória. főleg hogy nagysúlyú baba, biztosan nem fog havi 1,5 kilókat hízni, mint pl az enyém aki 2700 grammal született. ha jól alszik akkor biztos hogy nem aggódnék ezen. a lányom egyébként félévesen is 50-60 miliket evett, napi 7-8 alkalommal étkezett, és teljesen normálisan hízott vele. ő is nagy súlyú baba volt', NULL, 2);
INSERT INTO answer VALUES (9, '2017-04-28 16:49:00', 0, 6, 'Hányszor szopik egy nap?', NULL, 1);
INSERT INTO answer VALUES (10, '2017-04-28 16:49:00', 0, 7, 'Továbblépett.', NULL, 8);
INSERT INTO answer VALUES (11, '2017-04-28 16:49:00', 0, 7, 'pfff nem tom talán féltékennyé akar tenni', NULL, 5);
INSERT INTO answer VALUES (12, '2017-04-28 16:49:00', 0, 7, 'Meghalt', NULL, 10);
INSERT INTO answer VALUES (13, '2017-04-28 16:49:00', 0, 7, 'Szerintem egyszer megnyílt egy féreglyuk előtted amit nem vettél észre. Ezen keresztül átkerültél egy párhuzamos univerzumba, ahol minden ugyanaz, csak a fiú nem érez irántad semmit.', NULL, 7);
INSERT INTO answer VALUES (14, '2017-04-28 16:49:00', 0, 7, 'HAZUDOTT MIKOR EZT MONDTA NEKED!FELEJTSD EL AZ ILYET', NULL, 9);
INSERT INTO answer VALUES (15, '2017-04-28 16:49:00', 0, 8, 'Edes jo istenem. Meg a tejfogaid sem nottek ki mind', NULL, 5);
INSERT INTO answer VALUES (16, '2017-04-28 16:49:00', 0, 8, 'Terhes leszel, védekezz!!!', NULL, 3);
INSERT INTO answer VALUES (17, '2017-04-28 16:49:00', 0, 9, 'Nem járnék veled, az biztos', NULL, 1);
INSERT INTO answer VALUES (18, '2017-04-28 16:49:00', 0, 10, 'citromlé, bár lehet ez csak mende monda', NULL, 2);
INSERT INTO answer VALUES (19, '2017-04-28 16:49:00', 0, 10, 'Nekem a citromlé nem hatott a menstruációmra. Minden reggel szoktam inni.', NULL, 4);
INSERT INTO answer VALUES (20, '2017-04-28 16:49:00', 0, 11, 'Van! És Béla vagyok.', NULL, 4);
SELECT pg_catalog.setval('answer_id_seq', 20, true);

INSERT INTO comment VALUES (1, 0, NULL, 'Please clarify the question as it is too vague!', '2017-05-01 05:49:00', 1, 1);
INSERT INTO comment VALUES (2, NULL, 1, 'I think you could use my_list = list() as well.', '2017-05-02 16:55:00', 1, 1);
SELECT pg_catalog.setval('comment_id_seq', 2, true);

INSERT INTO tag VALUES (1, 'python');
INSERT INTO tag VALUES (2, 'sql');
INSERT INTO tag VALUES (3, 'css');
SELECT pg_catalog.setval('tag_id_seq', 3, true);

INSERT INTO question_tag VALUES (0, 1);
INSERT INTO question_tag VALUES (1, 3);
INSERT INTO question_tag VALUES (2, 3);
