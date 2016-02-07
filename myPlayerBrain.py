# Team Guest
# UVic 2016
# Michael Reiter, Kurt Dorflinger, Juan Carlos Gallegos, Nicholas Kobald

import random as rand
import api.units as lib
from api.units import SpecialPowers

import logic

NAME = "Team Guest"
SCHOOL = "University of Victoria"

#turn_count = 0

def random_element(list):
    if len(list) < 1:
        print "random element from empty list? returning None..."
        return None
    return list[rand.randint(0, len(list) - 1)]


class MyPlayerBrain(object):
    """The Python AI class."""

    def __init__(self):
        self.name = NAME
        self.school = SCHOOL
        if NAME is "Anders Hejlsberg" or SCHOOL is "Windward U.":
            print "Please enter your name and university at the top of MyPlayerBrain.py"

            #The player's avatar (looks in the same directory that this module is in).
            #Must be a 32 x 32 PNG file.
        try:
            avatar = open("avatar.jpg", "rb")
            avatar_str = b''
            for line in avatar:
                avatar_str += line
            avatar = avatar_str
        except IOError:
            avatar = None   # avatar is optional
        self.avatar = avatar

    def Setup(self, map, me, hotelChains, players):
        self.turn_count = 0
        self.drawUsed = False

    def QuerySpecialPowersBeforeTurn(self, map, me, hotelChains, players):
        if (self.turn_count == 0 or self.turn_count == 1) and self.drawUsed == False:
            self.drawUsed = True
            return SpecialPowers.DRAW_5_TILES
        return SpecialPowers.NONE

    def QueryTileOnly(self, map, me, hotelChains, players):
        tile = random_element(me.tiles)
        createdHotel = next((hotel for hotel in hotelChains if not hotel.is_active), None)
        mergeSurvivor = next((hotel for hotel in hotelChains if hotel.is_active), None)
        return PlayerPlayTile(tile, createdHotel, mergeSurvivor)

    def QueryTileAndPurchase(self, map, me, hotelChains, players):
        self.turn_count += 1

        #inactive = next((hotel for hotel in hotelChains if not hotel.is_active), None)

        #Determine what move to do on your turn
        #choice = [tile, created_hotel, merge_survivor]
        choice = self.chooseTileMove(map, me, hotelChains)
        turn = PlayerTurn(tile=choice[0],
                          created_hotel=choice[1], merge_survivor=choice[2])

        if self.turn_count == 6:
            turn.Card = SpecialPowers.BUY_5_STOCK
            turn.Buy.extend(self.chooseStockPurchases(me, hotelChains, 5))
        else:
            #Determine what stocks to buy
            turn.Buy.extend(self.chooseStockPurchases(me, hotelChains, 3))

        # Use our super powers
        if self.turn_count == 5:
            turn.Card = SpecialPowers.FREE_3_STOCK

        return turn

    def QueryMergeStock(self, map, me, hotelChains, players, survivor, defunct):
        myStock = next((stock for stock in me.stock if stock.chain == defunct.name), None)
        trade = myStock.num_shares / 3
        if trade % 2 != 0:
            trade += 1
        sell = myStock.num_shares - trade
        #print "\n\t", myStock.num_shares, "total, selling:", sell, "trading:", trade, "\n"

        return PlayerMerge(sell, 0, trade)

    def checkAdjacentTile(self, map, me, i, j):
        #Possible outcomes: all empty, one+ single, one+ hotel
        empty = 0   # these are the number of empty, single or hotels adjacent to the input tile (i, j)
        single = 0
        hotel = 0

        merging = []
        creating = []

        print i, j,

        #For every adjacent tile, check if it is either empty, single or hotel
        if i > 0:
            curr = map.tiles[i - 1][j]
            if curr.Type == curr.SINGLE:
                single += 1
                creating.append(map.tiles[i - 1][j])
            elif curr.Type == curr.HOTEL:
                hotel += 1
                merging.append((curr, curr.hotel))
            elif curr.Type == curr.UNDEVELOPED:
                empty += 1
        if i < map.width - 1:
            curr = map.tiles[i + 1][j]
            if curr.Type == curr.SINGLE:
                single += 1
                creating.append(map.tiles[i + 1][j])
            elif curr.Type == curr.HOTEL:
                hotel += 1
                merging.append((curr, curr.hotel))
            elif curr.Type == curr.UNDEVELOPED:
                empty += 1
        if j > 0:
            curr = map.tiles[i][j - 1]
            if curr.Type == curr.SINGLE:
                single += 1
                creating.append(map.tiles[i][j - 1])
            elif curr.Type == curr.HOTEL:
                hotel += 1
                merging.append((curr, curr.hotel))
            elif curr.Type == curr.UNDEVELOPED:
                empty += 1
        if j < map.height - 1:
            curr = map.tiles[i][j + 1]
            if curr.Type == curr.SINGLE:
                single += 1
                creating.append(map.tiles[i][j + 1])
            elif curr.Type == curr.HOTEL:
                hotel += 1
                merging.append((curr, curr.hotel))
            elif curr.Type == curr.UNDEVELOPED:
                empty += 1

        if hotel > 0:
            return [hotel + single, "hotel", merging]
        elif single > 0:
            return [single, "single", creating]
        else:
            return [0, "empty"]

    def chooseTileMove(self, map, me, hotelChains):
        create = []
        expand = []
        mergers = []

        # This populates lists for which moves will create a company,
        # which moves will expand a company, and which moves will cause a merger.
        for i in xrange(map.width):
            for j in xrange(map.height):
                for tile in me.tiles:
                    if i == tile.x and j == tile.y:
                        #print "\t\t", True
                        result = self.checkAdjacentTile(map, me, i, j)  # check adjacent tiles to see what it would result in
                        if result[1] == "hotel":
                            mergers.append([result, map.tiles[i][j], i, j])
                        elif result[1] == "single":
                            create.append([result, map.tiles[i][j], i, j])
                        else:
                            expand.append([map.tiles[i][j], i, j])

        #Determine which move you want to use here
        inactive = next((hotel for hotel in hotelChains if not hotel.is_active), None)
        chosen = logic.chooseTileMove(create, expand, mergers, me, inactive)
        if chosen is None:
            return [random_element(me.tiles), inactive, inactive]
        else:
            return chosen

    def chooseStockPurchases(self, me, hotelChains, stockCount):
        options = []

        # Create a list of hotel stocks that can be bought (are active) and the
        # currently owned shares. options = [[hotel, shares owned], ...]
        for hotel in hotelChains:
            if hotel.is_active:
                added = False
                for stock in me.stock:
                    if stock.chain == hotel:
                        added = True
                        options.append([hotel, stock.num_shares])
                        break
                if not added:
                    options.append([hotel, 0])

        # Expects a list in the form of [lib.HotelStock(hotel, purchase amount), ...]
        buyList = logic.chooseStockPurchases(options, hotelChains, stockCount)

        if buyList is None:
            print "Randoming stock..."
            return [lib.HotelStock(random_element(hotelChains), rand.randint(1, 4))]
        else:
            print "Buying: ", buyList
            return buyList


class PlayerMerge(object):
    def __init__(self, sell, keep, trade):
        self.Sell = sell
        self.Keep = keep
        self.Trade = trade


class PlayerPlayTile(object):
    def __init__(self, tile, created_hotel, merge_survivor):
        self.Tile = tile
        self.CreatedHotel = created_hotel
        self.MergeSurvivor = merge_survivor


class PlayerTurn(PlayerPlayTile):
    def __init__(self, tile, created_hotel, merge_survivor):
        super(PlayerTurn, self).__init__(tile, created_hotel, merge_survivor)
        self.Card = lib.SpecialPowers.NONE
        self.Buy = []   # hotel stock list
        self.Trade = []    # trade stock list


class TradeStock(object):
    def __init__(self, trade_in, get):
        self.Trade = trade_in
        self.Get = get
