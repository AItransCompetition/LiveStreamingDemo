import pyparams
import a3c
import tensorflow as tf
S_INFO = 7
S_LEN = 16
A_DIM = 8
ACTOR_LR_RATE = 1e-4
CRITIC_LR_RATE = 1e-3
NN_MODEL = "./submit/results/nn_model_ep_18200.ckpt" # model path settings
class Algorithm:
     def __init__(self):
     # fill your init vars
         self.buffer_size = 0
         
     # Intial 
     def Initial(self):
     # Initail your session or something
         with tf.Session() as sess:
             actor = a3c.ActorNetwork(sess,
                                 state_dim=[S_INFO, S_LEN], action_dim=A_DIM,
                                 learning_rate=ACTOR_LR_RATE)

             critic = a3c.CriticNetwork(sess,
                                 state_dim=[S_INFO, S_LEN],
                                 learning_rate=CRITIC_LR_RATE)
             sess.run(tf.global_variables_initializer())
             saver = tf.train.Saver()  # save neural net parameters

            # restore neural net parameters
             if NN_MODEL is not None:  # NN_MODEL is the path to file
                 saver.restore(sess, NN_MODEL)
                 print("Testing model restored.")

             IntialVars = []
             IntialVars.append(actor)
             IntialVars.append(critic)         
             return IntialVars

     #Define your al
     def run(self, time, S_time_interval, S_send_data_size, S_chunk_len, S_rebuf, S_buffer_size, S_play_time_len,S_end_delay, S_decision_flag, S_buffer_flag,S_cdn_flag, end_of_video, cdn_newest_id,download_id, IntialVars):
    
         # If you choose the marchine learning
         '''actor = IntialVars[0]
         critic = IntialVars[1]
         state = []

         state[0] = ...
         state[1] = ...
         state[2] = ...
         state[3] = ...
         state[4] = ...

         decision = actor.predict(state).argmax()
         bit_rate, target_buffer = decison//4, decison % 4 .....
         return bit_rate, target_buffer'''

         # If you choose BBA
         RESEVOIR = 0.4
         CUSHION =  1
         bit_rate = 1
         if S_buffer_size[-1] < RESEVOIR:
             bit_rate = 0
         elif S_buffer_size[-1] >= RESEVOIR + CUSHION:
             bit_rate = 2
         elif S_buffer_size[-1] >= CUSHION + CUSHION:
             bit_rate = 3
         else:
             bit_rate = 1
         target_buffer = 1
         return bit_rate, target_buffer

         # If you choose other
         #......



     def get_params(self):
     # get your params
        your_params = []
        return your_params
