from kernel import AVAILABLE_METHODS


class DataParser:
    STATUS_DICT = {0: 'OK',
                   -1: 'null_list', -2: 'unknown command',
                   -10: 'require username', -11: 'overage info',
                   -20: 'empty message', }
    CMD_LIST = AVAILABLE_METHODS

    def __init__(self, request):
        self.data_list = []
        self.request = request
        self.cmd = None
        self.parameter = None
        self.body = None
        self.status = 0
        self.clear_data = False
        self.parse_engine()

    def parse_engine(self):
        if self.fill_list() == 0:
            self.simple_validation()
            if self.status == 0:
                self.cmd = self.get_command()
                self.syntax_validation()
                if self.status == 0:
                    self.get_parameter()
                    self.get_body()

    def fill_list(self):
        try:
            self.data_list = self.request.strip(' ').split(' ')
            return 0
        except:
            return -1

    def get_command(self):
        cmd = self.data_list[0]
        if cmd.startswith('/'):
            cmd = cmd[1:]
            self.clear_data = True
        else:
            self.clear_data = False
        return cmd

    def get_parameter(self):
        if self.cmd == 'login' or self.cmd == 'msg':
            self.parameter = self.data_list[1]

    def get_body(self):
        if self.cmd == 'msg':
            self.body = self.data_list[2:]
        elif self.cmd == 'msgall':
            self.body = self.data_list[1:]

    def body_to_bytes(self, encoding='utf-8'):
        if self.body is not None:
            return bytes(' '.join(self.body), encoding)
        else:
            return None

    def body_with_name_to_bytes(self, username, encoding='utf-8'):
        if self.body is not None:
            body = ' '.join(self.body)
            body_with_name = f'[{username}]: {body}'
            return bytes(body_with_name, encoding)
        else:
            return None

    def simple_validation(self):
        self.status = 0
        if len(self.data_list) == 0:
            self.status = -1
        else:
            cmd = self.get_command()
            if cmd not in self.CMD_LIST:
                self.status = -2

    def syntax_validation(self):
        self.status = 0
        if self.cmd == 'login':
            if len(self.data_list) == 1:
                self.status = -10
            if len(self.data_list) > 2:
                self.status = -11
        elif self.cmd == 'msg':
            if len(self.data_list) == 1:
                self.status = -11
            elif len(self.data_list) == 2:
                self.status = -20
        elif self.cmd == 'msgall':
            if len(self.data_list) == 1:
                self.status = -20
        elif self.cmd == 'logout':
            if len(self.data_list) > 1:
                self.status = -11

    def get_status(self):
        self.simple_validation()
        if self.status == 0:
            self.syntax_validation()
        return self.status
