from random import random
from Player import Player
from copy import deepcopy
import math


class MiniMaxPlayer(Player):
    MAX_DEPTH = 2
    INFINITY = 9999
    global transpositionTable
    transpositionTable = dict()

    def bfs(self, opponent: Player):
        for player in [self, opponent]:
            destination = (
                self.board.get_white_goal_pieces()
                if player.color == "white"
                else self.board.get_black_goal_pieces()
            )
            visited = {}
            distances = {}
            for row in self.board.map:
                for piece in row:
                    visited[piece] = False
                    distances[piece] = self.INFINITY

            player_piece = self.board.get_piece(*player.get_position())

            queue = []
            queue.append(player_piece)
            visited[player_piece] = True
            distances[player_piece] = 0

            while queue:
                piece = queue.pop(0)

                for i in self.board.get_piece_neighbors(piece):
                    if visited[i] == False:
                        distances[i] = distances[piece] + 1
                        visited[i] = True
                        queue.append(i)

            min_distance = self.INFINITY
            for piece, dist in distances.items():
                if piece in destination:
                    if dist < min_distance:
                        min_distance = dist

            if player == self:
                self_distance = min_distance
            else:
                opponent_distance = min_distance

        return self_distance, opponent_distance

    # def evaluate(self, opponent):
    #     self_distance, opponent_distance = self.bfs(opponent)
    #     total_score = (5 * opponent_distance - self_distance) * (
    #         1 + self.walls_count / 2
    #     )
    #     return total_score

    def evaluate(self, opponent:Player):
        

        

       

       
        evaluate_val = 0
        self_distance, opponent_distance = self.bfs(opponent)

       
        evaluate_val+=opponent_distance
        evaluate_val-=2*self_distance

        

        if not self.is_winner():
            
            evaluate_val += 100/self_distance   ## as it gets closer to goal   self_distance deacreases so evaluate_val increases    ## self is twice more effective than opponent
        


        if not opponent.is_winner():
            evaluate_val -= 50/opponent_distance
        

        if self.is_winner():
            evaluate_val += 100000
        if opponent.is_winner():
               evaluate_val -= 500 

        evaluate_val += (self.walls_count - opponent.walls_count)*10
        evaluate_val -= self.walls_count * 5

        return evaluate_val



       

    def get_best_action(self, opponent):
        best_action_value = -self.INFINITY
        best_action = None
        for action in self.get_legal_actions(opponent):
            self.play(action, is_evaluating=True)
            if self.is_winner():
                self.undo_last_action()
                return action

            action_value = self.evaluate(opponent)
            if action_value > best_action_value:
                best_action_value = action_value
                best_action = action

            self.undo_last_action()

        return best_action


######################################################    minimax 

    def max_value(self,opponent,death):
        
        if(death==self.MAX_DEPTH):
            return None,self.evaluate(opponent)

        value = -self.INFINITY
        returnedAction = None
        for action in self.get_legal_actions(opponent):
            self.play(action, is_evaluating=True)
            returnedAction_temp,value_temp=opponent.min_value(self,death+1)
            if(value_temp>value):
                value = value_temp
                returnedAction=action
            self.undo_last_action()
        return  returnedAction,value



    def min_value(self,opponent,death):
       
        if(death==self.MAX_DEPTH):
            return None,self.evaluate(opponent)

        value = self.INFINITY
        returnedAction = None
        for action in self.get_legal_actions(opponent):
            self.play(action, is_evaluating=True)
            returnedAction_temp,value_temp = opponent.max_value(self,death+1)
            if(value_temp<value):
                value = value_temp
                returnedAction=action
            self.undo_last_action()

        return  returnedAction,value

    def miniMax_decision(self,opponent):
        returnedAction,value=self.max_value(opponent,0)
        print('miniMax_decision ', returnedAction)
        return returnedAction    




######################################################    minimax forward prune 

    
    



    def max_value_forwardPrune(self,opponent,death):
        
        if(death==self.MAX_DEPTH):
            return None,self.evaluate(opponent)

        value = -self.INFINITY
        index=0
        returnedAction = None
        for action in self.get_legal_actions(opponent):
             
          randn=random()  
          if randn<=0.5:
            self.play(action, is_evaluating=True)
            returnedAction_temp,value_temp=opponent.min_value_forwardPrune(self,death+1)
            if(value_temp>value):
                value = value_temp
                returnedAction=action
                if returnedAction==None :
                  continue 
            self.undo_last_action()
        if returnedAction==None:   ## if it is none just traverse none wall moves
            self.max_value(opponent,death)    
        return  returnedAction,value



    def min_value_forwardPrune(self,opponent,death):
       
        index=0
        if(death==self.MAX_DEPTH):
            return None,self.evaluate(opponent)
        
        value = self.INFINITY
        returnedAction = None
        for action in self.get_legal_actions(opponent):
            
            randn=random()
            if randn<=0.5:
                self.play(action, is_evaluating=True)
                returnedAction_temp,value_temp = opponent.max_value_forwardPrune(self,death+1)
                if(value_temp<value):
                    value = value_temp
                    returnedAction=action
                    if returnedAction==None :
                        continue 
                self.undo_last_action()
        if returnedAction==None:
            self.min_value(opponent,death)    
        return  returnedAction,value 

    def miniMax_decision_forwardPrune(self,opponent):
        returnedAction,value=self.max_value_forwardPrune(opponent,0)
        print('miniMax_decision_forwardPrune ', returnedAction)
        return returnedAction



   




   

  
    

