# Rllib docs: https://docs.ray.io/en/latest/rllib.html
# Malmo XML docs: https://docs.ray.io/en/latest/rllib.html

try:
    from malmo import MalmoPython
except:
    import MalmoPython

import sys
import time
import json
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randint

import gym, ray
from gym.spaces import Discrete, Box
from ray.rllib.agents import ppo


class DiamondCollector(gym.Env):

    def __init__(self, env_config):  
        # Static Parameters
        self.size = 50
        self.cow_density = .01
        self.mushroom_cow_density = .002
        self.obstacle_density = .05
        self.obs_size = 20
        self.max_episode_steps = 100
        self.log_frequency = 10
        self.action_dict = {
            0: 'move 1',  # Move one block forward
            1: 'turn 1',  # Turn 90 degrees to the right
            2: 'turn -1',  # Turn 90 degrees to the left
            3: 'attack 1'  # Destroy block
        }

        # Rllib Parameters
        self.action_space = Box(-1, 1, shape=(3,), dtype=np.float32) #Discrete(len(self.action_dict)) 
        self.observation_space = Box(0, 1, shape=(2 * self.obs_size * self.obs_size, ), dtype=np.float32)
        print(self.action_space)
        print(self.observation_space)

        # Malmo Parameters
        self.agent_host = MalmoPython.AgentHost()
        try:
            self.agent_host.parse( sys.argv )
        except RuntimeError as e:
            print('ERROR:', e)
            print(self.agent_host.getUsage())
            exit(1)

        # DiamondCollector Parameters
        self.obs = None
        self.allow_shoot_action = False
        self.episode_step = 0
        self.episode_return = 0
        self.returns = []
        self.steps = []

    def reset(self):
        """
        Resets the environment for the next episode.

        Returns
            observation: <np.array> flattened initial obseravtion
        """
        # Reset Malmo
        world_state = self.init_malmo()

        # Reset Variables
        self.returns.append(self.episode_return)
        current_step = self.steps[-1] if len(self.steps) > 0 else 0
        self.steps.append(current_step + self.episode_step)
        self.episode_return = 0
        self.episode_step = 0

        # Log
        if len(self.returns) > self.log_frequency + 1 and \
            len(self.returns) % self.log_frequency == 0:
            self.log_returns()

        # Get Observation
        self.obs, self.allow_shoot_action = self.get_observation(world_state)

        return self.obs

    def step(self, action):
        """
        Take an action in the environment and return the results.

        Args
            action: <int> index of the action to take

        Returns
            observation: <np.array> flattened array of obseravtion
            reward: <int> reward from taking action
            done: <bool> indicates terminal state
            info: <dict> dictionary of extra information
        """

        # Get Action
        #[move, turn, attack]
        #sample -> [-1, -1, 0.06] <- npfloat32
        
        move = action[0]
        turn = action[1]
        attack = action[2]
        if attack < 0:
            attack = 0
        else:
            attack = 1
        move_command = "move {}".format(move)
        turn_command = "turn {}".format(turn)
        attack_command = "attack {}".format(attack)
        
        #command = self.action_dict[action]
        if attack_command != 'attack 1' or self.allow_shoot_action==False:
            self.agent_host.sendCommand(move_command)
            self.agent_host.sendCommand(turn_command)
            time.sleep(.2)
            self.episode_step += 1
        else:
            print("go here")
            self.agent_host.sendCommand(attack_command)
            self.agent_host.sendCommand("move 0")
            self.agent_host.sendCommand("turn 0")
            time.sleep(.8)
            self.agent_host.sendCommand("attack 0")
            self.episode_step += 1

        # Get Observation
        world_state = self.agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:", error.text)
        self.obs, self.allow_shoot_action = self.get_observation(world_state) 

        # Get Done
        done = not world_state.is_mission_running 

        # Get Reward
        reward = 0
        for r in world_state.rewards:
            reward += r.getValue()
        self.episode_return += reward

        return self.obs, reward, done, dict()

    def get_mission_xml(self):
        import random

        my_xml = ""
        base_xml = "<DrawEntity x='{}' y='{}' z='{}' type='{}' xVel='1' zVel='1' />"
        cow_probability = int(self.cow_density * 1000)
        mushroom_cow_probability = int(self.mushroom_cow_density * 1000)
        chance = None
        #construct the xml here
        for x in range(-50, 50):
            for z in range(-50, 50):
                chance = random.randint(1, 1000)
                if chance <= mushroom_cow_probability:
                    my_xml += base_xml.format(x, 2, z, 'MushroomCow')
                elif chance <= cow_probability:
                    my_xml += base_xml.format(x, 2, z, 'Cow')

        #print("XML HERE: ", my_xml)

        #drawing glass obstacles in my_xml2
        my_xml2 = ""
        base_xml2 = "<DrawBlock x='{}' y='{}' z='{}' type='{}'/>"
        obstacle_probability = int(self.obstacle_density * 1000)
        chance = None
        #construct the xml here
        for x in range(-50, 50):
            for z in range(-50, 50):
                chance = random.randint(1, 1000)
                if chance <= obstacle_probability:
                    my_xml2 += base_xml2.format(x, 2, z, 'glass')
                    my_xml2 += base_xml2.format(x, 3, z, 'glass')
                if chance <= obstacle_probability * 0.75:
                    my_xml2 += base_xml2.format(x, 4, z, 'glass')
                if chance <= obstacle_probability * 0.5:
                    my_xml2 += base_xml2.format(x, 5, z, 'glass')
                if chance <= obstacle_probability * 0.25:
                    my_xml2 += base_xml2.format(x, 6, z, 'glass')
                    
        return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
                <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

                    <About>
                        <Summary>Diamond Collector</Summary>
                    </About>

                    <ServerSection>
                        <ServerInitialConditions>
                            <Time>
                                <StartTime>12000</StartTime>
                                <AllowPassageOfTime>false</AllowPassageOfTime>
                            </Time>
                            <Weather>clear</Weather>
                        </ServerInitialConditions>
                        <ServerHandlers>
                            <FlatWorldGenerator generatorString="3;7,2;1;"/>
                            <DrawingDecorator>''' + \
                                "<DrawCuboid x1='{}' x2='{}' y1='2' y2='2' z1='{}' z2='{}' type='air'/>".format(-self.size, self.size, -self.size, self.size) + \
                                "<DrawCuboid x1='{}' x2='{}' y1='1' y2='1' z1='{}' z2='{}' type='grass'/>".format(-self.size, self.size, -self.size, self.size) + \
                                my_xml + \
                                my_xml2 + \
                                '''
                                <DrawBlock x='0'  y='2' z='0' type='air' />
                                <DrawBlock x='0'  y='1' z='0' type='stone' />
                            </DrawingDecorator>
                            <ServerQuitWhenAnyAgentFinishes/>
                        </ServerHandlers>
                    </ServerSection>

                    <AgentSection mode="Survival">
                        <Name>CS175DiamondCollector</Name>
                        <AgentStart>
                            <Placement x="0.5" y="2" z="0.5" pitch="45" yaw="0"/>
                            <Inventory>
                                <InventoryItem slot="0" type="bow"/>
                                <InventoryItem slot="1" type="arrow" quantity="64"/>
                            </Inventory>
                        </AgentStart>
                        <AgentHandlers>
                            <ContinuousMovementCommands/>
                            <ObservationFromFullStats/>
                            <ObservationFromRay/>
                            <ObservationFromGrid>
                                <Grid name="floorAll">
                                    <min x="-'''+str(int(self.obs_size/2))+'''" y="-1" z="-'''+str(int(self.obs_size/2))+'''"/>
                                    <max x="'''+str(int(self.obs_size/2))+'''" y="0" z="'''+str(int(self.obs_size/2))+'''"/>
                                </Grid>
                            </ObservationFromGrid>
                            <ObservationFromNearbyEntities>
                                <Range name="Entities" xrange="20" yrange="1" zrange="20" update_frequency="20"/>
                            </ObservationFromNearbyEntities>
                            <RewardForCollectingItem>
                                <Item reward="1" type="diamond"/>
                            </RewardForCollectingItem>
                            <RewardForTouchingBlockType>
                                <Block reward="-1" type="lava" behaviour="onceOnly"/>
                            </RewardForTouchingBLockType>
                            <AgentQuitFromReachingCommandQuota total="'''+str(self.max_episode_steps)+'''" />
                            <AgentQuitFromTouchingBlockType>
                                <Block type="bedrock" />
                            </AgentQuitFromTouchingBlockType>
                        </AgentHandlers>
                    </AgentSection>
                </Mission>'''

    def init_malmo(self):
        """
        Initialize new malmo mission.
        """
        my_mission = MalmoPython.MissionSpec(self.get_mission_xml(), True)
        my_mission_record = MalmoPython.MissionRecordSpec()
        my_mission.requestVideo(800, 500)
        my_mission.setViewpoint(1)

        max_retries = 3
        my_clients = MalmoPython.ClientPool()
        my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000)) # add Minecraft machines here as available

        for retry in range(max_retries):
            try:
                self.agent_host.startMission( my_mission, my_clients, my_mission_record, 0, 'SteakCollector' )
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission:", e)
                    exit(1)
                else:
                    time.sleep(2)

        world_state = self.agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = self.agent_host.getWorldState()
            for error in world_state.errors:
                print("\nError:", error.text)

        return world_state

    def get_observation(self, world_state):
        """
        Use the agent observation API to get a flattened 2 x 20 x 20 grid around the agent. 
        The agent is in the center square facing up.

        Args
            world_state: <object> current agent world state

        Returns
            observation: <np.array> the state observation
            allow_shoot_action: <bool> whether the agent is facing a diamond
        """
        obs = np.zeros((2 * self.obs_size * self.obs_size, )) #cows
        obs2 = np.zeros((2 * self.obs_size * self.obs_size, )) #obstacles
        allow_shoot_action = False

        while world_state.is_mission_running:
            time.sleep(0.1)
            world_state = self.agent_host.getWorldState()
            if len(world_state.errors) > 0:
                raise AssertionError('Could not load grid.')

            if world_state.number_of_observations_since_last_state > 0:
                # First we get the json from the observation API
                msg = world_state.observations[-1].text
                observations = json.loads(msg)

                # Get observation
                print("OBSERVATIONS: ", observations)
                grid = observations['floorAll']
                cows = observations['Entities']
                for i, x in enumerate(cows):
                    obs[i] = x == 'Cow'

                # Rotate observation with orientation of agent
                obs = obs.reshape((2, self.obs_size, self.obs_size))
                yaw = observations['Yaw']
                if yaw >= 225 and yaw < 315:
                    obs = np.rot90(obs, k=1, axes=(1, 2))
                elif yaw >= 315 or yaw < 45:
                    obs = np.rot90(obs, k=2, axes=(1, 2))
                elif yaw >= 45 and yaw < 135:
                    obs = np.rot90(obs, k=3, axes=(1, 2))
                obs = obs.flatten()

                allow_shoot_action = observations['LineOfSight']['type'] == 'Cow'
                
                break

        return obs, allow_shoot_action

    def log_returns(self):
        """
        Log the current returns as a graph and text file

        Args:
            steps (list): list of global steps after each episode
            returns (list): list of total return of each episode
        """
        box = np.ones(self.log_frequency) / self.log_frequency
        returns_smooth = np.convolve(self.returns[1:], box, mode='same')
        plt.clf()
        plt.plot(self.steps[1:], returns_smooth)
        plt.title('Diamond Collector')
        plt.ylabel('Return')
        plt.xlabel('Steps')
        plt.savefig('returns.png')

        with open('returns.txt', 'w') as f:
            for step, value in zip(self.steps[1:], self.returns[1:]):
                f.write("{}\t{}\n".format(step, value)) 


if __name__ == '__main__':
    ray.init()
    trainer = ppo.PPOTrainer(env=DiamondCollector, config={
        'env_config': {},           # No environment parameters to configure
        'framework': 'torch',       # Use pyotrch instead of tensorflow
        'num_gpus': 0,              # We aren't using GPUs
        'num_workers': 0            # We aren't using parallelism
    })

    while True:
        print(trainer.train())
