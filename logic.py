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
    #Find the PlayerTile associated with a given i,j on the game board
    for tile in me.tiles:
        if i == tile.x and j == tile.y:
            return tile


def chooseTileMove(create, expand, mergers, me, inactive):
    # If we have tiles that can create a company, then randomly pick one
    if len(create) > 0:
        i = rand.randint(0, len(create) - 1)
        return [search(create[i][2], create[i][3], me), inactive, inactive]
    # Try to merge companies next or grow one if we have a tile to do so
    elif len(mergers) > 0:
        i = rand.randint(0, len(mergers) - 1)
        return [search(mergers[i][2], mergers[i][3], me), inactive, inactive]
    # Otherwise add a lone block
    elif len(expand) > 0:
        i = rand.randint(0, len(expand) - 1)
        return [search(expand[i][1], expand[i][2], me), inactive, inactive]
    # Random from the tiles if no player tiles match
    else:
        return [random_element(me.tiles), inactive, inactive]


def chooseStockPurchases(options, hotelChains, stockCount):
    return findLargestCompany(hotelChains, stockCount)


def findLargestCompany(hotelChains, stockCount):
    hotels = []
    for hotel in hotelChains:
        hotels.append([hotel, hotel.num_tiles, hotel.num_available_shares])

    # Sort hotels by number of tiles
    hotels = sorted(hotels, key=lambda x: x[1])
    total = 0
    buyList = []

    # Invest as much as possible in the largest hotel
    for hotel in hotels[::-1]:
        # Only invest in existing hotels
        if hotel[0].num_tiles > 0:
            # Check to see if we have invested in the max amount of stocks and stop investing
            if hotel[0].num_available_shares + total >= stockCount:
                buyList.append(lib.HotelStock(hotel[0], stockCount - total))
                return buyList
            # Otherwise invest if possible
            else:
                buyList.append(lib.HotelStock(hotel[0], hotel[0].num_available_shares))
                total += hotel[0].num_available_shares
    return [lib.HotelStock(hotels[0][0], 0)]
