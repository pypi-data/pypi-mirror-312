import jax
import jax.numpy as jnp
from jax import grad, jacrev, jacfwd, jvp
import jax.lax as lax
import jax.numpy as jnp
import numpy as np
from jax.tree_util import tree_flatten, tree_unflatten

def params_to_array(params_dict):
    params_flat, tree_struct = tree_flatten(params_dict)
    origin_struct = tuple(param.shape for param in params_flat)
    
    section_length = tuple(int(np.prod(shape)) for shape in origin_struct)
    
    struct_length = len(section_length)
    
    params_flat_array = jnp.concatenate([jnp.ravel(param) for param in params_flat])
    
    return params_flat_array, (origin_struct, section_length ,tree_struct, struct_length)
# def params_to_dict(params_arr, metadata):
#     """
#     Convert a 1D jnp.array back to a dictionary.

#     Args:
#         params_arr (jnp.ndarray): 1D array containing all parameter values.
#         metadata (list): List of metadata recording each parameter's key and shape.

#     Returns:
#         params_dict (dict): Dictionary with keys as strings and values as jnp.array, restored to original structure.
#     """
#     params_dict = {}
#     offset = 0

#     for key, shape in metadata:
#         size = jnp.prod(jnp.array(shape))  # Calculate the total number of elements for this parameter
#         param_values = params_arr[offset:offset + size]  # Slice out the corresponding parameter values
#         params_dict[key] = param_values.reshape(shape)  # Restore the original shape
#         offset += size

#     return params_dict

def params_to_dict(params_arr, metadata):
    params_flat = []
    offset = 0
    origin_struct, section_length ,tree_struct, struct_length = metadata
    for i in range(struct_length):
        size = section_length[i]
        param_flat = jax.lax.dynamic_slice(params_arr, (offset,), (size,))
        params_flat.append(param_flat.reshape(origin_struct[i])) 
        offset += size  
    
    return tree_unflatten(tree_struct, params_flat)




def H_xy_vy(h, x, y, vy):
    """
    Compute the Hessian-Vector Product: H_xy * vy.

    Args:
        h: Callable, scalar function h(x, y).
        x: 1D array, parameters with respect to x.
        y: 1D array, parameters with respect to y.
        vy: 1D array, vector to multiply with the Hessian H_xy (same shape as y).

    Returns:
        1D array, result of H_xy * vy (same shape as x).
    """
    # Define the function g(x, y) = ∂h / ∂x
    grad_x = lambda x_, y_: jax.grad(h, argnums=0)(x_, y_)

    # Compute the Hessian-vector product: (∂²h / ∂x ∂y^T) * vy
    _, hvp = jax.jvp(lambda y_: grad_x(x, y_), (y,), (vy,))
    return hvp

def H_yx_vx(h, x, y, vx):
    """
    Compute the Hessian-Vector Product: H_yx * vx.

    Args:
        h: Callable, scalar function h(x, y).
        x: 1D array, parameters with respect to x.
        y: 1D array, parameters with respect to y.
        vx: 1D array, vector to multiply with the Hessian H_yx (same shape as x).

    Returns:
        1D array, result of H_yx * vx (same shape as y).
    """
    # Define the function g(y, x) = ∂h / ∂y
    grad_y = lambda x_, y_: jax.grad(h, argnums=1)(x_, y_)

    # Compute the Hessian-vector product: (∂²h / ∂y ∂x^T) * vx
    _, hvp = jax.jvp(lambda x_: grad_y(x_, y), (x,), (vx,))
    return hvp

class Operater:
    def __init__(self, f, y_params_arr, x_params_arr, eta_y, eta_x):


        self.f = f
        self.y_params_arr = y_params_arr
        self.x_params_arr = x_params_arr
        self.eta_y = eta_y
        self.eta_x = eta_x
        self.shape = self.shape = (len(x_params_arr), len(x_params_arr))

    def __matmul__(self, v: jnp.array) -> jnp.array:
        """
        Performs a matrix-free matrix-vector product in JAX.

        Args:
            v: Input vector for the matrix-vector product (1D array). The same shape as x_params_arr.

        Returns:
            result: The result of the matrix-vector product (1D array).
        """
        # Scale the input vector by sqrt(eta_x) A^{1/2}_{x,t} v
        v0 = self.eta_x ** 0.5 * v

        # Compute the first Hessian-vector product: A_{y,t} * (D^2_{yx}f * v0)
        grad_fn1 = H_yx_vx(self.f, self.x_params_arr, self.y_params_arr, v0)
        v1 = self.eta_y * grad_fn1

        # Compute the second Hessian-vector product: A^{1/2}_{x,t} * (D^2_{xy}f * v1)
        grad_fn2 = H_xy_vy(self.f, self.x_params_arr, self.y_params_arr, v1)
        v2 = self.eta_x ** 0.5 * grad_fn2

        # Add the identity contribution: I * v + v2
        result = v + v2

        return result
    
    def as_function(self):
        return lambda v: self @ v


        


# def Hvp_vec(grad_fn, params, vec):
#     """
#     Hessian-vector product using JAX.
    
#     :param grad_fn: Gradient function w.r.t which the Hessian will be computed
#     :param params: Parameters for which the Hessian will be computed
#     :param vec: The vector in Hessian-vector product
#     :return: Hessian vector product
#     """
#     assert params.shape == vec.shape, "Shape mismatch: params and vec must have the same shape."
    
#     product = 
    
#     return hvp_fun(params)

# if __name__ =="__main__":
#     # 示例字典
#     params_dict = {
#         "w1": jnp.array([[1.0, 2.0], [3.0, 4.0]]),
#         "b1": jnp.array([0.5, 0.6]),
#         "w2": jnp.array([1.5, -2.3, 3.7]),
#     }

#     # 转换为数组
#     params_arr, metadata = params_to_array(params_dict)
#     print("Params Array:", params_arr)
#     print("Metadata:", metadata)

#     # 从数组还原为字典
#     reconstructed_dict = params_to_dict(params_arr, metadata)
#     print("Reconstructed Dict:", reconstructed_dict)

#     # 验证原始字典和还原字典是否一致
#     assert all(jnp.array_equal(params_dict[key], reconstructed_dict[key]) for key in params_dict)
