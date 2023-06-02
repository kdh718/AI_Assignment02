from pickle import NONE
from pacman import GameState, PacmanRules
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

## Example Agent
class ReflexAgent(Agent):

  def Action(self, gameState):
    move_candidate = gameState.getLegalActions() #어디로 움직일지 후보찾기     
    scores = [self.reflex_agent_evaluationFunc(gameState, action) for action in move_candidate]
    bestScore = max(scores)
    Index = [index for index in range(len(scores)) if scores[index] == bestScore]
    get_index = random.choice(Index)

    return move_candidate[get_index]

  def reflex_agent_evaluationFunc(self, currentGameState, action):

    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    return successorGameState.getScore()



def scoreEvalFunc(currentGameState):

  return currentGameState.getScore()

class AdversialSearchAgent(Agent):

  def __init__(self, getFunc ='scoreEvalFunc', depth ='2'):
    self.index = 0
    self.evaluationFunction = util.lookup(getFunc, globals())

    self.depth = int(depth)



class MinimaxAgent(AdversialSearchAgent):
  """
    [문제 01] MiniMaxAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def Action(self, gameState):
    ####################### Write Your Code Here ################################
    '''
    1. 처음 위치에서 갈 수 있는 다음 위치를 찾음 그 다음 고스트가 갈 수 있는 다음 위치를 찾음 -> 반복문말고 재귀함수 사용
    2. depth에 따라서 찾은 걸로 끝나지 않고 다음으로 이동했을 때 다시 이동할 수 있는 경우를 찾음
    3. agent는 항상 max 고스트는 항상 min으로 탐색 
    '''
    move_candidate = gameState.getLegalActions() #어디로 움직일지 후보찾기
    scores = []
    for next_move_str in move_candidate:
        each_state_selected_vaule = self.MiniMax_function(0, 0, gameState.generatePacmanSuccessor(next_move_str))
        scores.append(each_state_selected_vaule)
    bestScore = max(scores)
    Index = [index for index in range(len(scores)) if scores[index] == bestScore]
    get_index = random.choice(Index)
    return move_candidate[get_index]

  def MiniMax_function(self, agentIndex, depth, currentgameState):
    value_list = []; value = 0
    if currentgameState.isLose() or currentgameState.isWin() or depth==self.depth:
      return self.evaluationFunction(currentgameState) #마지막 depth까지 왔을때 이기거나 질때는 해당 값 반환 아니면 평가함수의 함수값 반환
    if agentIndex==0:
      for each_state_next_action in currentgameState.getLegalActions(): #각 스테이트에서 가능한 다음 움직임
        ele = self.MiniMax_function(1, depth,currentgameState.generateSuccessor(0,each_state_next_action))
        value_list.append(ele) #가능한 다음 스테이트일때 고스트의 움직임 확인
      value = max(value_list) #찾은 값 중 가장 큰 값 구함
      return value
    else:
      next_agent=agentIndex+1
      if currentgameState.getNumAgents() - 1==agentIndex: #전체 에이젼트 개수와 현재 확인한 에이전트 개수 비교 -1은 플레이어 에이전트도 세므로 하나 빼고 생각
        next_agent=0 #만약 에이전트를 모두 확인했다면 다시 0번째 플레이어 인덱스부터 확인
        depth += 1
      for each_state_next_action in currentgameState.getLegalActions(agentIndex):
        ele = self.MiniMax_function(next_agent, depth, currentgameState.generateSuccessor(agentIndex,each_state_next_action))
        value_list.append(ele) #각 고스트의 위치 전부 확인 다 확인하면 다시 팩맨 위치 확인
      value = min(value_list) #찾은 값 중 가장 작은 값 구함
      return value

    raise Exception("Not implemented yet")

    ############################################################################




class AlphaBetaAgent(AdversialSearchAgent):
  """
    [문제 02] AlphaBetaAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def Action(self, gameState):
    ####################### Write Your Code Here ################################
    '''
    1. 거의 전부다 minimax랑 같음
    2. 알파 = 음의 무한, 베타 = 양의 무한
    3. MAX를 찾는데 이미 찾아본 값보다 작은 값이 있는 자식 노드를 굳이 확인할 필요없음 -> 그런 노드는 탐색 안하도록 막음
    '''
    move_candidate = gameState.getLegalActions() #어디로 움직일지 후보찾기
    scores = []
    for next_move_str in move_candidate:
        each_state_selected_vaule = self.alphabeta_function(0, 0, gameState.generatePacmanSuccessor(next_move_str), -999999, 999999) #시작 알파베타를 무한대 대신 나올 수 없는 작은 값을 할당
        scores.append(each_state_selected_vaule)
    bestScore = max(scores)
    Index = [index for index in range(len(scores)) if scores[index] == bestScore]
    get_index = random.choice(Index)
    return move_candidate[get_index]

  def alphabeta_function(self, agentIndex, depth, currentgameState, alpha, beta):
    value = 0; candiate_vaule = 0
    if currentgameState.isLose() or currentgameState.isWin() or depth==self.depth:
      return self.evaluationFunction(currentgameState) #마지막 depth까지 왔을때 이기거나 질때는 해당 값 반환 아니면 평가함수의 함수값 반환
    if agentIndex==0: #다음 노드를 바로 확인하지 않고 alpha와 비교해서 결정
      left_bound = -999999 #음의 무한대이지만 팩맨 실행시 출력될 수 없는 낮은 수를 할당함
      for each_state_next_action in currentgameState.getLegalActions(): #각 스테이트에서 가능한 다음 움직임
        candiate_vaule = self.alphabeta_function(1, depth, currentgameState.generateSuccessor(0, each_state_next_action), alpha, beta) #가능한 다음 스테이트일때 고스트의 움직임 확인
        left_bound = max(left_bound, candiate_vaule) #찾은 값 중 가장 큰 값 구함
        value = left_bound
        if value >= beta: break # 베타보다 더 큰 값이 있다면 이전 min 선택에서 절대 선택하지 않을 것이므로 그런 경우는 배제함
        alpha = max(alpha, value) #alpha 업데이트
      return value
    else:
      next_agent=agentIndex+1
      right_bound = 999999 #마찬가지로 양의 무한대 대신 할당 
      if currentgameState.getNumAgents() -1 ==agentIndex: #전체 에이젼트 개수와 현재 확인한 에이전트 개수 비교
        next_agent=0 #만약 에이전트를 모두 확인했다면 다시 0번째 플레이어 인덱스부터 확인
        depth += 1
      for each_state_next_action in currentgameState.getLegalActions(agentIndex): #각 스테이트에서 가능한 다음 움직임
        candiate_vaule = self.alphabeta_function(next_agent, depth, currentgameState.generateSuccessor(agentIndex,each_state_next_action), alpha, beta) #가능한 다음 스테이트일때 고스트의 움직임 확인
        right_bound = min(right_bound, candiate_vaule) #찾은 값 중 가장 큰 값 구함
        value = right_bound
        if value <= alpha: break # 알바보다 더 작은 값이 있다면 이전 max 선택에서 절대 선택하지 않을 것이므로 그런 경우는 배제함
        beta = min(beta, value) #beta 업데이트
      return value
    raise Exception("Not implemented yet")

    ############################################################################



