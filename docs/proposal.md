---
layout: default
title: Proposal
---

## Summary

Our goal for this project is to train an agent to search for cows and have the agent shoot them with a bow and arrow from a distance. The agent will be placed in an open field, and each cow will be placed in a random subsection of the world (likely in the shape of a circle), where they are free to move around only within that subsection. The inputs will be the positions of the agent and cows (with that information, we’d keep track of direction vectors to each cow). Some outputs include the vertical angle of the bow and arrow, which direction the agent is facing and/or moving, the power/magnitude of the shot, and whether the cow was hit. Each time a cow is hit, there will be a reward, and misses will be penalized a large amount. The goal is to defeat as many cows as possible within the time frame of 1 minute. We’ll be using Malmo for our project, set in Minecraft.

## AI/ML Algorithms

We will likely use reinforcement learning in relation to continuous aiming actions at cows, and possibly Deep Q-Learning, using neural networks to approximate the optimal Q-function.

## Evaluation Plan

Quantitative Eval:
We will measure the total number of arrows shot and the number of dead cows in each game (if a cow takes more than 1 shot to kill, then we’ll also measure the total number of arrows that successfully hit a cow). Our main baseline will be to kill 1 cow within the minute. We expect our approach to improve the number of kills in the given time frame, increasing to at least 3-5 kills with faster detection and targeting. Furthermore, after training, there should be less shots taken to kill the same number of cows, which results in a higher accuracy and greater overall score (total rewards - penalties). The main data we will evaluate our success on is the total count of dead cows within the 1 minute. A greater number indicates a better algorithm for the agent to quickly search for and execute cows.

Qualitative Eval:
To verify our project is working, we will begin with some sanity cases. We will ensure the agent is able to fire the arrow, and face/move in different directions. Once these are working accurately, we will continue on with algorithms for detecting and moving within range to shoot a cow, and kill a cow with appropriately-fired arrows (adjusting vertical angle and power as needed). To better visualise the algorithm working within the game, we will have our project record and output data used to create error charts and graphs. This will allow us to compare different implementations and visualize the agent’s performance across multiple games. The moonshot case is to have 100% accuracy killing all the cows (each arrow hits a cow), but a value close to 100% would also indicate the algorithm is effective.

## Appointmnet with the Instructor
October 19, 2021
4 - 4:15 pm