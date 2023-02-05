# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_engine.ipynb.

# %% auto 0
__all__ = ['Value']

# %% ../nbs/00_engine.ipynb 3
class Value:
    def __init__(self,
                 data, # numeric value wrapped by `Value`
                 _children=(), # inputs to a given `Value`
                 _op='', # operation that resulted in a given `Value`
                 label='' # label for plotting graphs
                ):
        self.data = data
        self.grad = 0
        # Internal variables for graphviz
        self._backward = lambda : None
        self._prev = set(_children)
        self._op = _op
        self.label=''
    
    @staticmethod
    def _wrap(x):
        "Wrap x in Value"
        return x if isinstance(x, Value) else Value(x)
        
    def __add__(self, other):
        "self + other"
        other = self._wrap(other)
        out = Value(self.data + other.data, (self, other), _op='+')
        
        def _backward():
            self.grad += out.grad * 1 # global grad * local grad
            other.grad += out.grad * 1
        
        out._backward = _backward
        return out
        
    def __radd__(self, other):
        "other + self"
        return self + other
    
    def __sub__(self, other):
        "self - other"
        return self + (-other)
    
    def __rsub__(self, other):
        "other - self"
        return other + (-self)
    
    def __mul__(self, other):
        "self * other"
        other = self._wrap(other)
        out = Value(self.data * other.data, (self, other), _op='*')
        
        def _backward():
            self.grad += out.grad * other.data
            other.grad += out.grad * self.data
        
        out._backward = _backward
        return out
    
    def __rmul__(self, other):
        "other * mult"
        return self * other
 
    def __pow__(self, other):
        "self ** other. Other should be int or float"
        assert isinstance(other, (int,float)), f"{other} must be int or float"
        out = Value(self.data ** other, (self,), f"**{other}")
        
        def _backward():
            self.grad += out.grad * other * self.data**(other-1)
            
        out._backward = _backward
        return out
    
    def __truediv__(self, other):
        "self / other"
        return self * other**-1
    
    def __rtruediv__(self, other):
        "other / self"
        return other * self**-1
    
    def __neg__(self):
        "-self"
        return self *-1
    
    def tanh(self):
        "tanh"
        out = Value(math.tanh(self.data), (self,) , 'tanh')
        
        def _backward():
            self.grad += out.grad * (1-out**2)
        
        out._backward = _backward
        return out
        
    def relu(self):
        "relu"
        out = Value(max(self.data, 0), (self,), 'relu')
        
        def _backward():
            self.grad += out.grad * (1 if self.data > 0 else 0)
    
        out._backward = _backward
        return out
    
    def backward(self):
        topo = []
        visited = set()
        
        def topo_sort(node):
            if node not in visited:
                visited.add(node)
                for child in node._prev:
                    topo_sort(child)
                    # ipdb.set_trace()
                topo.append(node)
        topo_sort(self)
        
        # print(f"Topo list is {topo}")
        self.grad = 1
        # need to reverse because it topo returns nodes from left-to-right 
        for node in reversed(topo):
            node._backward()
        
    def __repr__(self):
        return f'Value(data={self.data})'
