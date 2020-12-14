# donawd-twump-twitter-bot

## Requirements

- sudo apt-get install python3
- sudo apt-get install -y python3-pip
- [indicoio](https://indico.io/blog/getting-started-indico-tutorial-for-beginning-programmers/)
  -- python3 -m pip install indicoio==1.4.1
- python3 -m pip install tweepy
- pip install simplejson
- ImportError: libf77blas.so.3
  -- sudo apt-get install python3-pip python3-dev
  -- wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v1.8.0/tensorflow-1.8.0-cp35-none-linux_armv7l.whl
  -- sudo pip3 install /tensorflow-1.8.0-cp35-none-linux_armv7l.whl
  -- sudo apt-get install libatlas-base-dev
- ImportError: libopenjp2.so.7
  -- sudo apt-get install libopenjp2-7
- ImportError: libtiff.so.5: cannot open shared object file: No such file or directory
  -- sudo apt install libtiff5

## TODO

- Attach Images/Videos in tweets (?)
- Truncated tweets should be displayed in multiple parts (1/2), (2/2), etc.
- Sentiment analysis on tweet to add specific emoticon
