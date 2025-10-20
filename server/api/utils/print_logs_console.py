def print_error(message):
    print(f"\033[91m❌ ОШИБКА: {message}\033[0m")

def print_success(message):
    print(f"\033[92m✅ УСПЕХ: {message}\033[0m")

def print_warning(message):
    print(f"\033[93m⚠️  ПРЕДУПРЕЖДЕНИЕ: {message}\033[0m")

def print_info(message):
    print(f"\033[94mℹ️  ИНФО: {message}\033[0m")