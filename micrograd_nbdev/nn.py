# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_nn.ipynb.

# %% auto 0
__all__ = ['Module', 'Neuron']

# %% ../nbs/02_nn.ipynb 3
class Module:
    "Base class"
    def zero_grad(self):
        for p in self.parameters():
            p.grad = 0
    
    def parameters(self):
        return []

# %% ../nbs/02_nn.ipynb 4
class Neuron(Module):
    # Neuron is a single calculation node
    def __init__(self,
                 nin, # number of inputs (parameters) for each node
                 nonlin=True # whether to use nonlinearity
                ):
        self.w = [Value(random.uniform(-1,1)) for _ in range(nin)]
        self.b = Value(0)
        self.nonlin = nonlin
    
    def __call__(self, x):
        return sum([xi*wi for (xi, wi) in zip(x, self.w)]) + self.b
    
    def parameters(self):
        return [weight for weight in self.w] + [self.b]
    
    def __repr__(self):
        return f"{'ReLU' if self.nonlin  else  'Linear'} Neuron({len(self.w)})"
