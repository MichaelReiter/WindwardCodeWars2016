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


def search(i, j, me):
    for tile in me.tiles:
        if i == tile.x and j == tile.y:
            return tile


def chooseTileMove(create, expand, mergers, me, inactive):

    # for merge in mergers:
    #   # mergers.0result.2merging.
    #   for hotel in mergers[0][2]:
    #     hotel[1]

    # if we have a tile that can create a merger, pick it
    if len(mergers) > 0:
        i = rand.randint(0, len(mergers) - 1)
        print "\t", "Merging companies."
        return [search(mergers[i][2], mergers[i][3], me), inactive, inactive]
    elif len(create) > 0:
        i = rand.randint(0, len(create) - 1)
        print "\t", "Creating company."
        return [search(create[i][2], create[i][3], me), inactive, inactive]
    elif len(expand) > 0:
        i = rand.randint(0, len(expand) - 1)
        print "\t", "Adding lone block."
        return [search(expand[i][1], expand[i][2], me), inactive, inactive]
    else:
        print "\t", "Randoming..."
        return [random_element(me.tiles), inactive, inactive]


def chooseStockPurchases(options, hotelChains, stockCount):
    return findLargestCompany(hotelChains, stockCount)


def findLargestCompany(hotelChains, stockCount):
    first = hotelChains[0]
    second = hotelChains[0]

    hotels = []
    for hotel in hotelChains:
        hotels.append([hotel, hotel.num_tiles, hotel.num_available_shares])

    hotels = sorted(hotels, key=lambda x: x[1])
    total = 0
    buyList = []
    for hotel in hotels[::-1]:
        print hotel[1],
        if hotel[0].num_tiles > 0:
            if hotel[0].num_available_shares + total >= stockCount:
                print "\n\t\t", "Buying", stockCount - total, "of", hotel[0].name, "\n\n"
                buyList.append(lib.HotelStock(hotel[0], stockCount - total))
                return buyList
            else:
                print "\n\t\t", "Buying", hotel[0].num_available_shares, "of", hotel[0].name, "\n\n"
                buyList.append(lib.HotelStock(hotel[0], hotel[0].num_available_shares))
                total += hotel[0].num_available_shares
    print "\n\t\t", "Can't buy anything of use...", "\n\n"
    return [lib.HotelStock(hotels[0][0], 0)]

def findOurMinStock(stocks):
    min = stocks[0]
    for stock in stocks:
        if min.num_tiles > stock.num_tiles:
            min = stock
    return min
