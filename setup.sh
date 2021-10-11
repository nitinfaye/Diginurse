mkdir -p ~/.rasa/train
echo "\
[general]\n\
email = \"myemail@gmail.com\"\n\
" > ~/.rasa/credentials.yml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.rasa/config.yml