#######################################################################   pruningAB


    def miniMax_pruningAB_decision(self,opponent):
        returnedAction,value=self.max_value_pruningAB(opponent,0,-self.INFINITY,+self.INFINITY)
        print('miniMax_pruningAB_decision ', returnedAction)
        return returnedAction    



    def max_value_pruningAB(self,opponent,death,alpha,beta):
        
        if(death==self.MAX_DEPTH):
            return None,self.evaluate(opponent)

        value = -self.INFINITY
        returnedAction = None
        for action in self.get_legal_actions(opponent):
            self.play(action, is_evaluating=True)
            returnedAction_temp,value_temp=opponent.min_value_pruningAB(self,death+1,alpha,beta)
            if(value_temp>value):
                value = value_temp
                returnedAction=action
                alpha=max(alpha,value)
            self.undo_last_action()
            if(value>=beta):
                return  returnedAction,value

        return  returnedAction,value



    def min_value_pruningAB(self,opponent,death,alpha,beta):
        
        if(death==self.MAX_DEPTH):
            return None,self.evaluate(opponent)

        value = self.INFINITY
        returnedAction = None
        for action in self.get_legal_actions(opponent):
            self.play(action, is_evaluating=True)
            returnedAction_temp,value_temp = opponent.max_value_pruningAB(self,death+1,alpha,beta)
            if(value_temp<value):
                value = value_temp
                returnedAction=action
                beta=min(beta,value)
            self.undo_last_action()
            if value<=alpha:
                return  returnedAction,value

        return  returnedAction,value


#######################################     transpositionTable  in pruningAB



    def miniMax_pruningAB_decision_transpositionTable(self,opponent):
        returnedAction,value=self.max_value_pruningAB_transpositionTable(opponent,0,-self.INFINITY,+self.INFINITY)
        print('miniMax_pruningAB_decision ', returnedAction)
        return returnedAction  


    def max_value_pruningAB_transpositionTable(self,opponent,death,alpha,beta):
        # if (self.is_winner):
        #     return  None,self.evaluate(opponent)
        
        if(death==self.MAX_DEPTH):
            return None,self.evaluate(opponent)

        value = -self.INFINITY
        returnedAction = None
        for action in self.get_legal_actions(opponent):
            self.play(action, is_evaluating=True)
            if transpositionTable.get(str(self.board.get_hash())) == None :  # it is new 
                returnedAction_temp,value_temp=opponent.min_value_pruningAB_transpositionTable(self,death+1,alpha,beta)
                transpositionTable[str(self.board.get_hash())]=value_temp
            else :
                value_temp=transpositionTable.get(str(self.board.get_hash()))
            if(value_temp>value):
                value = value_temp
                returnedAction=action
                alpha=max(alpha,value)
            self.undo_last_action()
            if(value>=beta):
                return  returnedAction,value

        return  returnedAction,value



    def min_value_pruningAB_transpositionTable(self,opponent,death,alpha,beta):
        # if(self.is_winner):
        #    None,self.evaluate(opponent)
        
        if(death==self.MAX_DEPTH):
            return None,self.evaluate(opponent)

        value = self.INFINITY
        returnedAction = None
        for action in self.get_legal_actions(opponent):
            self.play(action, is_evaluating=True)
            if transpositionTable.get(str(self.board.get_hash())) == None :  # it is new 
                returnedAction_temp,value_temp = opponent.max_value_pruningAB_transpositionTable(self,death+1,alpha,beta)
                transpositionTable[str(self.board.get_hash())]=value_temp
            else :
                value_temp=transpositionTable.get(str(self.board.get_hash()))
            #returnedAction_temp,value_temp = opponent.max_value_pruningAB(self,death+1,alpha,beta)
            if(value_temp<value):
                value = value_temp
                returnedAction=action
                beta=min(beta,value)
            self.undo_last_action()
            if value<=alpha:
                return  returnedAction,value

        return  returnedAction,value