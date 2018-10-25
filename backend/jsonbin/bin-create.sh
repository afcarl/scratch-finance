curl --header "Content-Type: application/json" \
  --header "secret-key: $JSONBIN_KEY" \
  --request POST \
  --data '{"sample": "Hello World"}' \
  https://api.jsonbin.io/b
