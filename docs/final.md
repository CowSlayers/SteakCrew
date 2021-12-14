---
layout: default
title: Final Report
---

## Video:

<iframe width="560" height="315" src="https://www.youtube.com/embed/lDvnZDauJ0E" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Project Summary:
Our goal for this project is to train an agent to search for cows and have the agent shoot them with a bow and arrow from a distance. The agent will be placed in an open field, on top of bedrock and set in rainy weather. Each cow is placed randomly throughout the world, and each mission of shooting cows lasts 60 seconds. The cows are able to move around freely, and will run even faster after being hit once by an arrow - if it is not a killshot.

There are obstacles placed around the field with varying heights. This will encourage the agent to move around the obstacles to find and shoot cows, and slightly adjust the pitch angle trajectory of their shot to reach the cow. In order to make the game a bit more exciting, we also decided to add in exploding arrows. These special arrows can be created through the command block in Minecraft. When there is a clear line of sight to a cow, the arrow damages them normally. When the agent sees an obstacle, the arrows will explode on impact and act similarly to as if it were hit by a TNT. This makes subsequent shots to cows easier as glass obstacles are destroyed, and more direct lines of sight are opened up for cows within shooting distance.

Each time a cow is hit, there will be a reward of 1, defined as a reward for damaging an entity in the mission XML. Obtaining a beef or leather item yields the greatest reward of 2, as that is a cost-effective method to determine whether a cow has been killed. The goal is to defeat as many cows as possible within the 1 minute time frame. Reinforcement learning will encourage the agent in getting around obstacles, detecting shootable cows, and defeating as many as possible each mission. Our project uses Malmo, an AI platform set in Minecraft.

## Approach:
Our approach uses proximal policy optimization, a form of reinforcement learning for our agent in relation to continuous aiming actions at cows. We have the agent use observations from nearby entities to determine which cows are within shooting range, and then target the nearest cow to damage using an observation list sorted by distance to the agent.

`cows = sorted([ent for ent in observations["entities"][1:] if ent['name'] in ['Cow', 'MushroomCow']], key=lambda x: math.sqrt((x['x']-agent_info['x'])**2 + (x['z']-agent_info['z'])**2))`

To detect the cow, we are also using ObservationFromRay’s “LineOfSight” JSON object. This is convenient, because the agent’s first person view while holding a bow and arrow shows that exact observation space in the center of the screen in the form of a “+” sign. We are then utilizing data such as the cows’ positions, agent’s position, pitch, and yaw to determine the best shot to take. We have the agent calculate the correct amount of degrees to turn in order to face the cow directly and shoot it quickly. We used `direction_vector = [cow_vector[0] - agent_vector[0], cow_vector[1] - agent_vector[1]]` to determine the x and z components for where the cow is relative to the agent. We then applied `radians = math.atan2(direction_vector[1],direction_vector[0])` to calculate the right angle between the two. Converting `degrees = radians * 180 / math.pi`, and setting `yaw = degrees - 90` gave us the correct yaw for the agent to turn to when shooting, since Minecraft’s yaw and coordinate system do not match up with conventional wisdom or the debug values we printed to the console. As a good linear approximation for how high or low to shoot, we used `pitch = 4 - (distance/2)`, as further cows require higher aiming and a lower pitch value.

As stated earlier, in the XML, we are utilizing RewardForDamagingEntity to give a reward of 1 whenever either a Cow or MushroomCow is hit. One shot does not always kill a cow, and it may end up successfully running away. In order to determine whether a cow has been killed, we needed to get creative and use RewardForCollectingItem. When the cow is killed, a beef or leather item is dropped. Only when the agent goes toward it and picks it up do we know that the cow was previously killed. So, using ObservationsFromNearbyEntities, we took a similar approach for walking directly towards beef and leather items. The items are given priority over shooting the cows, as the reward is greater, but the agent is only given `time.sleep(2)` seconds before the next set of observations is evaluated.

The setup to have arrows explode on impact was tricky, but a few tutorials helped us achieve the right functionality. We used the pynput library to control automated mouse and keyboard movement at the start of each mission, and we were able to access Minecraft’s in-game command line using the “chat” command. Using a specific sequence of commands for mouse positioning and key presses, we have the agent set up exploding arrows at the start of each mission (see Exploding Arrows Setup tutorial for the actual commands).

## Evaluation: 
Quantitative Evaluation: Our main form of quantitative evaluation is the reward value incremented by damaging entities and for collecting items. The agent receives a reward of 1 for damaging cows and mushroom cows, and a reward of 2 for picking up beef and leather. Rather than evaluating based on the number of dead cows in the game, we evaluate based on the number of times cows have been damaged, and number of items collected, since beef and leather items are only dropped after killing a cow.

We expect the number of arrows shot to increase as the agent slowly trains using the PPO (Proximal Policy Optimization) Trainer, which basically takes the ratio of a current and baseline policy, calculating an advantage for each action by comparing it to the average action for each state. The policy is expected to improve incrementally over time, resulting in slightly greater rewards on average. Importantly, new policies won’t be significantly different from old policies since the change is clipped by the epsilon hyperparameter (see more info on the math for PPO). Overall, our results show an improvement of approximately .78828 in return per 10,000 steps on average.

Qualitative Evaluation: Our agent passes the following sanity cases: setting up the command blocks, firing an arrow, adjusting pitch and yaw, and general movement. The agent is able to reliably detect nearby cows and walk towards their dropped beef and leather items. We notice the agent’s performance across multiple runs improves after around 30000-40000 steps, as the agent appears faster and takes less time in between making shots, which is in line with what our goal was - to optimize for killing cows.

![Rewards over time 5hr](https://github.com/CowSlayers/SteakCrew/blob/main/static/returns5hrs.png?raw=true)

![Rewards over time 7hr](https://github.com/CowSlayers/SteakCrew/blob/main/static/results7hrs.png?raw=true)

The images above show the rewards earned over time in relation to the amount of steps taken. The first is a 5 hour test run reaching 40000 steps, and the second is a 7 hour test run at nearly 60000 steps. From these graphs, our Cow Shooter agent sees modest improvements in its cow-slaying capabilities over time. Fine-tuning various parameters such as pitch angle, the agent’s base movement, cow entity/block placement, and different time delays between send commands could yield even greater improvement from training, but these results are satisfactory.

## References: 
Public Malmo Github:
https://github.com/microsoft/malmo/blob/master/Schemas/Types.xsd

XML Schema Documentation:
http://microsoft.github.io/malmo/0.16.0/Schemas/MissionHandlers.html

Simulating Key Presses:
https://pypi.org/project/pynput/
https://www.youtube.com/watch?v=DTnz8wA6wpw

Exploding Arrows Setup:
https://youtu.be/8EzKGEGTe_E?t=121

More Info on Proximal Policy Optimization:
https://spinningup.openai.com/en/latest/algorithms/ppo.html
