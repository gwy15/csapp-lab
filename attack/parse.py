from typing import List, Optional
from dataclasses import dataclass
import re
import subprocess
import struct
import os

@dataclass
class Instruction:
    addr: str
    hexes: List[int]
    asm: str

    def __repr__(self):
        hexes = ' '.join(f'{h:02x}' for h in self.hexes)
        return f'{self.addr:6x}: {hexes:20} \t {self.asm}'

@dataclass
class Segment:
    addr: int
    name: str
    instructions: List[Instruction]

    def __repr__(self):
        return '\n'.join([
            f'{self.addr:016x} <{self.name}>',
            *('  ' + str(ins) for ins in self.instructions)
        ])

    def try_exploit(self):
        assert len(self.instructions) == 2
        assert self.instructions[1].asm == 'retq'
        ins = self.instructions[0]
        # iterate position through hexes
        i, n = 1, len(ins.hexes)
        while i < n:
            args = ins.hexes[i:]
            if r := AsmParser.parse_hexes(args):
                if r == '<ret>': # a ret instruction is no use
                    i += 1
                    continue
                # print(self)
                # print('    !! exploitable address found!:')
                addr = self.addr + i
                print('0x{:x}: {}'.format(
                    addr,
                    ' '.join(f'{h:02x}' for h in ins.hexes[i:])
                ))
                print('\n'.join('    ' + i for i in r.split(';')))
                return

            i += 1
            


class AsmParser:
    SEGMENT_START = re.compile(r'([\da-f]{16}) <(\w+)>:')
    HEXES = r''
    INSTRUCTION = re.compile(r'  ([\da-f]+):\t(([\da-f]{2} )*[\da-f]{2})\s+(.*)')

    def parse(self, lines: List[str]) -> List[Segment]:
        segments = []
        i, n = 0, len(lines)
        while i < n:
            line = lines[i]
            if match := self.SEGMENT_START.match(line):
                # line start!
                addr, name = int(match[1], base=16), match[2]
                segment = Segment(addr=addr, name=name, instructions=[])
                segments.append(segment)
                i += 1
                # parse body
                while i < n and lines[i].strip() != '':
                    # parse line
                    line = lines[i]
                    match = self.INSTRUCTION.match(line)
                    if match is None:
                        print(lines[i])
                        raise RuntimeError
                    addr, hexes, asm = int(match[1], base=16), match[2], match[4].strip()
                    hexes = [
                        int(h, base=16) for h in hexes.split()
                    ]
                    ins = Instruction(addr=addr, hexes=hexes, asm=asm)
                    segment.instructions.append(ins)
                    i += 1
            else:
                i += 1
        return segments

    @staticmethod
    def parse_hexes(hexes: List[int]) -> Optional[str]:
        if len(hexes) == 0:
            return '<ret>'
        if hexes[0] == 0xc3:
            return '<ret>'
        if hexes[0] == 0x90:
            if rest := AsmParser.parse_hexes(hexes[1:]):
                return rest
        # popq
        if 0x58 <= hexes[0] <= 0x5f:
            if rest := AsmParser.parse_hexes(hexes[1:]):
                index = hexes[0] - 0x58
                registers = 'rax rcx rdx rbx rsp rbp rsi rdi'.split()
                ins = 'popq %{};'.format(registers[index])
                return ins + rest
        # movl
        if len(hexes) >= 2 and hexes[0] == 0x89 and 0xc0 <= hexes[1] <= 0xff:
            if rest := AsmParser.parse_hexes(hexes[2:]):
                dest = 'eax ecx edx ebx esp ebp esi edi'.split()[hexes[1] & 0x7]
                src = 'eax ecx edx ebx esp ebp esi edi'.split()[(hexes[1] - 0xc0) >> 3]
                ins = f'movl %{src}, %{dest};'
                return ins + rest
        # movq
        if len(hexes) >= 3 and hexes[0:2] == [0x48, 0x89] and 0xc0 <= hexes[2] <= 0xff:
            if rest := AsmParser.parse_hexes(hexes[3:]):
                dest = 'rax rcx rdx rbx rsp rbp rsi rdi'.split()[hexes[2] & 0x7]
                src = 'rax rcx rdx rbx rsp rbp rsi rdi'.split()[(hexes[2] - 0xc0) >> 3]
                ins = f'movq %{src}, %{dest};'
                return ins + rest
        # 
        if len(hexes) >= 2:
            op, r = hexes[:2]
            if op in [0x20, 0x08, 0x38, 0x84] and r in (0xc0, 0xc9, 0xd2, 0xdb):
                op = {0x20: 'andb', 0x08: 'orb', 0x38:'cmpb', 0x84:'testb'}[op]
                r = {0xc0:'al', 0xc9:'cl', 0xd2:'dl', 0xdb:'bl'}[r]
                if rest := AsmParser.parse_hexes(hexes[2:]):
                    ins = f'{op} %{r}, %{r};'
                    return ins + rest

        return None


if __name__ == '__main__':
    with open('rtarget.asm') as f:
        lines = f.readlines()
    segments = AsmParser().parse(lines)
    segments = {
        s.name: s
        for s in segments
    }
    exploit_funcs = [
        'getval_142',
        'addval_273',
        'addval_219',
        'setval_237',
        'setval_424',
        'setval_470',
        'setval_426',
        'getval_280',
        # phase 5
        'add_xy', 'getval_481', 'setval_296', 'addval_113', 'addval_490',
        'getval_226', 'setval_384', 'addval_190', 'setval_276', 'addval_436',
        'getval_345', 'addval_479', 'addval_187', 'setval_248', 'getval_159',
        'addval_110', 'addval_487', 'addval_201', 'getval_272', 'getval_155',
        'setval_299', 'addval_404', 'getval_311', 'setval_167', 'setval_328',
        'setval_450', 'addval_358', 'addval_124', 'getval_169', 'setval_181',
        'addval_184', 'getval_472', 'setval_350',
    ]
    for func in exploit_funcs:
        segment = segments[func]
        segment.try_exploit()
