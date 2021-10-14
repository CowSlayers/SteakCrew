---
layout: default
title: Proposal
---

## Summary

Our goal for this project is to train an agent to search for cows and shoot them with a bow and arrow from a distance. We will be using Malmo for our project, set in Minecraft. The agent will be placed on an open field with cows scattered around the world. The start position of the agent and cows will be inputs. Some outputs include the bow and arrow angle, the power of the shot, which direction the agent is facing and/or moving, and whether the cow was hit. When cows are hit, there will be a reward, and misses will be penalized. The goal is to hit as many cows as possible within the time frame of 1 minute.

## AI/ML Algorithms

We will use reinforcement learning in relation to continuous aiming actions at cows.

## Evaluation Plan

Quantitative Eval:
We will measure the total number of shots taken and dead cows in each game. Our main baseline will be 1 cow within the minute. We expect our approach to improve the number of kills in the given time frame, increasing by 3-5. Furthermore, there should be less shots taken, in other words a higher accuracy. The main data we will evaluate our success on is the total count of dead cows. The higher the number, the better our algorithm is.

Qualitative Eval:
To verify our project is working, we will begin with some sanity cases. We will ensure the agent is able to fire the arrow, face and move in different directions, detect a cow, and kill a cow. Once these are working accurately, we will continue on with the game. To better visualise the algorithm working within the game, we will have our project record and output a sort of error chart or graph. This will allow us to compare and see the project working in multiple games. Our moonshot case is to have 100% accuracy when killing all the cows, as in one shot per cow.

## Appointmnet with the Instructor
October 19, 2021
4 - 4:15 pm