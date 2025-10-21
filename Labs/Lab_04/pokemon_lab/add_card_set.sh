#!/bin/bash

read -p "TCG Card Set ID: " SET_ID
if [ -z "$SET_ID" ]; then
    echo "Error: Set ID cannot be empty." >&2
    exit 1
fi
echo "Fetching the data for set ID: $SET_ID"
mkdir -p card_set_lookup
curl -s "https://api.pokemontcg.io/v2/cards?q=set.id:$SET_ID" -o "card_set_lookup/$SET_ID.json"