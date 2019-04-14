import random
import decklist_parser
import card_info

'''
'good hand' simulator

define a good hand as: X-Y power, XXYZ influence, undepleted power for turn 3, 'has N of [cards 1 2 3]

simulate eternal's mulligan rules and mulligan based on the above

Input: decklist, definition of good hand, output odds of getting a good hand
use this to tweak powerbase

can also define tiers of hands, and odds of each given mull

TODO: move data to a separate file (data => which cards are which types
TODO: simulate cards 'plays unit' for banner, 'draws card' for card-draw

# TODO: 'good hand function generator functions'
# Then a good_hand definition can be created with AND(HAS_POWER(3,5), HAS_INFLUENCE('TPS'))

# TODO: have a concept of 'things that are bad for a hand' and count how many problems a hand has. A hand is good if the problem count is <= x, or strength count is >=y

TODO: output information on why hands are generally bad (too much power, too little power, missing influence) and also on redundant influence
'''

decklist = '''
2 Lethrai Lobotomy (Set5 #152)
4 Pitfall Trap (Set5 #116)
4 Rat Cage (Set5 #153)
1 Secret Passage (Set5 #154)
3 Suffocate (Set1 #251)
3 Curator's Spear (Set5 #157)
4 Equivocate (Set1003 #21)
4 Lethrai Courtier (Set5 #220)
3 Lethrai Hideaway (Set5 #192)
4 Teacher of Humility (Set4 #67)
4 Display of Knowledge (Set5 #233)
2 Ebon Dune Smuggler (Set5 #221)
4 Great Valley Smuggler (Set5 #204)
1 Clock of Stolen Hours (Set1005 #7)
4 Severin, the Mad Mage (Set1005 #26)
3 Jotun Hurler (Set1 #227)
2 Time Sigil (Set1 #63)
4 Amber Waystone (Set3 #51)
1 Crest of Cunning (Set3 #267)
2 Crest of Mystery (Set4 #266)
2 Crest of Wisdom (Set3 #261)
4 Diplomatic Seal (Set1 #425)
3 Elysian Banner (Set1 #421)
4 Feln Banner (Set1 #417)
3 Xenan Banner (Set2 #201)
--------------MARKET---------------
1 Dissociate (Set5 #44)
1 Vara's Choice (Set2 #206)
1 Xenan Obelisk (Set1 #103)
1 Bazaar Stampede (Set5 #206)
1 Praxis Banner (Set2 #171)
'''

def count_power(cards):
  power_in_hand = sum(card_info.is_power(card) for card in cards)

def draw_hand(deck, draw_number):
  if draw_number not in (1,2,3):
    raise Exception('draw_number should be 1-3, but was %s' % draw_number)
  random.shuffle(deck)
  hand_size = 6 if draw_number == 3 else 7
  if draw_number == 1:
    hand = deck[:7]
    while count_power(hand) in (0,7):
      hand = deck[:7]
  else:
    deck_power = [card for card in deck if card_info.is_power(card)]
    deck_non_power = [card for card in deck if not card_info.is_power(card)]
    num_power = random.randint(2,4)
    hand = deck_power[:num_power] + deck_non_power[:hand_size - num_power]
  return hand


def mulligan_for_good_hand(deck_txt, good_hand_fn):
  deck = decklist_parser.parse_decklist(deck_txt)
  for i in range(1,4):
    hand = draw_hand(deck, 1)
    if good_hand_fn(hand):
      return True
  return False

def has_345_power_and_tps_influence(hand):
  power_in_hand = sum(card_info.is_power(card) for card in hand)
  pledge_in_hand = 1 if any(card_info.is_pledge(card) for card in hand) else 0
  # only use the pledge card as power if you would otherwise have too little power
  influence_in_hand = set()
  for card in hand:
    # TODO: use the 'goal' for choices like diplo and pledge
    # TODO: use a counter object to support multiple of the same influence
    influence_from_card, is_choose_one_card = card_info.get_influence_produced(card)
    influence_in_hand.update(influence_from_card)
  #print('this hand\'s influence is %s' % influence_in_hand)
  good_amount_of_power = (power_in_hand in (3,4,5)) or (pledge_in_hand + power_in_hand == 3)
  good_influence = set('TPS').issubset(influence_in_hand)
  if not good_influence:
    print('This hand is missing: %s' % (set('TPS') - influence_in_hand))
  return good_amount_of_power and good_influence

def main():
  simulation_count = 10
  good_hands = 0
  for _ in range(simulation_count):
    good_hands += 1 if mulligan_for_good_hand (decklist, has_345_power_and_tps_influence) else 0
  print('%s%% of %s hands were good' % (100 * good_hands // simulation_count, simulation_count))

if __name__ == '__main__':
  main()
