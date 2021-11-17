---
layout: default
title: Status
---

# Click to Watch

[![Watch the video](https://i.imgur.com/WemUoPa.jpeg)](https://www.youtube.com/watch?v=EoC5cjQLEZE){:width="30px"}

## Project Summary:
Since things may have changed since proposal (even if they haven’t), write a short paragraph summarizing the goals of the project (updated/improved version from the proposal).

Our goal for this project is to train an agent to search for cows and have the agent shoot them with a bow and arrow from a distance. The agent will be placed in an open field, with each cow placed in a random subsection of the world. The cows will be able to move around freely, and will run even faster after being hit once by an arrow — if it is not a killshot. There will be obstacles placed around the field with varying heights. This will force the agent to either move around the obstacles to find and shoot the cows, or change the angle and trajectory of their shot.
Each time a cow is hit, there will be a reward, while misses will be penalized, and hitting obstacles will be penalized further. The goal is to defeat as many cows as possible within the time frame of 1 minute. The agent should learn to avoid obstacles, find cows, and defeat as many as possible in a short time. We’ll be using Malmo for our project, set in Minecraft.


## Approach:
Give a detailed description of your approach, in a few paragraphs. You should summarize the
main algorithm you are using, such as by writing out the update equation (even if it is off-the-shelf). You should also give details about the approach as it applies to your scenario. For example, if you are using reinforcement learning for a given scenario, describe the setup in some detail, i.e. how many states/actions you have, what does the reward function look like. A good guideline is to incorporate sufficient details so that most of your approach is reproducible by a reader. I encourage you to use figures for this, as appropriate, as we used in the writeups for the assignments. I recommend at least 2-3 paragraphs.

We are using reinforcement learning for our agent in relation to continuous aiming actions at cows. We have the agent use its nearby observations to determine whether it is close to any cows, and then locate the most efficient cow to damage. To detect the cow, we are using the observation’s “LineOfSight” to detect the cows, which are type “entity” We are then utilizing data such as the cows’ locations, agent’s yaw, pitch, and direction to determine the best shot. The agent must turn the right amount to face the moving cow and damage it quickly. 
In the XML, we are utilizing the RewardForDamagingEntity element of Malmo to give a reward of 1 whenever either a Cow or MushroomCow is hit. As for the penalty for hitting a diamond block obstacle, we use RewardforTouchingBlockType in the XML to give a reward -1. When the agent sends a command to shoot an arrow, but misses the cow, we give a reward -1.


## Evaluation: 
An important aspect of your project, as we mentioned in the beginning, is evaluating your
project. Be clear and precise about describing the evaluation setup, for both quantitative and qualitative results. Present the results to convince the reader that you have a working implementation. Use plots, charts, tables, screenshots, figures, etc. as needed. I expect you will need at least a 1-2 paragraphs to describe each type of evaluation that you perform.

Quantitative Eval: Currently, we are rewarding the agent with a reward for 1 for damaging a cow upon damaging a cow with an arrow. Rather than evaluating based on the number of dead cows in the game, we have decided to switch to damaging cows as our main source of quantitative evaluation for now. We expect the number of hits to increase as the agent slowly improves. Other stats such as shots missed can be used as a penalty or a gauge to our agent's performance. Our agent does not currently deal with shots missed.

Qualitative Eval: Our agent passes the following sanity cases:  firing an arrow, moving, and facing different directions. We are able to pass our baseline case to shoot down one cow. To better visualise the algorithm working within the game, we will have our project record and output data used to create error charts and graphs. This will allow us to compare different implementations and visualize the agent’s performance across multiple games. The moonshot case is to have 100% accuracy killing all the cows (each arrow hits a cow), but a value close to 100% would also indicate the algorithm is effective.

![Rewards over time](https://github.com/CowSlayers/SteakCrew/blob/main/static/returns.png?raw=true)


## Remaining Goals and Challenges: 
In a few paragraphs, describe your goals for the next 4-5 weeks, when the final report is due. At the very least, describe how you consider your prototype to be limited, and what you want to add to make it a complete contribution. Note that if you think your algorithm is quite good, but have not performed sufficient evaluation, doing them can also be a reasonable goal. Similarly, you may propose some baselines (such as a hand-coded policy) that you did not get a chance to implement, but want to compare against for the final submission. Finally, given your experience so far, describe some of the challenges you anticipate facing by the time your final report is due, how crippling you think it might be, and what you might do to solve them.

For the next 3-4 weeks, we want to improve our algorithm and its ability to avoid an increased amount of obstacles. We wanted to test the agent’s ability to locate and shoot cows before adding as many obstacles as we had hoped. We also want to add some more variables to the project to make it more exciting, now that the foundation is complete. The main focus is to improve the agent’s ability to learn quickly and damage the cows.
Some challenges we might encounter will probably be learning how to utilize all the Malmo elements and functions efficiently. We may encounter some bumps when trying to teach the agent to see both the obstacles and cows and determine how to get around the blocks to reach the cows. To solve this, we will need to use sources such as the Malmo Github to better our understanding of Malmo documentation. We can also research more about reinforcement learning in regards to continuous aim. 

## Resources Used: 
Public Malmo Github:
https://github.com/microsoft/malmo/blob/master/Schemas/Types.xsd

XML Schema Documentation:
http://microsoft.github.io/malmo/0.16.0/Schemas/MissionHandlers.html


