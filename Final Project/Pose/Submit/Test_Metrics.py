import numpy as np
from numpy.linalg import norm
from utils import *
def epose(q_pred, q_real, r_pred, r_real):
    rot_err = []
    tr_err = []
    # norm 1 to find magnitude
    for l in range(len(r_pred)):
        q_err = 2*(np.arccos(abs((q_pred[l] @ np.transpose(q_real[l])))))
        rot_err.append(np.array(q_err))
        r_err = abs(norm(r_real[l]-r_pred[l], 2) / norm(r_real[l], 2))
        tr_err.append(np.array(r_err))

    return rot_err, tr_err

def evaluate(model, dataloader, device):
    model.eval()
    q_batch = []
    r_batch = []
    E_q= [] #orientation error
    E_r = [] #translation error
    E_p = 0.0 #pose error
    for i, data in enumerate(dataloader, 0):
        with torch.set_grad_enabled(False):
            inputs, labels = data[0], data[1].float()
            outputs = model(inputs, 'test')
                       
            predicted = outputs.data

            q_batch=(outputs[:, :4].cpu().numpy())
            r_batch=(outputs[:, -3:].cpu().numpy())
            if i<2 :
                plt.figure()
                viz_pose(inputs.numpy()[i].transpose(1,2,0), q_batch[i], r_batch[i])
                plt.title('Predicted Pose= '+ str(predicted.cpu().numpy()[i]) + '\n Actual Pose= ' + str(labels.cpu().numpy()[i]))
                plt.savefig("predictedPose.png") 
                plt.show()
            rot, tr= epose(q_batch, labels[:, :4].cpu().numpy(), r_batch, labels[:, -3:].cpu().numpy())
            E_q.append(rot)
            E_r.append(tr)

    E_q= np.concatenate(E_q,  axis=None)
    E_r= np.concatenate(E_r,  axis=None)

    # Test
    #-----------Pose Error-----------#
    print(f'Best orientation error:{np.min(E_q)}')
    print(f'Best translarion error: {np.min(E_r)}')
    E_p = np.sum([E_q, E_r], dtype=np.float32)/len(dataloader.dataset)
    print(f'The Pose error is: {E_p}')
    
    #----------- METRICS -------------#

    return
##-----------------------------------------------------------------------------------------------------------##
