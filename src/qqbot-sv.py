# coding:utf-8
# by e0e
import BaseHTTPServer, urllib
from qqbot import _bot as bot
import re, time, signal


class NoticeHandler():
    def __init__(self, qq_num_sender='2590870063', ip='0.0.0.0', port='8189'):
      self.qq_num_sender = qq_num_sender
      self.ip = ip
      self.port = port

    def Notice(self, nickname='jack', content='Hello World'):
        try:
            bot.Login(['-q', self.qq_num_sender, '-ip', self.ip, '-hp', self.port, '--daemon','-r'])
            nickname = 'jack' if nickname =='' else nickname
            content = 'Hello World' if content =='' else content
            bl = bot.List('buddy', nickname)
            if bl:
                b = bl[0]
                bot.SendTo(b, content)
                return "Notice '{ct}' sent to {nickname} successfully!".format(ct=content, nickname=nickname)
            return 'Get buddy error!'
        except:
            return 'Notice Error!'
    
    def Update(self, update=False):
        if (update):
            bot.Login(['-q', self.qq_num_sender, '-ip', self.ip, '-hp', self.port, '--daemon','-r'])
            bot.Update('buddy')
            bot.Update('group')
            return "update successfully!"

class ServerException(Exception):
    '''服务器内部错误'''
    print Exception
    pass

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def handler(self, signum, frame):
        self.send_content("Timeout!")
    
    def do_GET(self):
        try:
            full_path = self.path
            content = ''
            nickname = ''
            update = ''
            print full_path
            if '?' in self.path:
                query = urllib.splitquery(self.path)
                action = query[0]
                if query[1]: 
                    queryParams={}
                    for qp in query[1].split('&'):
                        kv = qp.split('=')
                        queryParams[kv[0]] = urllib.unquote(kv[1]).decode("utf-8",'ignore')
                    if 'content' in queryParams.keys():
                        content = queryParams['content']
                    if 'nickname' in queryParams.keys():
                        nickname = queryParams['nickname']
                    if 'update' in queryParams.keys():
                        update = queryParams['update']
                        signal.signal(signal.SIGALRM, self.handler)
                        signal.alarm(10)
                        res = NoticeHandler().Update(update)
                        signal.alarm(0)
                        self.send_content(res)
                        return True

            if ('ntype' in queryParams.keys() and queryParams['ntype']=='qq'):
                signal.signal(signal.SIGALRM, self.handler)
                signal.alarm(10)
                res = NoticeHandler().Notice(nickname, content)
                self.send_content(res)
                signal.alarm(0)
                return True
            else:
                excep = "Unknown object '{0}'".format(self.path)
                self.send_content(excep)
                raise ServerException(excep)

        except Exception as msg:
            print msg
            self.send_content('do_Get error!')
            pass

    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


if __name__ == '__main__':
    NoticeHandler().Notice(content='Login successfully!')
    serverAddress = ('', 1999)
    server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()