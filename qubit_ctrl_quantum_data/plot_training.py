import numpy as np
#from scipy.linalg import expm

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt 

#os.environ["PATH"] += ':/usr/local/texlive/2015/bin/x86_64-darwin' # <-- change to local path
plt.rc('text', usetex=True)
plt.rc('font', **dict(family='serif', size=18) )
plt.tick_params(labelsize=18)
plt.rcParams["figure.figsize"] = [6.5, 5.5] 



# fix seed
seed=0 
np.random.seed(seed)

# fix output array
np.set_printoptions(suppress=True,precision=2) 



############################################################

#save=True
save=False

colors = ['b', 'r', 'g', 'm']

fig, axs = plt.subplots(4, 1, sharex=True)

j=0
for p_emit in [0.0, 0.05]:
    for p_ent in [0.0, 0.1]:

        data = np.load('data/PG-quantum_training-p_emit={0:0.3f}-p_ent={1:0.3f}.npz'.format(p_emit, p_ent))


        episodes=data['episodes'] 
        mean_final_reward=data['mean_final_reward'] 
        std_final_reward=data['std_final_reward'] 
        min_final_reward=data['min_final_reward']
        max_final_reward=data['max_final_reward']
        pseudo_loss=data['pseudo_loss']

        axs[j].hlines([0.5, 0.9, 1.0],episodes[0],episodes[-1], color='k', linestyle='dotted', linewidth=1.0)

        axs[j].plot(episodes, mean_final_reward, '-'+colors[j], label='$p_\\mathrm{emit}='+'{0:0.2f}$,'.format(p_emit)+' $p_\\mathrm{ent}='+'{0:0.2f}$'.format(p_ent) )
        axs[j].fill_between(episodes, 
                         mean_final_reward-0.5*std_final_reward, 
                         np.minimum(1.0, mean_final_reward+0.5*std_final_reward), 
                         color=colors[j], 
                         alpha=0.25)



        # plt.plot(episodes, min_final_reward, '.b' , markersize=2, label='batch minimum' )
        # plt.plot(episodes, max_final_reward, '.r' , markersize=1, label='batch maximum' )

        axs[j].legend(fontsize=14)

        j+=1

plt.xlim([episodes[0],episodes[-1]])

axs[3].set_xlabel('training episode')
axs[1].set_ylabel('mean final reward:  $r_T{=}|\\langle\\psi_\\ast|\\psi(T)\\rangle|^2$')
axs[1].yaxis.set_label_coords(-0.1,-0.0)


#fig.tight_layout()

if save:
	plt.savefig('figs/RL-qa_training-curve.pdf')
	plt.savefig('figs/RL-qa_training-curve.png', dpi=300)
else:
	plt.show()

plt.close()




