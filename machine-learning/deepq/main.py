from environments import Environment
from agents import DeepQAgent
import os, warnings, sys
# hide warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore")

environment = Environment()

# get the shape of the observation and action space
state_num  = environment.env.observation_space.shape[0]
action_num = environment.env.action_space.n

print("State %2f"  % state_num)
print("Action %2f"  % action_num)

agent = DeepQAgent(state_num, action_num)

if len(sys.argv) > 1 and sys.argv[1] == 'train':
    environment.train(agent)
else:
    agent.is_training = False
    environment.run(agent)
