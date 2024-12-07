import torch
from torch.library import Library, impl, _impls
from torch._ops import OpOverload

torch_npu_m = Library("npu", "IMPL", "Meta")
crossing_npu_m = Library("crossing_npu", "IMPL", "Meta")


def check_exists(m, op_name, dispatch_key=""):
    if dispatch_key == "":
        dispatch_key = m.dispatch_key

    if isinstance(op_name, str):
        name = op_name
    elif isinstance(op_name, OpOverload):
        name = op_name._schema.name
        overload_name = op_name._schema.overload_name
        if overload_name != "":
            name = name + "." + overload_name
    else:
        raise RuntimeError(
            "impl should be passed either a name or an OpOverload object as the first argument"
        )

    key = m.ns + "/" + name.split("::")[-1] + "/" + dispatch_key
    return key in _impls


def torch_npu_impl_if_exists(m, op_name):
    def wrapper(f):
        import torch_npu

        if hasattr(torch_npu, op_name):
            if check_exists(m, op_name):
                m.m.impl(op_name, m.dispatch_key, f)
            else:
                impl(m, op_name)(f)

    return wrapper


def crossing_npu_impl_if_exists(m, op_name):
    def wrapper(f):
        import crossing_npu

        if hasattr(crossing_npu.ops, op_name):
            if check_exists(m, op_name):
                m.m.impl(op_name, m.dispatch_key, f)
            else:
                impl(m, op_name)(f)

    return wrapper


@torch_npu_impl_if_exists(torch_npu_m, "npu_geglu")
def npu_geglu(hidden_states, dim=-1, approximate=1, activate_left=False):
    shape = list(hidden_states.shape)
    shape[dim] = shape[dim] // 2
    result = torch.empty(shape, dtype=hidden_states.dtype, device=hidden_states.device)
    result_gelu = torch.empty(
        shape, dtype=hidden_states.dtype, device=hidden_states.device
    )
    return result, result_gelu
