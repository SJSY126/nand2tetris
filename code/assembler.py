import sys


class Parser():
    def __init__(self, filename):
        with open(filename, "r") as f:
            self.commands = f.readlines()
        self.nowline = 0
        self.nowcommand = ""

    def has_more_commands(self):
        if len(self.commands) > self.nowline:
            return True
        else:
            return False

    def advance(self):
        while True:
            command = self.commands[self.nowline].rstrip()
            self.nowline += 1
            if command != "" and command[:2] != "//":
                if "//" in command:
                    self.nowcommand = command[command.find("//")].rstrip()
                else:
                    self.nowcommand = command
                break
            else:
                pass

    def command_type(self):
        if self.nowcommand[0] == "@":
            return "A_COMMAND"
        elif self.nowcommand[0] == "(":
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    def symbol(self):
        if self.nowcommand[0] == "@":
            return self.nowcommand[1:]
        elif self.nowcommand[0] == "(":
            return self.nowcommand[1:-1]

    def dest(self):
        if "=" in self.nowcommand:
            return self.nowcommand[:self.nowcommand.find("=")]
        else:
            return "null"

    def comp(self):
        eq = self.nowcommand.find("=")
        sc = self.nowcommand.find(";")
        if eq > 0 and sc > 0:
            return self.nowcommand[eq+1:sc]
        elif eq > 0 and sc < 0:
            return self.nowcommand[eq+1:]
        elif eq < 0 and sc > 0:
            return self.nowcommand[:sc]
        else:
            return "null"

    def jump(self):
        if ";" in self.nowcommand:
            return self.nowcommand[self.nowcommand.find(";")+1:]
        else:
            return "null"


class Code():
    def __init__(self):
        self.comp_dic = {
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "!D": "0001101",
            "!A": "0110001",
            "-D": "0001111",
            "-A": "0110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "D+A": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "D|A": "0010101",
            "M": "1110000",
            "!M": "1110001",
            "-M": "1110011",
            "M+1": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "D-M": "1010011",
            "M-D": "1000111",
            "D&M": "1000000",
            "D|M": "1010101"
        }
        self.dest_dic = {
            "null": "000",
            "M": "001",
            "D": "010",
            "MD": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "AMD": "111"
        }
        self.jump_dic = {
            "null": "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111"
        }

    def dest(self, mnemonic):
        return self.dest_dic[mnemonic]

    def comp(self, mnemonic):
        return self.comp_dic[mnemonic]

    def jump(self, mnemonic):
        return self.jump_dic[mnemonic]


def main(filename):
    p = Parser(filename)
    c = Code()
    output = []
    while p.has_more_commands():
        p.advance()
        if p.command_type() == "A_COMMAND":
            # print("@"+p.symbol())
            bin = "0"+format(int(p.symbol()), "015b")
            # print(bin)
            output.append(bin+"\n")
        elif p.command_type() == "L_COMMAND":
            # print("("+p.symbol()+")")
            pass
        elif p.command_type() == "C_COMMAND":
            # print(p.dest()+"="+p.comp()+";"+p.jump())
            bin = "111"+c.comp(p.comp())+c.dest(p.dest())+c.jump(p.jump())
            # print(bin)
            output.append(bin+"\n")

    output_filename = filename.split(".asm")[0]+".hack"
    for i in range(len(output)):
        print(output[i], end="")
    with open(output_filename, "w") as f:
        f.writelines(output)


if __name__ == "__main__":
    filename = sys.argv[1]
    print(filename)
    main(filename)
