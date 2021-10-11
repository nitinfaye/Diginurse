mkdir -p ~/.rasa/train
echo "\
[general]\n\
email = \"nitin.faye@gmail.com\"\n\
" > ~/.rasa/actions
" > ~/.rasa/credentials.yml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.rasa/config.yml
