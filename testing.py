import random
import math
def Action(self, gameState):

    # Action 함수는 루트 노드의 역할

    # 1. 현재 Pacman이 할 수 있는 모든 행동을 찾는다.
    # 2. 작성한 minimax 함수에 이를 대입하여 탐색한다.
    # 3. Max value를 선택하여 행동한다.

    move = gameState.getLegalActions() # default agent is pacman
    utility = [self.MiniMax(0, 0, gameState.generatePacmanSuccessor(action)) for action in move] # call minimax from root node
    max_value = max(utility)
    Index=[index for index in range(len(utility)) if utility[index]==max_value]
    get_index=random.choice(Index)

    return move[get_index]
def MiniMax(self,agent, depth, gameState):
    # Terminal Test
    if gameState.isLose() or gameState.isWin() or depth==self.depth:
      return self.evaluationFunction(gameState)
    # Pacman
    # select max value
    if agent==0:
      return max(self.MiniMax(1, depth,gameState.generateSuccessor(0,action)) for action in gameState.getLegalActions())
    # Ghost
    # select min value
    else:
      next_agent=agent+1
      if gameState.getNumAgents()==agent+1:
        next_agent=0
        # one cycle end then increase depth
        depth+=1
      return min(self.MiniMax(next_agent, depth, gameState.generateSuccessor(agent,action)) for action in gameState.getLegalActions(agent))

def AlphaBeta(self, agent, depth, gameState, alpha, beta):
    # Terminal Test
    if gameState.isLose() or gameState.isWin() or depth==self.depth:
      return self.evaluationFunction(gameState)
    # pacman
    if agent==0:
      pacman_actions=gameState.getLegalActions()
      tmp=-math.inf
      for action in pacman_actions:
        tmp=max(tmp, self.AlphaBeta(1,depth,gameState.generatePacmanSuccessor(action), alpha,beta))
        alpha=max(alpha,tmp)
        if tmp>=beta:
          break # pruning the redundant branch
      return tmp
    # ghost
    else:
      ghost_actions=gameState.getLegalActions(agent)
      tmp=math.inf
      next_agent=agent+1
      if gameState.getNumAgents()==agent+1:
        next_agent=0
        # end of one cycle
        depth+=1
      for action in ghost_actions:
        tmp=min(tmp, self.AlphaBeta(next_agent,depth,gameState.generateSuccessor(agent,action), alpha,beta))
        beta=min(beta,tmp)
        if tmp<=alpha:
          break # pruning the redundant branch
      return tmp
def Expectimax(self, agent, depth, gameState):
    #Terminal Test
    if gameState.isLose() or gameState.isWin() or depth==self.depth:
      return self.evaluationFunction(gameState)

    # max와 min 모두 chance 노드로 부터 선택을 해야 한다.
    # chance node는 (probabilty*value)의 총 합
    # probability는 모두 동일한 것으로 계산하므로 평균을 구하는 것과 같다.

    # pacman
    if agent==0:
      pacman_actions=gameState.getLegalActions()
      actions_num=len(pacman_actions)
      return sum(self.Expectimax(1,depth, gameState.generatePacmanSuccessor(action)) for action in pacman_actions)/(actions_num)
    # Ghost
    else:
      next_agent=agent+1
      ghost_actions=gameState.getLegalActions(agent)
      actions_num=len(ghost_actions)
      if gameState.getNumAgents()==agent+1: # end of one cycle
        next_agent=0
        depth+=1
      return sum(self.Expectimax(next_agent, depth, gameState.generateSuccessor(agent, action))for action in ghost_actions)/(actions_num)