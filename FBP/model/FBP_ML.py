import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.metrics import accuracy_score
from graphviz import Digraph


def get_train_set(path):
    xgb.DMatrix(path)


def eryuan():
    train_set = xgb.DMatrix('data_201701_201906_libsvm')
    test_set = xgb.DMatrix('target_libsvm')
    params = {
        'objective': 'binary:logistic',
        'booster': 'gbtree',
        # 'objective': 'multi:softmax',  # 多分类的问题
        # 'num_class': 3,               # 类别数，与 multisoftmax 并用
        'gamma': 0.1,                  # 用于控制是否后剪枝的参数,越大越保守，一般0.1、0.2这样子。
        'max_depth': 5,               # 构建树的深度，越大越容易过拟合
        'lambda': 2,                   # 控制模型复杂度的权重值的L2正则化项参数，参数越大，模型越不容易过拟合。
        'subsample': 0.7,              # 随机采样训练样本
        'colsample_bytree': 0.7,       # 生成树时进行的列采样
        'min_child_weight': 3,
        'silent': 1,                   # 设置成1则没有运行信息输出，最好是设置为0.
        'eta': 0.007,                  # 如同学习率
        'seed': 1000,
        'nthread': 4,                  # cpu 线程数
        # 'eval_metric': 'auc'
    }
    num_round = 2
    bst = xgb.train(params, train_set, num_round)
    train_preds = bst.predict(train_set)

    train_predictions = [round(value) for value in train_preds]
    y_train = train_set.get_label()
    train_accuracy = accuracy_score(y_train, train_predictions)

    print("Test Accuracy:%.2f%%"%(train_accuracy * 100.0))

    train_preds = bst.predict(test_set)
    print(train_preds)
    train_predictions = [round(value) for value in train_preds]
    print(train_predictions)
    y_train = test_set.get_label()
    train_accuracy = accuracy_score(y_train, train_predictions)

    print("Test Accuracy:%.2f%%" % (train_accuracy * 100.0))
    xgb.plot_tree(bst, num_trees=0, rankdir='LR')
    xgb.plot_importance(bst)
    plt.show()


    # print ('AUC: %.4f' % metrics.roc_auc_score(test_y,ypred))
    # print ('ACC: %.4f' % metrics.accuracy_score(test_y,y_pred))
    # print ('Recall: %.4f' % metrics.recall_score(test_y,y_pred))
    # print ('F1-score: %.4f' %metrics.f1_score(test_y,y_pred))
    # print ('Precesion: %.4f' %metrics.precision_score(test_y,y_pred))
    # print(metrics.confusion_matrix(test_y,y_pred))

def sanyuan():
    train_set = xgb.DMatrix('data_201701_201906_libsvm')
    test_set = xgb.DMatrix('target_libsvm')
    params = {
        # 'objective': 'binary:logistic',
        'booster': 'gbtree',
        'objective': 'multi:softmax',  # 多分类的问题
        'num_class': 3,               # 类别数，与 multisoftmax 并用
        'gamma': 0.1,                  # 用于控制是否后剪枝的参数,越大越保守，一般0.1、0.2这样子。
        'max_depth': 5,               # 构建树的深度，越大越容易过拟合
        'lambda': 2,                   # 控制模型复杂度的权重值的L2正则化项参数，参数越大，模型越不容易过拟合。
        'subsample': 0.7,              # 随机采样训练样本
        'colsample_bytree': 0.7,       # 生成树时进行的列采样
        'min_child_weight': 3,
        'silent': 1,                   # 设置成1则没有运行信息输出，最好是设置为0.
        'eta': 0.007,                  # 如同学习率
        'seed': 1000,
        'nthread': 4,                  # cpu 线程数
        # 'eval_metric': 'auc'
    }
    num_round = 2
    bst = xgb.train(params, train_set, num_round)
    train_preds = bst.predict(train_set)

    train_predictions = [round(value) for value in train_preds]
    y_train = train_set.get_label()
    train_accuracy = accuracy_score(y_train, train_predictions)

    print("Test Accuracy:%.2f%%"%(train_accuracy * 100.0))

    train_preds = bst.predict(test_set)
    print(train_preds)
    train_predictions = [round(value) for value in train_preds]
    print(train_predictions[19])
    y_train = test_set.get_label()
    train_accuracy = accuracy_score(y_train, train_predictions)

    print("Test Accuracy:%.2f%%" % (train_accuracy * 100.0))
    xgb.plot_tree(bst, num_trees=0, rankdir='LR')
    xgb.plot_importance(bst)
    plt.show()


    # print ('AUC: %.4f' % metrics.roc_auc_score(test_y,ypred))
    # print ('ACC: %.4f' % metrics.accuracy_score(test_y,y_pred))
    # print ('Recall: %.4f' % metrics.recall_score(test_y,y_pred))
    # print ('F1-score: %.4f' %metrics.f1_score(test_y,y_pred))
    # print ('Precesion: %.4f' %metrics.precision_score(test_y,y_pred))
    # print(metrics.confusion_matrix(test_y,y_pred))

if __name__ == '__main__':
    eryuan()
    # sanyuan()
