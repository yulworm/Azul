import os
import datetime
import tools_ai
import tensorflow as tf
import numpy as np
import Azul_game

class ai(object):
    """description of class"""

    def __init__(self,variation='conv_5x5',use_tactics=False,epochs=40):

        self.variation = variation

        self.classification_actions = tools_ai.get_complete_3D_action_list()
        self.model = self.get_model(variation)
        self.use_tactics = use_tactics
        self.epochs = epochs

    def choose_action(self, game):
        # get the probabilities for all the possible actions
        g_actions = game.available_actions(game)

        if self.use_tactics:
            # avoid putting a tile in the penalty
            rows_to_avoid = [Azul_game.penalty_stack_row_idx]

            # avoid filling a row and ending the game
            wall = game.players[game.current_player_idx].wall
            for i in range(0,5):
                if sum(wall[i]) == 4:
                    rows_to_avoid.append(i)

            for row in rows_to_avoid:
                f_actions = list()
                for action in g_actions:
                    if action[2]!=row:
                        f_actions.append(action)

                # if there are still any actions left, then we will use the filtered list
                if len(f_actions) > 0:
                    g_actions = f_actions


        # get the prediction action index
        a_3D_idx = self.choose_action_idx_from_state(self.get_state_for_game(game), g_actions)

        # get the 3D action of the index
        action_3D = self.classification_actions[a_3D_idx]

        # add a 4th dimension to the 3D action
        return tools_ai.convert_3D_action_to_game_action_random(action_3D, g_actions)

    def choose_action_idx_from_state(self, state_a, possible_g_actions):
        # get the predictions
        # the straight forward method is written in the comment below, but for performance I am trying something else
        # this might be another suggestion https://machinelearningmastery.com/use-different-batch-sizes-training-predicting-python-keras/
        # predictions = self.model.predict(np.array([state_a]))
        predictions = self.model(np.array([state_a]))

        # check that our assumption about the classification system used by the model is still true
        if len(predictions[0]) != len(self.classification_actions):
            raise Exception('The model does not have the right number of classifications/actions')

        # of the actions that are possible, which one has the highest probability
        highest_prob = -1
        idx_highest_prob = None
        for idx in tools_ai.get_3D_action_idxs_for_game_actions(possible_g_actions,self.classification_actions):
            if predictions[0][idx] > highest_prob:
                highest_prob = predictions[0][idx]
                idx_highest_prob = idx

        return idx_highest_prob

    def evaluate_model(self, states, a_taken, gas_possible):
        nbr_success = 0
        for i in range(0,len(states)):
            if a_taken[i] == self.choose_action_idx_from_state(states[i], gas_possible[i]):
                nbr_success += 1
            tools_ai.progress(i,len(states)-1)

        return (nbr_success/len(states), len(states))

    def get_name(self):
        return f"nn_{self.variation}"


    def train_from_games(self, games):
        x_train_l = list()
        y_train_l = list()
        possible_g_actions = list()
        for game_sequence in games:
            states, taken_actions, possible_actions = self.get_actions_and_states_from_game_sequence(game_sequence)
            x_train_l.extend(states)
            y_train_l.extend(taken_actions)
            possible_g_actions.extend(possible_actions)

        # we convert the actions, which are now integers, into the categorical form that keras needs
        y_train = np.array(tf.keras.utils.to_categorical(y_train_l, len(self.classification_actions)))

        # Fit model on training data
        self.model.fit(np.array(x_train_l), y_train, epochs=self.epochs)

        #print( self.evaluate_model(x_train_l, y_train_l, possible_g_actions) )

    def get_actions_and_states_from_game_sequence(self, game_sequence):
        """
        returns a tuple containing
        - list of states - the form of the state changes with the variation in use
        - list of actions that were taken - the action are the index of the action in the complete 3D list of actions
        - list of list of actions that were possible
        """
        taken_actions = list()
        states = list()
        possible_actions = list()
        for f_game, g_action, t_game in game_sequence:        
            taken_actions.append( g_action )
            possible_actions.append( f_game.available_actions(f_game) )
            states.append( self.get_state_for_game(f_game) ) 

        return (states, tools_ai.get_3D_action_idxs_for_game_actions(taken_actions, self.classification_actions), possible_actions)
    
    def get_state_for_game(self, game, player_idx=None):
        if player_idx is None:
            player_idx = game.current_player_idx

        if self.variation in ['conv_5x5', 'F5x5']:
            return np.array( game.players[player_idx].get_merged_wall_and_floor() )[:,:,np.newaxis]
        elif self.variation in ['F6x5']:
            return np.array( game.get_current_player_state_without_factory() )[:,:,np.newaxis]
        elif self.variation in ['F6x11']:
            return np.array( game.get_current_player_and_factory() )[:,:,np.newaxis]

    def get_model(self,variation):
        if variation == 'conv_5x5':
            return self.get_model_conv_5x5()
        elif self.variation == 'F5x5':
            return self.get_model_F5x5()
        elif self.variation == 'F6x5':
            return self.get_model_F6x5()
        elif self.variation == 'F6x11':
            return self.get_model_F6x11()

    def get_model_conv_5x5(self):
        """
        Returns a compiled convolutional neural network model. 
        """
        model = tf.keras.models.Sequential()

        model.add( tf.keras.layers.Conv2D(32, (3,3), input_shape=(5,5,1)) )

        model.add( tf.keras.layers.Conv2D(32, (3,3) ) )

        model.add( tf.keras.layers.Flatten() )

        model.add( tf.keras.layers.BatchNormalization() )
        
        model.add( tf.keras.layers.Dense(512,activation="relu") )
    
        model.add( tf.keras.layers.Dropout(0.15) )

        model.add( tf.keras.layers.Dense(256,activation="relu") )

        model.add( tf.keras.layers.Dense(len(self.classification_actions), activation="softmax") )

        model.compile(
            optimizer="adam",
            loss="categorical_crossentropy",
            metrics=["accuracy"])

        return model

    def get_model_F5x5(self):
        """
        Returns a compiled convolutional neural network model. 
        """
        model = tf.keras.models.Sequential()

        model.add( tf.keras.layers.Flatten(input_shape=(5,5)) )

        model.add( tf.keras.layers.Dense(256,activation="relu") )
    
        #model.add( tf.keras.layers.Dropout(0.15) )

        model.add( tf.keras.layers.Dense(256,activation="relu") )

        model.add( tf.keras.layers.Dense(len(self.classification_actions), activation="softmax") )

        model.compile(
            optimizer="adam",
            loss="categorical_crossentropy",
            metrics=["accuracy"])

        return model

    def get_model_F6x5(self):
        model = tf.keras.models.Sequential()

        model.add( tf.keras.layers.Flatten(input_shape=(6,5)) )

        model.add( tf.keras.layers.Dense(256,activation="relu") )
    
        #model.add( tf.keras.layers.Dropout(0.15) )

        model.add( tf.keras.layers.Dense(256,activation="relu") )

        model.add( tf.keras.layers.Dense(len(self.classification_actions), activation="softmax") )

        model.compile(
            optimizer="adam",
            loss="categorical_crossentropy",
            metrics=["accuracy"])

        return model

    def get_model_F6x11(self):
        model = tf.keras.models.Sequential()

        model.add( tf.keras.layers.Flatten(input_shape=(6,11)) )

        model.add( tf.keras.layers.Dense(256,activation="relu") )
    
        #model.add( tf.keras.layers.Dropout(0.15) )

        model.add( tf.keras.layers.Dense(256,activation="relu") )

        model.add( tf.keras.layers.Dense(len(self.classification_actions), activation="softmax") )

        model.compile(
            optimizer="adam",
            loss="categorical_crossentropy",
            metrics=["accuracy"])

        return model

    def save_model(self, folder):
        filename = f'{self.get_name()}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.h5'

        self.model.save(os.path.join(folder,filename))

        return filename
        #with open(os.path.join(folder,filename), 'wb') as model_file:
        #
        #  pickle.dump(ai, model_file)
        #  print(os.path.abspath(model_file.name))

        #return filename

    def load_model(self, folder, filename):
        self.model = tf.keras.models.load_model(os.path.join(folder,filename))