class ExpectimaxAgent(AdversialSearchAgent):
  """
    [문제 03] ExpectimaxAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def Action(self, gameState):
    ####################### Write Your Code Here ################################
    '''
    알파베타랑 비슷한데 max만 구하고 max이전에 확률노드를 구해서 움직임
    확률노드는 기대값으로 구현 기댓값 선택할 확률이 동일할 때 각 확률은 갈 수 있는 다음 스테이트 개수의 역수
    기댓값 = 다음 스테이트의 값 X 그 스테이트를 선택할 확률
    '''
    move_candidate = gameState.getLegalActions() #어디로 움직일지 후보찾기
    scores = []
    for next_move_str in move_candidate:
        each_state_selected_vaule = self.Expectimax_function(0, 0, gameState.generatePacmanSuccessor(next_move_str))
        scores.append(each_state_selected_vaule)
    bestScore = max(scores) #구한 모든 기댓값 중 가장 큰 거 선택
    Index = [index for index in range(len(scores)) if scores[index] == bestScore]
    get_index = random.choice(Index)
    return move_candidate[get_index]

  def Expectimax_function(self, agentIndex, depth, currentgameState):
    Expectaiton = 0
    if currentgameState.isLose() or currentgameState.isWin() or depth==self.depth:
      return self.evaluationFunction(currentgameState)
    if agentIndex==0:
      each_state_next_action = currentgameState.getLegalActions() #각 스테이트에서 가능한 다음 움직임
      number_of_cases = len (each_state_next_action) #바로 다음 하위 노드의 개수 = 각 확률의 분모
      for action in each_state_next_action:
        Expectaiton += self.Expectimax_function(1, depth, currentgameState.generateSuccessor(0, action)) #기댓값은 확률 X 각 노드의 값인데 확률이 모두 같으므로 미리 더하기
      Expectaiton /= number_of_cases #더한 값을 확률로 나누기
      return Expectaiton
    else:
      next_agent=agentIndex+1
      each_state_next_action = currentgameState.getLegalActions(agentIndex) #각 스테이트에서 가능한 다음 움직임
      number_of_cases = len (each_state_next_action)
      if currentgameState.getNumAgents() -1 ==agentIndex: #전체 에이젼트 개수와 현재 확인한 에이전트 개수 비교
        next_agent=0 #만약 에이전트를 모두 확인했다면 다시 0번째 플레이어 인덱스부터 확인
        depth += 1
      for action in each_state_next_action:
        Expectaiton += self.Expectimax_function(next_agent, depth, currentgameState.generateSuccessor(agentIndex, action))
      Expectaiton /= number_of_cases
      return Expectaiton
    raise Exception("Not implemented yet")
    ############################################################################
