import sys
import fcntl
import termios

cmd = "q"
print(cmd)
with open('/dev/tty1', mode='w') as f:
    fcntl.ioctl(f, termios.TIOCSTI, cmd)