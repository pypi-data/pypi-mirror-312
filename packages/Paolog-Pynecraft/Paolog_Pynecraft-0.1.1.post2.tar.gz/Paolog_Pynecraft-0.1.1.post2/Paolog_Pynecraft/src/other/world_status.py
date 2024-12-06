class WORLD_STATUS:
    VALID = "valid"
    DEPRECATED = "deprecated"
    NEWER = "newer"
    INVALID = "invalid"

class WORLD_GENERATOR_STATUS:
    class WORLD_SIZE_0(Exception): pass

    class EMPTY_WORLD_NAME(Exception): pass

    class INVALID_WORLD_NAME(Exception): pass

    class OS_ERROR(Exception): pass

    class UNKNOWN_EXCEPTION(Exception): pass
