import PIL
import numpy as np
from PIL import Image

def deck_to_image(deck, scale_factor, colour_for_card):
    img = Image.new( 'RGB', (len(deck),len(deck)), "white") # Create a new black image
    pixels = img.load()

    for i in range(len(deck)):
        pixels[deck[i], i] = colour_for_card(deck[i])
        
    scaled_size = (img.width * scale_factor, img.height * scale_factor)
    return img.resize(scaled_size, resample=PIL.Image.Resampling.NEAREST)

def multiple_decks_to_image(deck_arr, scale_factor, colour_for_card):
    section_width = len(deck_arr[0]) + 1
    img = Image.new( 'RGB', (len(deck_arr) * section_width, len(deck_arr[0])), "white")
    pixels = img.load()
    
    for x in range(len(deck_arr)):
        for i in range(len(deck_arr[x])):
            pixels[(section_width * x) + deck_arr[x][i], i] = colour_for_card(deck_arr[x][i])
            
        for i in range(len(deck_arr[x])):
            pixels[(section_width * x) + len(deck_arr[x]), i] = (0, 0, 150)

    scaled_size = (img.width * scale_factor, img.height * scale_factor)
    return img.resize(scaled_size, resample=PIL.Image.Resampling.NEAREST)

def visualise_deck(deck, display, scale_factor=3, colour_for_card=lambda _: (0,0,0)):    
    img = deck_to_image(deck, scale_factor, colour_for_card)
    display(img)
    
def visualise_multiple_decks(deck_arr, display, scale_factor=3, colour_for_card=lambda _: (0,0,0)):
    img = multiple_decks_to_image(deck_arr, scale_factor, colour_for_card)
    display(img)
    
def interleave(a, b):
    c = np.empty((a.size + b.size,), dtype=a.dtype)
    c[0::2] = a
    c[1::2] = b
    return c

def faro_shuffle(deck):
    half_size = int(len(deck) / 2)
    top_half = deck[:half_size]
    bottom_half = deck[half_size:]
    return interleave(top_half, bottom_half)

def gsr_riffle_shuffle(deck):
    # probability 50% of coming from top packet (0) or bottom packet (1)
    # e.g. 0, 1, 1, 0, 0, 1, ...
    new_sequence_map = np.random.randint(0, 2, len(deck))

    # figure out how many we need in the top packet
    # i.e. how many 0s we have
    cut_index = len(list(filter(lambda x: x == 0, new_sequence_map)))

    top_packet = deck[:cut_index]
    botttom_packet = deck[cut_index:]

    # TODO this could probably be simplfied
    # populate new deck with cards from top / bottom packet
    # based on 0/1 in our map
    new_deck = np.empty(len(deck))
    top_packet_index = 0
    botttom_packet_index = 0
    for i in range(len(new_sequence_map)):
        if (new_sequence_map[i] == 0):
            new_deck[i] = top_packet[top_packet_index]
            top_packet_index = top_packet_index + 1
        else:
            new_deck[i] = botttom_packet[botttom_packet_index]
            botttom_packet_index = botttom_packet_index + 1
    
    return new_deck

def overhand_shuffle(deck):
    
    # probability of splitting at a given card
    # we've chosen 0.15, which is splitting around 8 times
    # in a 52 card deck
    p = 0.15
    
    # for every card in the deck
    # 1 means split
    # 0 means don't split
    random_values = np.random.rand(len(deck))
    split_map = list(map(lambda x: 1 if x <= p else 0, random_values))
    
    new_deck = np.empty(len(deck))
    
    last_split = 0
    for i in range(len(deck)):
        if (split_map[i] == 1):
            new_deck[len(deck)-i:len(deck)-last_split] = deck[last_split:i]
            last_split = i
    new_deck[0:len(deck)-last_split] = deck[last_split:len(deck)]
    return new_deck

def cut(deck, cut_at):
    new_deck = np.empty(len(deck))
    new_deck[:len(deck)-cut_at] = deck[cut_at:]
    new_deck[len(deck)-cut_at:] = deck[:cut_at]
    return new_deck

def split_test_train(arr, percentage):
    split_at = int(arr.shape[0] * percentage)
    return (arr[:split_at], arr[split_at:])