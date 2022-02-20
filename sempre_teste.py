import shell


def get_gateway_by_default_route():
    cmd = shell.ShellCmd("ip route | grep default | head -n 1 | cut -d ' ' -f 3")
    cmd(False)
    if cmd.return_code != 0:
        return None

    out = cmd.stdout
    out = out.strip(' \t\n\r')
    if not out:
        return None

    return out

print(get_gateway_by_default_route())