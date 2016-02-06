import random as rand
import api.units as lib
from api.units import SpecialPowers

# create, expand and mergers are lists of lists

# first priority, try to expand companies we own shares in (mergers)
# next, create companies  (create)
# else, add on to existing companies (expand)

def chooseTileMove(create, expand, mergers, inactive):

  # for merge in mergers:
  #   # mergers.0result.2merging.
  #   for hotel in mergers[0][2]:
  #     hotel[1]

  # if we have a tile that can create a merger, pick it
  if len(mergers) > 0:
    return [mergers[0][1], inactive, inactive]
  elif len(create) > 0:
    return [create[0][1], inactive, inactive]
  else:
    return [expand[0][0], inactive, inactive]
