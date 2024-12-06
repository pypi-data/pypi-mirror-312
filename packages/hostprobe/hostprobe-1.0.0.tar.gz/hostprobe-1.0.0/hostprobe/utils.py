def mebibyte(mbval):
    """value, represented in mebibytes, that is converted into its binary byte representation as an integer \n
    ```
    >>> one_mib = mebibyte(1)
    >>> print(one_mib)
    1048576
    ```"""
    return int(mbval * 1024 ** 2)