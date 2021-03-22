#corta o texto no primeiro balance
#primeira linha seguinte Nome do player
#cada linha que começa com tabulação, é um campo do player, corta no ':' e o seguinte do ':' tira as ',' e trata como int

def file_to_text(file_name):
    f = open(file_name, 'r')
    text = f.read()
    f.close()
    return text

def get_player_from_array(player_array):
    player = {}
    player['name'] = player_array[0]
    if '(Leader)' in player['name']:
        player['name'] = player['name'].replace(' (Leader)', '')
    for i in range(1,6):
        line = player_array[i].split(':')
        player[line[0].replace('\t', '').lower()] = int(line[1].replace(',',''))
    return player


def get_players_from_copy(text):
    players_raw = text.split('\n')[6:]   
    quantidade_players = int(len(players_raw)/6)
    players = []
    for i in range(quantidade_players):
        players.append(get_player_from_array(players_raw[i*6:(i+1)*6]))
    return players

def prey_card_value(tibia_coin_price):
    return tibia_coin_price*10

def real_balance(players, prey_cards, tibia_coin_price):
    for player in players:
        try:
           prey_card = next(prey_card for prey_card in prey_cards if prey_card['name'] == player['name'])
           player['real_balance'] = player['balance'] - int(prey_card['amount'] * prey_card_value(tibia_coin_price))
        except StopIteration:
            player['real_balance'] = player['balance']
    return players

def should_receive(players):
    total_balance = sum(player['real_balance'] for player in players)
    profit_each = total_balance/len(players)
    for player in players:
        player['should_receive'] = int(profit_each - player['real_balance'])
    return players

def separetes_into_debtors_and_creditors(players):
    debtors = []
    creditors = []
    for player in players:
        player['transfer_or_receive'] = player['should_receive']
        if player['should_receive'] <= 0:
            debtors.append(player)
        else:
            creditors.append(player)
    return debtors, creditors

def who_transfers_to_whom(debtors, creditors):
    transfer_to = []
    for debtor in debtors:
        debtor_dict = {
            "name": debtor['name'],
            "transfers_to": []
        }
        for creditor in creditors:
            transfer_value = creditor['transfer_or_receive'] if creditor['transfer_or_receive'] <= abs(debtor['transfer_or_receive']) else -debtor['transfer_or_receive']
            debtor['transfer_or_receive'] += abs(transfer_value)
            creditor['transfer_or_receive'] -= transfer_value
            if transfer_value:
                debtor_dict['transfers_to'].append({
                'to': creditor['name'],
                'amount': abs(transfer_value)})
            if not creditor['transfer_or_receive']:
                continue
        transfer_to.append(debtor_dict)
    return transfer_to

def whole_text(transfer_to):
    string = ''
    for debtor in transfer_to:
        string += f'*{debtor["name"]}* transfer to:\\n'
        for line in debtor['transfers_to']:
            string += f'transfer {line["amount"]} to {line["to"]}\\n'
        string += '\\n'
    return string


def text_to_should_receive(text, prey_cards, tibia_coin_price):
    players = get_players_from_copy(text)
    players = real_balance(players, prey_cards, tibia_coin_price)
    players = should_receive(players)
    transfer_to = who_transfers_to_whom(*separetes_into_debtors_and_creditors(players))
    text_to_clipboard = whole_text(transfer_to)
    return players, transfer_to, text_to_clipboard


