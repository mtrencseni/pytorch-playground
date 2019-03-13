import torch

dim = 2
A = torch.rand(dim, dim, requires_grad=False)
b = torch.rand(dim, 1,  requires_grad=False)
x = torch.autograd.Variable(torch.rand(dim, 1), requires_grad=True)
stop_loss = 1e-2
step_size = stop_loss / 3.0
print('Loss before: %s' % (torch.norm(torch.matmul(A, x) - b)))
for i in range(1000*1000):
    Δ = torch.matmul(A, x) - b
    L = torch.norm(Δ, p=2)
    L.backward()
    x.data -= step_size * x.grad.data # step
    x.grad.data.zero_()
    if i % 10000 == 0: print('Loss is %s at iteration %i' % (L, i))
    if abs(L) < stop_loss:
        print('It took %s iterations to achieve %s loss.' % (i, step_size))
        break
print('Loss after: %s' % (torch.norm(torch.matmul(A, x) - b)))
