import re
import time
import socket

def get_generated_files(text):
    patterns = {
        'html': r'```html\n(.+?)\n```',
        'jsx': r'```jsx\n(.+?)\n```',
        'tsx': r'```tsx\n(.+?)\n```',
    }
    result = {}

    for ext, pattern in patterns.items():
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            content = '\n'.join(matches).strip()
            result[f'index.{ext}'] = content

    if len(result) == 0:
        result["index.html"] = text.strip()
    return result


def remove_code_block(text):
    pattern = r"```html\n(.+?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return text.strip()

        
def get_random_available_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0)) # a random socket
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
        _, port = s.getsockname()   # get port
    return port


def wait_for_port(port, timeout=10):
    """
        Wait the port to be listend
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("localhost", port))
                return True
        except (ConnectionRefusedError, OSError):
            time.sleep(0.5)  
    return False  

# if __name__ == "__main__":
#     for i in range(10):
#         port = get_random_available_port()
#         print(f"随机可用端口: {port}")