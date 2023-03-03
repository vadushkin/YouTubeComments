# Script for getting comments on YouTube videos

Installation
------------

#### Clone a repository

```
git clone https://github.com/vadushkin/YouTubeComments.git
```

#### Change a folder

```
cd YouTubeComments
```

#### Venv

Windows:

```shell
python -m venv venv
.\venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Linux:

```shell
python3 -m venv venv
source venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

#### Poetry

```
poetry install
poetry shell
```

Examples
---------

A small example comment

```shell
python main.py
```

```example/not_translated_comments.json```

```json
{
  "Rick Astley": "1 BILLION views for Never Gonna Give You Up!  Amazing, crazy, wonderful! Rick ️",
  "Juli is Online": "Jokes on you I love this song\n\nNow where's my free iPhone",
  "haz3rz": "мне просто трек нравится",
  "그대만이": "옛 추억의 노래",
  "человек": "Легенда\n",
  "Сварливерчик": "Рикрольте меня, я хочу слушать это всегда",
  "Jessica veiga": "Clássico atemporal",
  "fox mccloud93": "The 172,000 people who disliked this video are only mad because they've been rick rolled.",
  "프테": "이 노래도 추억이 됐네..",
  "스테이씨비타민씨": "아..일본 시티팝같은 느낌인데, 뭔가 몽글몽글해지는 감성..좋다!",
  "Laura Vargas": "Soy milenial pero amo estas canciones esto si es buena música <3",
  "Alexia🇲🇳": "Mi 1% de batería que me queda me lo voy a gastar escuchando este temazo",
  "Cinematic Captures": "Wait this isn’t How To Rickroll People Tutorial.",
  "DANK MEMES": "Fun fact: The second  person who got rickrolled was Rick's editor.\n\nSo many likes\n ",
  "Its Thlippery": "I used to get mad about getting rickrolled but now I'm liking it.",
  "Diablo [GMD]": "Начало это лучшее что со мной было...",
  "...": "..."
}
```

Translate dictionary

```python
translate_dictionary(dictionary, is_rename_names=True, to_language="en")
```

```examples/translated_comments.json```

```json
{
  "Rick Astley": "1 BILLION views for Never Gonna Give You Up!  Amazing, crazy, wonderful! Rick ️",
  "July is Online": "Jokes on you I love this song\n\nNow where's my free iPhone",
  "haz3rz": "I just love the track",
  "only you": "old memories song",
  "Human": "A legend",
  "Svarliverchik": "Rickroll me, I want to listen to this always",
  "Jessica Veiga": "timeless classic",
  "fox mccloud93": "The 172,000 people who disliked this video are only mad because they've been rick rolled.",
  "pte": "This song also became a memory..",
  "Stay C Vitamin C": "Ah.. It feels like Japanese city pop, but the sensibility is kind of fuzzy.. I like it!",
  "Laura Vargas": "I'm a millennial but I love these songs this is good music <3",
  "Alexia🇲🇳": "My 1% of battery that I have left I'm going to spend it listening to this great song",
  "Cinematic Captures": "Wait this isn’t How To Rickroll People Tutorial.",
  "THANKS MEMES": "Fun fact: The second  person who got rickrolled was Rick's editor.\n\nSo many likes",
  "Its Thlippery": "I used to get mad about getting rickrolled but now I'm liking it.",
  "Diablo [GMD]": "The beginning is the best thing that happened to me...",
  "...": "..."
}
```

Get a list of comments

```shell
['1 BILLION views for Never Gonna Give You Up!\xa0 Amazing, crazy, wonderful! Rick ️',
 "Jokes on you I love this song\n\nNow where's my free iPhone", 'мне просто трек нравится', '옛 추억의 노래', 'Легенда\n',
 'Рикрольте меня, я хочу слушать это всегда', 'Clássico atemporal',
 "The 172,000 people who disliked this video are only mad because they've been rick rolled.", '이 노래도 추억이 됐네..',
 '아..일본 시티팝같은 느낌인데, 뭔가 몽글몽글해지는 감성..좋다!', 'Soy milenial pero amo estas canciones esto si es buena música <3',
 'Mi 1% de batería que me queda me lo voy a gastar escuchando este temazo',
 'Wait this isn’t How To Rickroll People Tutorial.',
 "Fun fact: The second  person who got rickrolled was Rick's editor.\n\nSo many likes\n ",
 "I used to get mad about getting rickrolled but now I'm liking it.", 'Начало это лучшее что со мной было...',
 ...]
```

Translate list

```python
translate_list(list_of_comments, to_language="en")
```

```shell
['1 BILLION views for Never Gonna Give You Up!\xa0 Amazing, crazy, wonderful! Rick ️',
 "Jokes on you I love this song\n\nNow where's my free iPhone", 'I just love the track', 'old memories song',
 'A legend', 'Rickroll me, I want to listen to this always', 'timeless classic',
 "The 172,000 people who disliked this video are only mad because they've been rick rolled.",
 'This song also became a memory..',
 'Ah.. It feels like Japanese city pop, but the sensibility is kind of fuzzy.. I like it!',
 "I'm a millennial but I love these songs this is good music <3",
 "My 1% of battery that I have left I'm going to spend it listening to this great song",
 'Wait this isn’t How To Rickroll People Tutorial.',
 "Fun fact: The second  person who got rickrolled was Rick's editor.\n\nSo many likes",
 "I used to get mad about getting rickrolled but now I'm liking it.",
 'The beginning is the best thing that happened to me...',
 ...]

```

Speed
-----

Selenium - no fastest, so for just get comments and run to watch favorite movie - yes.

For a plenty of videos - no.

For a large number of videos using [GoogleAPI](https://developers.google.com/youtube/v3)
