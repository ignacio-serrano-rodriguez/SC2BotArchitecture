from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.ids.ability_id import AbilityId

class MyBot(BotAI):
	async def on_step(self, iteration: int):
     
		# for loop_larva in self.larva:
		# 	if loop_larva.tag in self.unit_tags_received_action:
		# 		continue
			# while self.can_afford(UnitTypeId.DRONE):
				self.train(UnitTypeId.DRONE)
				# Add break statement here if you only want to train one
			# else:
			# 	# Can't afford drones anymore
			# 	break



def main():
    run_game(
  		maps.get("AcropolisLE"),
        [Bot(Race.Zerg, MyBot(), name="test"),
         Computer(Race.Random, Difficulty.VeryEasy)],
        realtime=False,
    )

if __name__ == "__main__":
    main()