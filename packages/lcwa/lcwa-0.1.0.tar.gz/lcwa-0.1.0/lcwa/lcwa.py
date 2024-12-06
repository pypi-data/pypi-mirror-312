import numpy as np
import torch
import torch.nn as nn
from copy import deepcopy
from pyhessianv2 import hessian as hessianCalculate
import time


class LCWA(nn.Module):
    """
    Loss Curvature Weighted Averaging (LCWA) implementation.

    Args:
        model (nn.Module): The neural network model to be trained
        device (torch.device): Device to run the model on (CPU or GPU)
        train_loader (DataLoader): DataLoader for training data
        criterion (nn.Module): Loss function
        layer_name (str): Name of the layer to apply LCWA (e.g., 'classifier', 'linear', 'mlp_head')
    """

    def __init__(self, model, device=None, train_loader=None, criterion=None, layer_name=None):
        super(LCWA, self).__init__()
        self.module = deepcopy(model)
        if device is not None:
            self.module = self.module.to(device)

        # Initialize buffers
        self.register_buffer('n_averaged', torch.tensor(0, dtype=torch.long, device=device))
        self.register_buffer('LCWA_sum_aps', torch.tensor(0.0, device=device))
        self.register_buffer('LCWA_sum_aps0', torch.tensor(0.0, device=device))
        self.register_buffer('swa_sum_aps', torch.tensor(0.0, device=device))

        # Store configuration
        self.criterion = criterion
        self.train_loader = train_loader
        self.layer_name = layer_name
        self.device = device

        # Initialize parameters
        self.w_243_init = 1
        self.norm_L1_sum = 0

    def forward(self, *args, **kwargs):
        """Forward pass of the model."""
        return self.module(*args, **kwargs)

    @staticmethod
    def get_model_param_vec(model):
        """Convert model parameters to a single vector."""
        vec = []
        for name, param in model.named_parameters():
            vec.append(param.detach().cpu().numpy().reshape(-1))
        return np.concatenate(vec, 0)

    @staticmethod
    def update_param(model, param_vec):
        """Update model parameters from vector."""
        param_vec = torch.from_numpy(param_vec).cuda()
        idx = 0
        for name, param in model.named_parameters():
            arr_shape = param.data.shape
            size = arr_shape.numel()
            param.data = param_vec[idx:idx + size].reshape(arr_shape).clone()
            idx += size

    def update_parameters(self, model, epoch):
        """Update LCWA parameters."""
        A = self.getA_Hessian_theory(self.train_loader, self.module, model, self.criterion, epoch)

        if self.n_averaged == 0:
            self.module = deepcopy(model)
            self.LCWA_sum_aps = A
            self.LCWA_sum_aps0 = torch.tensor(1)
        elif self.n_averaged == 1:
            self.module = deepcopy(model)
            self.LCWA_sum_aps = self.LCWA_sum_aps + A
        else:
            self.module, self.LCWA_sum_aps = self.LCWA_update(model, self.LCWA_sum_aps, A, self.module,
                                                              w0=self.LCWA_sum_aps0)
        self.n_averaged += 1
        return A

    def LCWA_update(self, mn1, Sum_an_n, an1, wn, w=0, w0=0):
        """LCWA update procedure."""
        down = Sum_an_n + an1 - w - w0
        wn1 = self.add_two_models(wn, mn1, weight1=Sum_an_n - w0, weight2=an1 - w, weight3=down)
        Sum_an_n1 = Sum_an_n + an1 - w
        return wn1, Sum_an_n1

    def add_two_models(self, m1, m2, weight1=1, weight2=1, weight3=1):
        """Add parameters of two models with weights."""
        w1 = self.get_model_param_vec(m1)
        w2 = self.get_model_param_vec(m2)
        weightAdd1 = weight1 / weight3
        weightAdd2 = weight2 / weight3
        w3 = weightAdd1.detach().cpu().numpy() * w1 + weightAdd2.detach().cpu().numpy() * w2
        self.update_param(m1, w3)
        return m1

    def set_requires_grad_for_specific_layers(self, model, layer_names):
        """Set requires_grad for specific layers."""
        for param in model.parameters():
            param.requires_grad = False

        for layer_name in layer_names:
            layer = getattr(model, layer_name, None)
            if layer is None:
                continue

            if isinstance(layer, nn.Sequential):
                for param in layer[-1].parameters():
                    param.requires_grad = True
            else:
                for param in layer.parameters():
                    param.requires_grad = True

    @staticmethod
    def decay_a(i, max_iterations=200):
        """Compute decay factor."""
        return 1 - i / max_iterations if i < max_iterations else 0

    def getA_Hessian_theory(self, train_loader, modelw, models, criterion, epoch):
        """Calculate Hessian-based weight for LCWA."""
        models.eval()
        modelw.eval()
        models.zero_grad()
        modelw.zero_grad()

        hessian_sum = 0
        vector_sum = 0
        firstGradMw = 0
        firstGradMw_sgd = 0

        models.train()
        modelw.train()
        models.to(self.device)
        modelw.to(self.device)

        totalSum = 10

        # Get model weights based on layer name
        if self.layer_name == 'classifier':
            Ms = models.classifier[-1].weight.detach().cpu().numpy().flatten()
        elif self.layer_name == 'mlp_head':
            Ms = models.mlp_head[-1].weight.detach().cpu().numpy().flatten()
        elif self.layer_name == 'linear':
            Ms = models.linear.weight.detach().cpu().numpy().flatten()
        else:
            raise ValueError(f"Unsupported layer_name: {self.layer_name}")

        for i, (input_var, target_var) in enumerate(train_loader):
            if i > totalSum:
                break

            target_var = target_var.to(self.device)
            input_var = input_var.to(self.device)

            output_s = models(input_var)
            output = modelw(input_var)
            models.zero_grad()
            modelw.zero_grad()
            input_var.requires_grad = True

            loss_s = criterion(output_s, target_var)
            loss = criterion(output, target_var)
            loss = loss.float()
            loss_s = loss_s.float()

            # Calculate gradients based on layer name
            if self.layer_name == 'classifier':
                grads = torch.autograd.grad(loss, modelw.classifier[-1].weight, create_graph=True)
                grads_sgd = torch.autograd.grad(loss_s, models.classifier[-1].weight, create_graph=True)
            elif self.layer_name == 'mlp_head':
                grads = torch.autograd.grad(loss, modelw.mlp_head[-1].weight, create_graph=True)
                grads_sgd = torch.autograd.grad(loss_s, models.mlp_head[-1].weight, create_graph=True)
            elif self.layer_name == 'linear':
                grads = torch.autograd.grad(loss, modelw.linear.weight, create_graph=True)
                grads_sgd = torch.autograd.grad(loss_s, models.linear.weight, create_graph=True)

            firstGradMw += grads[0].detach().cpu().numpy().flatten()
            firstGradMw_sgd += grads_sgd[0].detach().cpu().numpy().flatten()

            modelw.zero_grad()
            modelW_H = deepcopy(modelw)
            self.set_requires_grad_for_specific_layers(modelW_H, [self.layer_name])

            hessian_comp = hessianCalculate(modelW_H, criterion, data=(input_var, target_var),
                                            cuda=True, device=self.device)
            top_eigenvalues, top_eigenvector = hessian_comp.eigenvalues(top_n=1)

            hessian_sum += np.max(top_eigenvalues)
            vector_sum += top_eigenvector[0][0].flatten().cpu().numpy()
            eigenvector2 = top_eigenvector[0][0].flatten().cpu().numpy()

            wvalue1 = (self.LCWA_sum_aps * np.mean(np.abs(firstGradMw * eigenvector2)) /
                       (np.max(top_eigenvalues) * np.mean(np.abs(Ms * eigenvector2))))

        lambdaH = hessian_sum / (i + 1)
        eigenvector = vector_sum / (i + 1)
        DMw = firstGradMw / (i + 1)

        if self.LCWA_sum_aps == 0:
            return torch.tensor(1, dtype=torch.float64)
        else:
            wvalue2 = np.abs(
                self.LCWA_sum_aps * np.mean(np.abs(DMw * eigenvector)) /
                (lambdaH * np.mean(np.abs(Ms * eigenvector)))
            )
            wvalue = wvalue1 * self.decay_a(epoch) + (1 - self.decay_a(epoch)) * wvalue2
            return wvalue


def bn_update(loader, model, max_batches=10):
    """Update BatchNorm statistics."""
    model.train()
    for i, (input, _) in enumerate(loader):
        if i > max_batches:
            break
        input_var = input.cuda()
        _ = model(input_var)