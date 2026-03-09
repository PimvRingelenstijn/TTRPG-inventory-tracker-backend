def exception_assert_helper(exc_info):
    print("\n\n======= EXCEPTION DEBUG INFO =======")
    print(f"---- Info: \n{exc_info}")
    print(f"---- Type: \n{exc_info.type}")
    print(f"---- Value: \n{exc_info.value}")
    if hasattr(exc_info.value, 'errors'):
        print(f"---- Errors: \n{exc_info.value.errors()}")
    print("====================================")
