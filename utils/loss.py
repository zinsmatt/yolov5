# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Loss functions
"""

import torch
import torch.nn as nn

from utils.metrics import bbox_iou, ellipses_sampling_distance, wasserstein_distance, bhattacharyya_distance, ellipses_iou_no_grad_list
from utils.torch_utils import is_parallel
from math import pi
import numpy as np


def smooth_BCE(eps=0.1):  # https://github.com/ultralytics/yolov3/issues/238#issuecomment-598028441
    # return positive, negative label smoothing BCE targets
    return 1.0 - 0.5 * eps, 0.5 * eps


class BCEBlurWithLogitsLoss(nn.Module):
    # BCEwithLogitLoss() with reduced missing label effects.
    def __init__(self, alpha=0.05):
        super(BCEBlurWithLogitsLoss, self).__init__()
        self.loss_fcn = nn.BCEWithLogitsLoss(reduction='none')  # must be nn.BCEWithLogitsLoss()
        self.alpha = alpha

    def forward(self, pred, true):
        loss = self.loss_fcn(pred, true)
        pred = torch.sigmoid(pred)  # prob from logits
        dx = pred - true  # reduce only missing label effects
        # dx = (pred - true).abs()  # reduce missing label and false label effects
        alpha_factor = 1 - torch.exp((dx - 1) / (self.alpha + 1e-4))
        loss *= alpha_factor
        return loss.mean()


class FocalLoss(nn.Module):
    # Wraps focal loss around existing loss_fcn(), i.e. criteria = FocalLoss(nn.BCEWithLogitsLoss(), gamma=1.5)
    def __init__(self, loss_fcn, gamma=1.5, alpha=0.25):
        super(FocalLoss, self).__init__()
        self.loss_fcn = loss_fcn  # must be nn.BCEWithLogitsLoss()
        self.gamma = gamma
        self.alpha = alpha
        self.reduction = loss_fcn.reduction
        self.loss_fcn.reduction = 'none'  # required to apply FL to each element

    def forward(self, pred, true):
        loss = self.loss_fcn(pred, true)
        # p_t = torch.exp(-loss)
        # loss *= self.alpha * (1.000001 - p_t) ** self.gamma  # non-zero power for gradient stability

        # TF implementation https://github.com/tensorflow/addons/blob/v0.7.1/tensorflow_addons/losses/focal_loss.py
        pred_prob = torch.sigmoid(pred)  # prob from logits
        p_t = true * pred_prob + (1 - true) * (1 - pred_prob)
        alpha_factor = true * self.alpha + (1 - true) * (1 - self.alpha)
        modulating_factor = (1.0 - p_t) ** self.gamma
        loss *= alpha_factor * modulating_factor

        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        else:  # 'none'
            return loss


class QFocalLoss(nn.Module):
    # Wraps Quality focal loss around existing loss_fcn(), i.e. criteria = FocalLoss(nn.BCEWithLogitsLoss(), gamma=1.5)
    def __init__(self, loss_fcn, gamma=1.5, alpha=0.25):
        super(QFocalLoss, self).__init__()
        self.loss_fcn = loss_fcn  # must be nn.BCEWithLogitsLoss()
        self.gamma = gamma
        self.alpha = alpha
        self.reduction = loss_fcn.reduction
        self.loss_fcn.reduction = 'none'  # required to apply FL to each element

    def forward(self, pred, true):
        loss = self.loss_fcn(pred, true)

        pred_prob = torch.sigmoid(pred)  # prob from logits
        alpha_factor = true * self.alpha + (1 - true) * (1 - self.alpha)
        modulating_factor = torch.abs(true - pred_prob) ** self.gamma
        loss *= alpha_factor * modulating_factor

        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        else:  # 'none'
            return loss


class ComputeLoss:
    # Compute losses
    def __init__(self, model, autobalance=False):
        self.sort_obj_iou = False
        device = next(model.parameters()).device  # get model device
        h = model.hyp  # hyperparameters

        # Define criteria
        BCEcls = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([h['cls_pw']], device=device))
        BCEobj = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([h['obj_pw']], device=device))

        # Class label smoothing https://arxiv.org/pdf/1902.04103.pdf eqn 3
        self.cp, self.cn = smooth_BCE(eps=h.get('label_smoothing', 0.0))  # positive, negative BCE targets

        # Focal loss
        g = h['fl_gamma']  # focal loss gamma
        if g > 0:
            BCEcls, BCEobj = FocalLoss(BCEcls, g), FocalLoss(BCEobj, g)

        det = model.module.model[-1] if is_parallel(model) else model.model[-1]  # Detect() module
        self.balance = {3: [4.0, 1.0, 0.4]}.get(det.nl, [4.0, 1.0, 0.25, 0.06, .02])  # P3-P7
        self.ssi = list(det.stride).index(16) if autobalance else 0  # stride 16 index
        self.BCEcls, self.BCEobj, self.gr, self.hyp, self.autobalance = BCEcls, BCEobj, 1.0, h, autobalance
        for k in 'na', 'nc', 'nl', 'anchors':
            setattr(self, k, getattr(det, k))
        self.DEBUG = []

    def __call__(self, p, targets, epoch=-1):  # predictions, targets, model
        # print("NC = ", self.nc)
        # print("predictions size = ", len(p))
        # print(p[0].shape, p[1].shape, p[2].shape)
        # print(targets[:2, :])

        device = targets.device
        lcls, lbox, lobj = torch.zeros(1, device=device), torch.zeros(1, device=device), torch.zeros(1, device=device)
        tcls, tbox, tangle, indices, anchors = self.build_targets(p, targets)  # targets
        # print(tcls[0].shape)
        # print(tbox[0].shape)
        # print(tangle[0].shape)
        # print(len(indices), len(indices[0]), indices[0][0].shape)
        # print(anchors[0].shape)
        # if epoch != -1:
        #     print("===========================>", epoch)
        # Losses
        for i, pi in enumerate(p):  # layer index, layer predictions
            b, a, gj, gi = indices[i]  # image, anchor, gridy, gridx
            # print("image: ", b)
            # print("anchor: ", a)
            # print("grid xy: ", gj, gi)
            tobj = torch.zeros_like(pi[..., 0], device=device)  # target obj

            n = b.shape[0]  # number of targets
            if n:
                ps = pi[b, a, gj, gi]  # prediction subset corresponding to targets

                # Regression
                # no need to add grid center or multiply by the stride because it is the same for the predicted and the gt boxes => no influence
                # the dimensions are multiplied by the anchors 
                pxy = ps[:, :2].sigmoid() * 2. - 0.5
                pwh = (ps[:, 2:4].sigmoid() * 2) ** 2 * anchors[i]

                # pa = ps[:, 4:5].sigmoid() * 2 - 1.0#.tanh()
                pa = ps[:, 4:5].tanh()
                pbox = torch.cat((pxy, pwh), 1)  # predicted box
                # print("pbox = ", pbox.shape)
                # print("tbox[i] = ", tbox[i].shape)


                iou = bbox_iou(pbox.T, tbox[i], x1y1x2y2=False, CIoU=True)  # iou(prediction, target)

                # iou = ellipses_iou_no_grad_list(torch.cat((pbox[:, 2:4]/2, torch.arcsin(pa), pbox[:, :2]), 1).detach().cpu().numpy(),
                #                                 torch.cat((tbox[i][:, 2:4]/2, tangle[i], tbox[i][:, :2]), 1).detach().cpu().numpy()).to(device)
                # print("iou: ", iou.shape)

                # print(pa[:10, :])
                # print(pbox.grad)

                # l_ell = ellipses_sampling_distance(torch.cat((pbox, pa), 1), torch.cat((tbox[i], torch.sin(tangle[i])), 1))
                # l_ell = wasserstein_distance(torch.cat((pbox, pa), 1), torch.cat((tbox[i], torch.sin(tangle[i])), 1))
                # l_ell = bhattacharyya_distance(torch.cat((pbox, pa), 1), torch.cat((tbox[i], torch.sin(tangle[i])), 1))
                # lbox += torch.mean(torch.sum((pbox - tbox[i])**2, dim=1))
                
                # l_ell = ellipses_sampling_distance(pbox, tbox[i])

                # l_ell = ellipses_sampling_distance(pbox, tbox[i])
                # l_ell = ellipses_sampling_distance(pbox, tbox[i])
                # print("=============> l_ell = ", l_ell)
                # print("pbox shape:: ", pbox.shape)
                # print("tbox shape::: ", tbox[i].shape)
                # aa = torch.mean((pbox - tbox[i])**2)
                # bb = torch.mean((2*ps[:, 4].tanh() - torch.sin(tangle[i]))**2)
                # print(tangle[i])
                # lbox += aa + bb * 4
                # lbox += torch.mean((pbox - tbox[i])**2) + torch.mean((ps[:, 4].tanh())**2)

                lbox += (1.0 - iou).mean()  # iou loss
                # lbox += torch.mean(torch.abs((pbox-tbox[i])))
                # pa.register_hook(lambda grad: print(grad))

                # if epoch >= 10:
                #     lbox += l_ell*0.1 #0.0001

                lbox += torch.mean((torch.sin(tangle[i]) - pa)**2)

                # lbox += l_ell * 0.0001
                # lbox += l_ell * 0.1
                # lbox += l_ell * 0.025  # 0.025
                # lbox += l_ell
                # lbox += l_ell * 0.0125  # 0.025
                # lbox += l_ell * 0.1# * 0.025
                # pbox.register_hook(lambda grad: print(grad))

                # Objectness
                score_iou = iou.detach().clamp(0).type(tobj.dtype)
                if self.sort_obj_iou:
                    sort_id = torch.argsort(score_iou)
                    b, a, gj, gi, score_iou = b[sort_id], a[sort_id], gj[sort_id], gi[sort_id], score_iou[sort_id]
                tobj[b, a, gj, gi] = (1.0 - self.gr) + self.gr * score_iou  # iou ratio ([mz] used as gt label for conf)

                # Classification
                if self.nc > 1:  # cls loss (only if multiple classes)
                    t = torch.full_like(ps[:, 6:], self.cn, device=device)  # targets ([mz] logits with self.cn/self.cp for negative/positive)
                    t[range(n), tcls[i]] = self.cp
                    lcls += self.BCEcls(ps[:, 6:], t)  # BCE

                # Append targets to text file
                # with open('targets.txt', 'a') as file:
                #     [file.write('%11.5g ' * 4 % tuple(x) + '\n') for x in torch.cat((txy[i], twh[i]), 1)]

            obji = self.BCEobj(pi[..., 5], tobj) # loss for confidence between the predicted conf pi and the iou ratio tobj
            lobj += obji * self.balance[i]  # obj loss
            if self.autobalance:
                self.balance[i] = self.balance[i] * 0.9999 + 0.0001 / obji.detach().item()

        if self.autobalance:
            self.balance = [x / self.balance[self.ssi] for x in self.balance]
        # print("lbox: ", lbox, self.hyp['box'])
        # print("lobj: ", lobj, self.hyp['obj'])
        # print("lcls: ", lcls, self.hyp['cls'])
        lbox *= self.hyp['box']
        lobj *= self.hyp['obj']
        lcls *= self.hyp['cls']
        # print(lobj)
        # self.DEBUG.append(lobj.cpu().detach().numpy())

        bs = tobj.shape[0]  # batch size

        return (lbox + lobj + lcls) * bs, torch.cat((lbox, lobj, lcls)).detach()

    def build_targets(self, p, targets):
        # print("build targets = ", targets.shape)
        # print("targets = ", targets.shape)
        # print("targets[6] = ", targets[:, 6])
        # Build targets for compute_loss(), input targets(image,class,x,y,w,h)
        na, nt = self.na, targets.shape[0]  # number of anchors, targets
        # print("nb anchors = ", na)
        # print("nb targets = ", nt)
        tcls, tbox, tangle, indices, anch = [], [], [], [], []
        gain = torch.ones(8, device=targets.device)  # normalized to gridspace gain
        ai = torch.arange(na, device=targets.device).float().view(na, 1).repeat(1, nt)  # same as .repeat_interleave(nt)

        targets = torch.cat((targets.repeat(na, 1, 1), ai[:, :, None]), 2)  # append anchor indices
        # print("AFTER SHAPE = ", targets.shape)
        # print(targets.shape)
        # print(targets[0, :, 0])
        # print(targets.shape)
        # print(targets[0, :8, :])

        g = 0.5  # bias
        off = torch.tensor([[0, 0],
                            [1, 0], [0, 1], [-1, 0], [0, -1],  # j,k,l,m
                            # [1, 1], [1, -1], [-1, 1], [-1, -1],  # jk,jm,lk,lm
                            ], device=targets.device).float() * g  # offsets

        for i in range(self.nl):
            anchors = self.anchors[i]
            # [mz] multiply by the size of the grid in x and y of layer 'i'
            gain[2:6] = torch.tensor(p[i].shape)[[3, 2, 3, 2]]  # xyxy gain

            # Match targets to anchors
            t = targets * gain # [mz] element-wise multiplication (seems to be just a scale factor applied on the coordinates)
            # print("anchors = ", anchors)
            if nt:

                # [mz] First filtering
                # print("t = ", t[:, :, 4:6])
                # print("anchors = ", anchors[:, None])
                # print("t = ", t[:, :, 4:6].shape)
                # print("anchors = ", anchors[:, None].shape)

                # Matches
                r = t[:, :, 4:6] / anchors[:, None]  # wh ratio
                # print("r = ", r.shape)
                # print("anchors[:, None] = ", anchors[:, None])
                # print(t.shape)
                # print(anchors.shape)
                # print(anchors[:, None].shape)
                # print("r shaoe = ", r.shape)
                # print(r[0, :4, :])

                #print("r = ", r)
                j = torch.max(r, 1. / r).max(2)[0] < self.hyp['anchor_t']  # compare
                # j = wh_iou(anchors, t[:, 4:6]) > model.hyp['iou_t']  # iou(3,n)=wh_iou(anchors(3,2), gwh(n,2))
                t = t[j]  # filter

                # [mz] Second filtering
                # Offsets
                gxy = t[:, 2:4]  # grid xy
                gxi = gain[[2, 3]] - gxy  # inverse
                j, k = ((gxy % 1. < g) & (gxy > 1.)).T
                l, m = ((gxi % 1. < g) & (gxi > 1.)).T
                j = torch.stack((torch.ones_like(j), j, k, l, m))
                t = t.repeat((5, 1, 1))
                t = t[j]

                offsets = (torch.zeros_like(gxy)[None] + off[:, None])[j]
            else:
                t = targets[0]
                offsets = 0

            # Define
            b, c = t[:, :2].long().T  # image, class
            gxy = t[:, 2:4]  # grid xy
            gwh = t[:, 4:6]  # grid wh
            # print(gwh[:10, :])
            gij = (gxy - offsets).long()
            gi, gj = gij.T  # grid xy indices

            # filter bad angles
            sup = torch.where(t[:, 6] > pi/2)[0]
            inf = torch.where(t[:, 6] < -pi/2)[0]
            t[sup, 6] -= pi
            t[inf, 6] += pi


            # Append
            a = t[:, 7].long()  # anchor indices
            indices.append((b, a, gj.clamp_(0, gain[3] - 1), gi.clamp_(0, gain[2] - 1)))  # image, anchor, grid indices
            tbox.append(torch.cat((gxy - gij, gwh), 1))  # box
            anch.append(anchors[a])  # anchors
            tcls.append(c)  # class
            tangle.append(t[:, 6].reshape((-1, 1)))

            # print(tbox[-1].shape)
            # print(anch[-1].shape)
            # print(tcls[-1].shape)
            # print(tangle[-1].shape)
            # print(tbox[-1][:4, :])
            # print("tcls = ", tcls)
            # print("tbox = ", tbox)
            # print(tangle.shape)
            # print("tangle = ", tangle.T)
            # print("indices = ", indices)
            # print("anch = ", anch)

        return tcls, tbox, tangle, indices, anch

    def save_DEBUG(self):
        np.savetxt("/home/mzins/dev/yolov5/runs/debug.txt", self.DEBUG)