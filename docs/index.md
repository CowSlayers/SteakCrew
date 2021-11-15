---
layout: default
title:  Home
---

## Welcome 
Welcome to our Cow Slayer Project Page, this is a project for CS 175 - Project in AI (In Minecraft). 
In this project, we apply reinforment learning algorithms to teach our AI agent how to shoot cows with improving accuracy.

Reports:

- [Proposal](proposal.html)
- [Status](status.html)
- [Final](final.html)

Source code: https://github.com/CowSlayers/SteakCrew

## Summary
Our project will involve training an agent to shoot cows effectively. It will be the agent's goal to move, turn, and shoot cows scattered throughout the world. Using Malmo, along with some Reinforcement Learning algorithms, the agent will take in a state which includes the agent's current posititon in (x, y, z) format and the agent's yaw (the direction the agent is facing). The agent's reward for any one mission will be dependant on how many cows were successfull shot. The action space will be continuous and include the following actions: moving forward, turning, and using the bow. This action pool may have more or fewer actions in the future as we learn what creative features we can implement in the agent's mission.
