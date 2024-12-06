from typing import Callable, TypeVar, Final, overload


class _Feature:
    """Internal feature flag used by Pylang for special annotations."""
    pass


__T = TypeVar("__T", bound=Callable[..., ...])


@overload
def native(func: __T, /) -> __T:
    """
    Compile this function/class to native code, bypassing Pylang's default behavior.

    ### Parameters:
    - `only` (`bool`, optional):
      - `True`: Only compile this function/class into native code.
      - `False` (default): Allow Pylang to decide whether to compile the entire module.

    ### Notes:
    - Native compilation can improve performance but may alter Python's behavior.
    - If compilation fails, Pylang will fall back to interpreting the function.

    ### Example:
    ```python
    @native
    def compute(x, y):
        return x ** y

    @native(True)
    def isolated_func(a, b):
        return a + b
    ```
    """
    pass

@overload
def native(only: bool = False, /) -> Callable[[__T], __T]:
    """
    Compile this function/class to native code, bypassing Pylang's default behavior.

    ### Parameters:
    - `only` (`bool`, optional):
      - `True`: Only compile this function/class into native code.
      - `False` (default): Allow Pylang to decide whether to compile the entire module.

    ### Notes:
    - Native compilation can improve performance but may alter Python's behavior.
    - If compilation fails, Pylang will fall back to interpreting the function.

    ### Example:
    ```python
    @native
    def compute(x, y):
        return x ** y

    @native(True)
    def isolated_func(a, b):
        return a + b
    ```
    """
    pass


def pure(func: __T, /) -> __T:
    """
    Mark this function as a pure function, allowing Pylang to precompute its result.

    A pure function is one that always returns the same output for the same input and does not depend on
    or modify external state. By using the `@pure` decorator, Pylang can optimize the function by potentially
    precomputing its result at compile time, eliminating the need to call it at runtime.

    **Note**:
    - Pylang **may** precompute the result of a pure function, but this is not guaranteed. In some cases,
      Pylang may still retain the function call.
    - Make sure that the function truly adheres to the definition of a pure function, i.e., no side effects
      and consistent return values for the same inputs.
    - Using `@pure` on functions that are not pure may lead to incorrect optimizations.

    Example:
        @pure
        def add(a, b):
            return a + b
    """
    pass


skip_module: Final[_Feature] = _Feature()
"""
`skip_module` is an annotation used to mark a module that should be skipped during optimization.

To use it, place the following import at the top of your module:
    from pylang.annotations import skip_module
"""

__all__ = ["native", "pure", "skip_module"]
