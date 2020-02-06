# from maze_env import Maze
from stock_env import stock
from RL_brain import DeepQNetwork
import pandas as pd


def game_step(observation, step=None, train=True, show_log=False):
    
    # RL choose action based on observation
    action = RL.choose_action(observation, train)

    # RL take action and get next observation and reward
    observation_, reward, done = env.step(action, show_log)

    RL.store_transition(observation, action, reward, observation_)
    # print("total profit:%.3f" % env.total_profit, end='\r')
    if step and (step > 200) and (step % 5 == 0):
        RL.learn()

    # swap observation
    observation = observation_
    
    return observation, done
    

def run(max_round):
    step = 0
    for episode in range(max_round):
        # initial observation
        observation = env.reset()

        while True:
            
            observation, done = game_step(observation, step=step)
            # print(observation)
            # break while loop when end of this episode
            if done:
                break
            step += 1
        
        print('epoch:%d, total_profit:%.3f' % (episode, env.total_profit))
        # BackTest(False)


def BackTest(env, show_log=True):
    observation = env.reset()
    step=0
    while True:
        observation, done = game_step(observation, train=False, show_log=show_log)
        # break while loop when end of this episode
        if done:
            break
    print('total_profit:%.3f' % (env.total_profit))
    return env


if __name__ == "__main__":
    max_round = 50
    file_path = '000065.SZ_NormalData.csv'
    df = pd.read_csv(file_path)
    df = df.sort_values('trade_date', ascending=True)
    trend = df.close.values.tolist() #选取收盘数据做测试
    env = stock(trend[0:1750])
    RL = DeepQNetwork(env.n_actions, env.n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=3000,
                      # output_graph=True
                      )
    
    run(max_round)
    env = stock(trend[1750:])
    env = BackTest(env, show_log=False)
    env.draw()
    # RL.plot_cost()