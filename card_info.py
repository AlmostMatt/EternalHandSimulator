import re

'''
TODO: documentation
TODO: card-draw logic (seek power and favors) - what about hojan, bayonet, etc?

TODO: see if I can import card data from eternalwarcry, eternalcards or something similar
TODO: iterate all power cards to verify they all have expected influence
'''

factions_for_word = {
  'fire': 'F',
  'time': 'T',
  'justice': 'J',
  'primal': 'P',
  'shadow': 'S',
  'granite': 'F',
  'amber': 'T',
  'emerald': 'J',
  'cobalt': 'P',
  'amethyst': 'S',
  'shugo': 'F',
  'temple': 'T',
  'crownwatch': 'J',
  'clan': 'P',
  'cabal': 'S',
  'impulse': 'FT',
  'glory': 'FJ',
  'fury': 'FP',
  'chaos': 'FS',
  'progress': 'TJ',
  'wisdom': 'TP',
  'mystery': 'TS',
  'order': 'JP',
  'vengeance': 'JS',
  'cunning': 'PS',
  'praxis': 'FT',
  'rakano': 'FJ',
  'skycrag': 'FP',
  'stonescar': 'FS',
  'combrei': 'TJ',
  'elysian': 'TP',
  'xenan': 'TS',
  'hooru': 'JP',
  'argenport': 'JS',
  'feln': 'PS',
  # special cases: tokens, diplo, common cause
  'instinct': 'FTP',
  'honor': 'FJP',
  'ambition': 'FJS',
  'vision': 'TJS',
  'knowledge': 'TPS',
  'diplomatic': 'FTJPS',
  'common': 'FTJPS',
}

def is_power(card):
  # note: I consider standards and monuments to be power
  return re.search('seat | standard| banner| sigil|waystone|crest |diplomatic seal|common cause|sealed writ|chairman\'s contract', card) != None

def is_pledge(card):
  # TODO: have a separate file with pledge card data
  return re.search('severin, the mad mage', card) != None

# Returns a string of the produceable influence colors and a boolean
# indicating whether or not it is a 'choose-one' card like Diplomatic Seal
def get_influence_produced(card):
  # TODO: handle the is_pledge(card) case
  if not is_power(card):
    return '', False
  for word in card.split():
    if word in factions_for_word:
      factions = factions_for_word[word]
      choose_one_card = (card in ('common cause', 'diplomatic seal')) or ('token' in card)
      return factions, choose_one_card
  return '', False

def get_required_influence(card):
  # TODO: have a separate file with power and influence cost data
  return False

def is_depleted(card, board, hand, influence):
  return False
