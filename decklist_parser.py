
def parse_decklist(deck_txt):
  deck_txt = deck_txt.lower()
  deck = []
  # TODO: --------------MARKET---------------
  for line in deck_txt.splitlines():
    line = line.split(' (')[0]
    if ' ' not in line: continue
    count, card_name = line.split(' ', 1)
    deck += int(count) * [card_name]
  return deck