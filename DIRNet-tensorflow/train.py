import tensorflow as tf
from models import DIRNet,ResNet
from config import get_config
from data import DIRNetDatahandler
import numpy as np
from ops import mkdir


def main():
    tf.reset_default_graph()
    train_ResNet()
    # sess_config = tf.ConfigProto()
    # sess_config.gpu_options.allow_growth = True
    # sess = tf.Session(config=sess_config)
    # config = get_config(is_train=True)
    # mkdir(config.tmp_dir)
    # mkdir(config.ckpt_dir)
    #
    # reg = DIRNet(sess, config, "DIRNet", is_train=True)
    # # reg.restore(config.ckpt_dir)
    # dh = DIRNetDatahandler( config=config)
    #
    # amnt_pics = np.shape(dh.d_data)[0]
    # for epoch in range(13):
    #     loss_sum = 0
    #     acc = 0
    #     for i in range(amnt_pics):
    #         batch_x, batch_y, batch_labels = dh.get_pair_by_idx(i)
    #         # loss = reg.fit((1, batch_x[0], batch_x[1], batch_x[2]),
    #         #                (1, batch_y[0], batch_y[1], batch_y[2]))
    #         loss, prediction = reg.fit(batch_x, batch_y, batch_labels)
    #         loss_sum += loss
    #         prediction = int(prediction[0])
    #         truth = int(batch_labels[0])
    #         # print("pred {} truth {}".format(prediction, truth))
    #         if prediction == truth:
    #             acc += 1
    #     print("epoch {0}: Loss: {1:.4f} Acc: {2:.4f}".format(epoch, loss_sum / amnt_pics, acc / amnt_pics))
    #     # loss_sum = 0
    #     # acc = 0
    #     # amnt_eva = np.shape(dh.d_data_eval)[0]
    #     # for i in range(amnt_eva):
    #     #     batch_x, batch_y, batch_labels = dh.get_eval_pair_by_idx(i)
    #     #     # loss = reg.fit((1, batch_x[0], batch_x[1], batch_x[2]),
    #     #     #                (1, batch_y[0], batch_y[1], batch_y[2]))
    #     #     loss, prediction = reg.deploy_with_labels(batch_x, batch_y, batch_labels)
    #     #     loss_sum += loss
    #     #     prediction = int(prediction[0])
    #     #     truth = int(batch_labels[0])
    #     #     # print("pred {} truth {}".format(prediction, truth))
    #     #     if prediction == truth:
    #     #         acc += 1
    #     # print("evalu {0}: Loss: {1:.4f} Acc: {2:.4f}".format(epoch, loss_sum / amnt_eva, acc / amnt_eva))
    #
    #
    #     if (epoch + 1) % 5 == 0:
    #     # if (epoch+1) % config.checkpoint_distance == 0:
    #     # reg.deploy(config.tmp_dir, batch_x, batch_y)
    #         print('saving model...')
    #         reg.save(config.ckpt_dir)
    #
    #
    # amnt_eva = np.shape(dh.d_data_eval)[0]
    # acc = 0
    # for i in range(amnt_eva):
    #     batch_x, batch_y, batch_labels = dh.get_eval_pair_by_idx(i)
    #     prev_x = batch_x
    #     # loss = reg.fit((1, batch_x[0], batch_x[1], batch_x[2]),
    #     #                (1, batch_y[0], batch_y[1], batch_y[2]))
    #     prediction = reg.deploy_with_labels(batch_x, batch_y, batch_labels)
    #     truth = int(batch_labels[0])
    #     # print("pred {} truth {}".format(prediction, truth))
    #     if prediction == truth:
    #         acc += 1
    # print("Acc: {0:.4f}".format(acc / amnt_eva))
    # reg.calc_rmse_all(y=dh.d_data_eval, x=dh.s_data_eval,dir_path='', save_images=False)
    # # for i in range(config.iteration):
    # #     # create new random batch
    # #     batch_x, batch_y, batch_labels = dh.sample_pair(config.batch_size)
    # #
    # #     # run sess => minimize loss
    # #     loss = reg.fit(batch_x, batch_y,batch_labels)
    # #
    # #     print("iter {:>6d} : {}".format(i + 1, loss))
    # #
    # #     if (i + 1) % config.checkpoint_distance == 0:
    # #         # reg.deploy(config.tmp_dir, batch_x, batch_y)
    # #         reg.save(config.ckpt_dir)

def train_ResNet():
    sess_config = tf.ConfigProto()
    sess_config.gpu_options.allow_growth = True
    sess = tf.Session(config=sess_config)
    config = get_config(is_train=True)
    mkdir(config.tmp_dir)
    mkdir(config.ckpt_dir)

    reg = ResNet(sess, config, "DIRNet", is_train=True)
    # reg.restore(config.ckpt_dir)
    dh = DIRNetDatahandler(config=config)

    amnt_pics = np.shape(dh.d_data)[0]
    for epoch in range(5):
        loss_sum = 0
        acc = 0
        for i in range(amnt_pics-1):
            batch_x, batch_y, batch_labels = dh.get_pair_by_idx(i)


            # loss = reg.fit((1, batch_x[0], batch_x[1], batch_x[2]),
            #                (1, batch_y[0], batch_y[1], batch_y[2]))
            loss, prediction = reg.fit(batch_x, batch_y, batch_labels)
            loss2, prediction2 = reg.fit(batch_y, batch_x, batch_labels)
            loss_sum += (loss+loss2)/2
            prediction = int(prediction[0])
            truth = int(batch_labels[0])
            # print("pred {} truth {}".format(prediction, truth))
            if prediction == truth:
                acc += 1
            if prediction2[0] == truth:
                acc += 1
        print("epoch {0}: Loss: {1:.4f} Acc: {2:.4f}".format(epoch, loss_sum / (amnt_pics*2), acc / (amnt_pics*2)))

        if (epoch + 1) % 5 == 0:
            # if (epoch+1) % config.checkpoint_distance == 0:
            # reg.deploy(config.tmp_dir, batch_x, batch_y)
            print('saving model...')
            # reg.save(config.ckpt_dir)

    amnt_pics = np.shape(dh.d_data)[0]
    acc = 0
    prev_x = np.empty(shape=(1, 222, 247))
    amnt_eva = np.shape(dh.d_data_eval)[0]
    for i in range(amnt_eva):
        batch_x, batch_y, batch_labels = dh.get_eval_pair_by_idx(i)
        if np.array_equal(prev_x, batch_x):
            print('weird')
        prev_x = batch_x
        # loss = reg.fit((1, batch_x[0], batch_x[1], batch_x[2]),
        #                (1, batch_y[0], batch_y[1], batch_y[2]))
        prediction = reg.deploy_with_labels(batch_x, batch_y, batch_labels)
        print(prediction, "::", batch_labels[0])
        truth = int(batch_labels[0])
        # print("pred {} truth {}".format(prediction, truth))
        if prediction == truth:
            acc += 1
    print("Acc: {0:.4f}".format(acc / amnt_eva))
if __name__ == "__main__":
    main()
