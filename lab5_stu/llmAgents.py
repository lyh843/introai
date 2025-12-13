# llmAgents.py
# -------------
# LLM-driven agents for Pacman game

from game import Agent, Directions
from openai import OpenAI
import os
import re
import datetime

# ANSI colors for console output
BLUE = "\033[94m"   # User Input
RED = "\033[91m"    # Model Output
RESET = "\033[0m"   # Reset Color

class LLMPacmanAgent(Agent):
    """
    A Pacman agent that uses a Large Language Model to make decisions.
    """

    def __init__(self, index=0):
        super().__init__(index)
        
        self.api_key=os.getenv("DEEPSEEK_API_KEY")   
        self.student_id = os.getenv("STUDENT_ID", "Unknown")     

        self.client = OpenAI(
            api_key=os.environ.get('DEEPSEEK_API_KEY'),
            base_url="https://api.deepseek.com/v1")
        # Setup Logging
        if not os.path.exists("log"):
            os.makedirs("log")
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.log_file_path = f"log/{timestamp}_{self.student_id}.log"
        print(f"Log file: {self.log_file_path}")

    def getAction(self, state):
        # 1. Extract raw game data (Independent variables)
        
        # 2. Format data into a string
        # 3. Get the student's prompt
        prompt = self.createPrompt(state)
        
        print(f"{BLUE}[SENDING USER INPUT]:\n{prompt}{RESET}")
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat", 
                messages=[
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0
            )

            llm_output = response.choices[0].message.content

            print(f"{RED}[RESPONSE]\n{llm_output}{RESET}")
            
            action = self.extractAction(llm_output)
            print(f"Action Executed: {action}")
            
            self.log_transaction(prompt, llm_output, action)

            # Validate Action
            legal_actions = state.getLegalPacmanActions()
            if action in legal_actions:
                return action
            else:
                import random
                return random.choice(legal_actions) if legal_actions else Directions.STOP

        except Exception as e:
            print(f"API Error: {e}")
            return Directions.STOP

    def createPrompt(self,state):
        """        
        --- DETAILS OF game_data---
        
        1. layout_list: (List of Strings) ["(0,0)=Wall", "(1,0)=Pacman"...]
        2. pacman_pos: (List of Integers) [x, y]
        3. ghost_pos: (List of Lists) [[x, y], [x, y]]
        4. score: (Integer)
        5. food_count: (Integer)
        6. legal_actions: (List of Strings) ['North', 'South', ...]

        --- SUGGESTED BASIC PROMPT STRUCTURE ---
        
        1. Role & Goal: "You are Pacman. Eat food and avoid ghosts."
        2. State Analysis: "Analyze the game state provided above."
        
        --DO NOT MODIFY THE format_prompt--
        """
        game_data = self.get_game_data(state)
        
        prompt = f"""
        "*** YOUR PROMPT HERE ***" 
            你现在是一个吃豆人。你要在避开ghosts的前提下，吃掉图中的所有食物。
            这个是当前的游戏数据：
            
            ================
            
            {game_data}
            
            ================
            
            数据含义： 
            1. layout_list: (List of Strings) ["(0,0)=Wall", "(1,0)=Pacman"...]
            2. pacman_pos: (List of Integers) [x, y]
            3. ghost_pos: (List of Lists) [[x, y], [x, y]]
            4. score: (Integer)
            5. food_count: (Integer)
            6. legal_actions: (List of Strings) ['North', 'South', ...]
            
            ================
            
            方向声明：'north'会使 y 减小，'south'会使 y 增加，'west'会使 x 减小，'east'会使 x 增加
            
            你的思路应该是：
            1. 从'legal_actions'中剔除掉'stop'，然后对剩下的动作进行遍历，思考选择这个动作后到达的新位置。
            2. 再从这个位置出发，遍历'north', 'south', 'west', 'east'，然后判断指向那个方向后会不会到'wall', \
                如果会的话就不选择那个方向；以及是否会回到上一个格子，如果会的话也不加到路径中。重复这个步骤5次，行程多组路径。
            3. 判断这两条条路径上是否存在ghosts
                如果存在一条路径没有ghosts，选择这条路径的第一步。
                否则选择ghosts出现得最晚的路径或者出现了食物的那一条路径。
            
            ===============
            下面给出一个示例：
            
            'layout_list': ['(0,0)=Wall,(1,0)=Wall,(2,0)=Wall,(3,0)=Wall,(4,0)=Wall,(5,0)=Wall,(6,0)=Wall', 
                            '(0,1)=Wall,(1,1)=Empty,(2,1)=Pacman,(3,1)=Empty,(4,1)=Empty,(5,1)=Empty,(6,1)=Wall', 
                            '(0,2)=Wall,(1,2)=Empty,(2,2)=Wall,(3,2)=Wall,(4,2)=Wall,(5,2)=Empty,(6,2)=Wall', 
                            '(0,3)=Wall,(1,3)=Empty,(2,3)=Wall,(3,3)=Food,(4,3)=Empty,(5,3)=Empty,(6,3)=Wall', 
                            '(0,4)=Wall,(1,4)=Empty,(2,4)=Wall,(3,4)=Wall,(4,4)=Wall,(5,4)=Empty,(6,4)=Wall', 
                            '(0,5)=Wall,(1,5)=Food,(2,5)=Empty,(3,5)=Ghost1,(4,5)=Empty,(5,5)=Empty,(6,5)=Wall', 
                            '(0,6)=Wall,(1,6)=Wall,(2,6)=Wall,(3,6)=Wall,(4,6)=Wall,(5,6)=Wall,(6,6)=Wall'], 
            'pacman_pos': [2, 1], 
            'ghost_pos': [[3, 5]], 
            'score': 0.0, 
            'food_count': 2, 
            'legal_actions': ['West', 'Stop', 'East']
            
            分析：
            目前的位置在 [2, 1]，合法的操作去掉'stop'后，是 'West'和'East'。
            那么有两条路径可选，
            路径一目前是: '[2, 1], [1, 1]' (执行West后到达新位置[1, 1])
            路径二目前是：'[2, 1], [3, 1]' (执行East后到达新位置[3, 1])
            
            走了一步之后，需要开始进入思路的第2步
            遍历'north', 'south', 'west', 'east'，
            针对路径一：
                - 'north' 'west'对应的位置是'wall'，不可选
                - 'east'对应的位置'[2, 1]'已经出现在了路径一中了，因此也不选
            故路径一新执行的action 应该是 'south'
            路径一更新为：'[2, 1], [1, 1], [1, 2]'
            同理，针对路径二：
                - 'north' 'south'对应的位置是'wall'，不可选
                - 'west'对应的位置'[2, 1]'已经出现在了路径一中了，因此也不选
            故路径二新执行的action 应该是 'east'
            路径二更新为：'[2, 1], [3, 1], [4, 2]'
            
            重复这个更新步骤5次，最后应该能得到
            路径一：'[2, 1], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [2, 5]'
            路径二：'[2, 1], [3, 1], [4, 1], [5, 1], [5, 2], [5, 3], [4, 3]'
            路径三：'[2, 1], [3, 1], [4, 1], [5, 1], [5, 2], [5, 3], [4, 4]'
            注意到这里的路径三的来源是因为原始的路径二拓展到'[5, 3]'时，发现'west'和'south'都是可选动作，
            针对这种大于一个可选动作的情况，可以复制该路径，然后两条路径分别执行不同动作。
            
            那么开始判断三个路径谁最优了，首先三个路径上都没有ghost出现，因此三条都是可选的。
            其次在第一条路径中出现了食物，而路径二、三没有，因此优先选择路径一。
            结果应该输出'West'。
            
            ===============
            
            请你每次给出结果的时候认真进行逐步思考，如同我的样例一样。
            
        """
        format_prompt="""输出最终行动，格式必须严格如下：<action>行动</action>。其中"行动"必须是以下之一: North, South, East, West, Stop\n 例如：<action>North</action>"""  
        return prompt + "\n" + format_prompt

    def get_game_data(self, state):
        """
        Extracts independent variables from the game state.
        """
        layout = state.data.layout
        width = layout.width
        height = layout.height
        pacman_pos = state.getPacmanPosition()
        ghost_positions = [state.getGhostPosition(i) for i in range(1, state.getNumAgents())]

        # Coordinate conversion (0,0 at bottom-left)
        pacman_display = [int(pacman_pos[0]), height - 1 - int(pacman_pos[1])]
        ghost_display = [[int(g[0]), height - 1 - int(g[1])] for g in ghost_positions]

        layout_rows = []
        for y in range(height):
            row_items = []
            for x in range(width):
                pacman_y = height - 1 - y
                if (x, y) == tuple(pacman_display): cell = "Pacman"
                elif [x, y] in ghost_display: 
                    idx = ghost_display.index([x, y]) + 1
                    cell = f"Ghost{idx}"
                elif layout.walls[x][pacman_y]: cell = "Wall"
                elif state.hasFood(x, pacman_y): cell = "Food"
                elif (x, pacman_y) in state.getCapsules(): cell = "Capsule"
                else: cell = "Empty"
                row_items.append(f"({x},{y})={cell}")
            layout_rows.append(",".join(row_items))

        return {
            "layout_list": layout_rows,
            "pacman_pos": pacman_display,
            "ghost_pos": ghost_display,
            "score": state.getScore(),
            "food_count": state.getNumFood(),
            "legal_actions": state.getLegalPacmanActions()
        }

    def log_transaction(self, full_input, response, action):
        """
        Save interaction to log file.
        """
        with open(self.log_file_path, "a", encoding="utf-8") as f:
            f.write(f"TIME: {datetime.datetime.now()}\n")
            f.write(f"--- FULL USER INPUT ---\n{full_input}\n")
            f.write(f"--- RESPONSE ---\n{response}\n")
            f.write(f"--- ACTION ---\n{action}\n")
            f.write("-" * 30 + "\n")

    def extractAction(self, llm_response):
        """
        Extracts the action from <action>...</action> tags.
        """
        matches = re.findall(r'<action>\s*(.*?)\s*</action>', llm_response, re.IGNORECASE | re.DOTALL)
        if matches:
            action_map = {
                'NORTH': Directions.NORTH, 'SOUTH': Directions.SOUTH,
                'EAST': Directions.EAST, 'WEST': Directions.WEST,
                'STOP': Directions.STOP
            }
            return action_map.get(matches[-1].strip().upper(), Directions.STOP)
        return Directions.STOP