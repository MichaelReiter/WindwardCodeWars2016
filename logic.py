import random as rand
import api.units as lib
from api.units import SpecialPowers

# create, expand and mergers are lists of lists

# first priority, try to expand companies we own shares in (mergers)
# next, create companies  (create)
# else, add on to existing companies (expand)


def random_element(list):
    if len(list) < 1:
        print "random element from empty list? returning None..."
        return None
    return list[rand.randint(0, len(list) - 1)]


def chooseTileMove(create, expand, mergers, me, inactive):

    # for merge in mergers:
    #   # mergers.0result.2merging.
    #   for hotel in mergers[0][2]:
    #     hotel[1]

    # if we have a tile that can create a merger, pick it
    if len(mergers) > 0:
        # examine each possible merger
        # for merge in mergers:
        #     if len(merge[0][2]) > 1:
        #         # we want to know if we would benefit from the merger
        #         # find largest company
        #         largest = merge[0][2][0]    # this is a tuple
                
        #         for move in merge[0][2]:
        #             hotel = move[1]


        return [mergers[0][1], inactive, inactive]

    elif len(create) > 0:
        return [create[0][1], inactive, inactive]
    elif len(expand) > 0:
        return [expand[0][0], inactive, inactive]
    else:
        return [random_element(me.tiles), inactive, inactive]


def chooseStockPurchases(options, hotelChains):
    return [lib.HotelStock(findLargestCompany(hotelChains), 3)]

def findLargestCompany(hotelChains):
    max = hotelChains[0]
    for hotel in hotelChains:
        if max.num_tiles < hotel.num_tiles:
            max = hotel
    return max

def findOurMinStock(stocks):
    min = stocks[0]
    for stock in stocks:
        if min.num_tiles > stock.num_tiles:
            min = stock
    return min