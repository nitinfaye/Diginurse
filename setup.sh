mkdir -p ~/.rasa/
echo "\
[general]\n\
email = \"myemail@gmail.com\"\n\
" > ~/.rasa/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.rasa/config.toml
