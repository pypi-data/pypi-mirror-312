import torch
import torch.nn as nn

__all__ = ['SPDConv']

def autopad(k, p=None, d=1):  # kernel, padding, dilation
    """Pad to 'same' shape outputs."""
    if d > 1:
        k = d * (k - 1) + 1 if isinstance(k, int) else [d * (x - 1) + 1 for x in k]  # actual kernel-size
    if p is None:
        p = k // 2 if isinstance(k, int) else [x // 2 for x in k]  # auto-pad
    return p


class SPDConv(nn.Module):
    """Standard convolution with args(ch_in, ch_out, kernel, stride, padding, groups, dilation, activation)."""
    default_act = nn.SiLU()  # default activation

    def __init__(self, c1, c2, k=1, s=1, p=None, g=1, d=1, act=True):
        """Initialize Conv layer with given arguments including activation."""
        super().__init__()
        c1 = c1 * 4  # Input channels are expanded by a factor of 4
        self.conv1x1 = nn.Conv2d(c1, c2, 1, 1, 0, groups=g, bias=False)  # 1x1 convolution to adjust channel depth
        self.conv = nn.Conv2d(c2 * 4, c2, k, s, autopad(k, p, d), groups=g, dilation=d, bias=False)  # Main convolution
        self.bn = nn.BatchNorm2d(c2)
        self.act = self.default_act if act is True else act if isinstance(act, nn.Module) else nn.Identity()

    def forward(self, x):
        # Split the input tensor into 4 sub-regions (2x2 sampling)
        x1 = x[..., ::2, ::2]  # Even rows and even columns
        x2 = x[..., 1::2, ::2]  # Odd rows and even columns
        x3 = x[..., ::2, 1::2]  # Even rows and odd columns
        x4 = x[..., 1::2, 1::2]  # Odd rows and odd columns

        # Apply 1x1 convolutions to each region to adjust their channel dimensions
        x1 = self.conv1x1(x1)
        x2 = self.conv1x1(x2)
        x3 = self.conv1x1(x3)
        x4 = self.conv1x1(x4)

        # Concatenate the 4 processed sub-regions along the channel dimension
        x = torch.cat([x1, x2, x3, x4], 1)  # Concatenate along the channel axis

        # Apply the main convolution, batch normalization, and activation
        return self.act(self.bn(self.conv(x)))

    def forward_fuse(self, x):
        """Perform transposed convolution of 2D data."""
        # Split the input tensor into 4 sub-regions (2x2 sampling)
        x1 = x[..., ::2, ::2]
        x2 = x[..., 1::2, ::2]
        x3 = x[..., ::2, 1::2]
        x4 = x[..., 1::2, 1::2]

        # Apply 1x1 convolutions to each region to adjust their channel dimensions
        x1 = self.conv1x1(x1)
        x2 = self.conv1x1(x2)
        x3 = self.conv1x1(x3)
        x4 = self.conv1x1(x4)

        # Concatenate the 4 processed sub-regions along the channel dimension
        x = torch.cat([x1, x2, x3, x4], 1)

        # Apply the final convolution (without batch normalization in the fuse case)
        return self.act(self.conv(x))

# import torch
# import torch.nn as nn
#
# __all__ = ['SPDConv']
#
#
# def autopad(k, p=None, d=1):  # kernel, padding, dilation
#     """Pad to 'same' shape outputs."""
#     if d > 1:
#         k = d * (k - 1) + 1 if isinstance(k, int) else [d * (x - 1) + 1 for x in k]  # actual kernel-size
#     if p is None:
#         p = k // 2 if isinstance(k, int) else [x // 2 for x in k]  # auto-pad
#     return p
#
#
# class SPDConv(nn.Module):
#     """Standard convolution with args(ch_in, ch_out, kernel, stride, padding, groups, dilation, activation)."""
#     default_act = nn.SiLU()  # default activation
#
#     def __init__(self, c1, c2, k=1, s=1, p=None, g=1, d=1, act=True):
#         """Initialize Conv layer with given arguments including activation."""
#         super().__init__()
#         c1 = c1 * 4
#         self.conv = nn.Conv2d(c1, c2, k, s, autopad(k, p, d), groups=g, dilation=d, bias=False)
#         self.bn = nn.BatchNorm2d(c2)
#         self.act = self.default_act if act is True else act if isinstance(act, nn.Module) else nn.Identity()
#
#     def forward(self, x):
#         x = torch.cat([x[..., ::2, ::2], x[..., 1::2, ::2], x[..., ::2, 1::2], x[..., 1::2, 1::2]], 1)
#         """Apply convolution, batch normalization and activation to input tensor."""
#         return self.act(self.bn(self.conv(x)))
#
#     def forward_fuse(self, x):
#         """Perform transposed convolution of 2D data."""
#         x = torch.cat([x[..., ::2, ::2], x[..., 1::2, ::2], x[..., ::2, 1::2], x[..., 1::2, 1::2]], 1)
#         return self.act(self.conv(x))

