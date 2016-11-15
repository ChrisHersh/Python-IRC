from credentials import *
import asyncio
import re
import handlers

def start_listening():
    reader, writer = yield from asyncio.open_connection(
        server_hostname, server_port)

    write_command(writer, "PASS", server_password)
    write_command(writer, "USER", '{0} 8 * :{0}'.format(nick))
    write_command(writer, "NICK", nick)

    while True:
        line = yield from reader.readline()

        rePing = re.compile(r'PING :(.+)$')
        reError = re.compile('ERROR :(.+)$')
        reNotice = re.compile(':[^ ]+ NOTICE [^ ]+ :(.+)$')
        reComd = re.compile(':[^ ]+ (\d\d\d) ([^:]+)(?: :(.+))?$')
        rePriv = re.compile(':([^!]+)!([^@]+)@([^ ]+) PRIVMSG ([^ ]+) :(.+)$')
        reJoin = re.compile(':([^!]+)!([^@]+)@([^ ]+) JOIN ([^ ]+)$')
        reQuit = re.compile(':([^!]+)[^ ]+ QUIT :(.+)$')

        if re.match(rePing, line):
            handlers.handlePing(line)
        elif re.match(reError, line):
            handlers.handleError(line)
        elif re.match(reNotice, line):
            handlers.handleNotice(line)
        elif re.match(reComd, line):
            handlers.handleCmd(line)
        elif re.match(rePriv, line):
            handlers.handlePriv(line)
        elif re.match(reJoin, line):
            handlers.handleJoin(line)
        elif re.match(reQuit, line):
            handlers.handleQuit(line)



def write_command(writer, command: str, msg: str) -> None:
    writer.write("{}: {}\r\n".fomat(command, msg))


if __name__ == "__main__":
    start_listening()