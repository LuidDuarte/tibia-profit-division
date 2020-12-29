from flask import (
    render_template,
    redirect,
    url_for,
    session,
    abort,
    flash,
    request,
    current_app,
    make_response)
from app.utils import text_to_should_receive
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    text = request.form['party_hunt'].replace('\r\n', '\n').replace('\r', '\n')
    prey_cards_raw = request.form['prey_cards'].split(';')[:-1]
    prey_cards = []
    for prey_card_raw in prey_cards_raw:
        prey_card = {}
        prey_card['name'] = prey_card_raw.split(',')[0]
        prey_card['amount'] = int(prey_card_raw.split(',')[1])
        prey_cards.append(prey_card)
    tibia_coin_price = int(request.form['tibia_coin_value'])
    return render_template('results.html', players=text_to_should_receive(text, prey_cards, tibia_coin_price))