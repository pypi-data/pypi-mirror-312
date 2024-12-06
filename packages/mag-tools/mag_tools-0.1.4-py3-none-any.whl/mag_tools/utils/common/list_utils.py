import re

class ListUtils:
    @staticmethod
    def split_segment(lines, keyword_map):
        text = "\n".join(lines)
        segments = []

        for segment_name, (begin_keyword, end_keyword) in keyword_map.items():
            # 使用正则表达式找到所有匹配的段落
            pattern = rf"{segment_name}\n{begin_keyword}.*?\n{end_keyword}"
            matches = re.findall(pattern, text, re.DOTALL)

            for match in matches:
                block_lines = match.split("\n")
                segments.append(block_lines)

        return segments

if __name__ == '__main__':
    # 示例使用
    data = """GRID
##################################################
DIMENS
 5 2 1

BOX FIPNUM 1 5 1 2 1 1 = 2

PERMX
49.29276      162.25308      438.45926      492.32336      791.32867
704.17102      752.34912      622.96875      542.24493      471.45953

COPY PERMX  PERMY  1 5 1 2 1 1 
COPY PERMX  PERMZ  1 5 1 2 1 1

BOX  PERMZ  1 5 1 2 1 1  '*' 0.01

PORO
 5*0.087
 5*0.097

TOPS 10*9000.00

BOX TOPS   1  1  1 2  1  1  '='  9000.00
BOX TOPS   2  2  1 2  1  1  '='  9052.90

DXV
 5*300.0

DYV
 2*300.0

DZV
 20

#GRID END#########################################

WELL
##################################################

TEMPLATE
'MARKER' 'I' 'J' 'K1' 'K2' 'OUTLET' 'WI' 'OS' 'SATMAP' 'HX' 'HY' 'HZ' 'REQ' 'SKIN' 'LENGTH' 'RW' 'DEV' 'ROUGH' 'DCJ' 'DCN' 'XNJ' 'YNJ' /
WELSPECS
NAME 'INJE1'
''  24  25  11  11  NA  NA  SHUT  NA  0  0  0  NA  NA  NA  0.5  NA  NA  NA  1268.16  NA  NA  
''  24  25  11  15  NA  NA  OPEN  NA  0  0  DZ  NA  NA  NA  0.5  NA  NA  NA  0  NA  NA  

NAME 'PROD2'
''  5  1  2  2  NA  NA  OPEN  NA  0  0  DZ  NA  0  NA  0.5  0  0  NA  NA  NA  NA  
''  5  1  3  3  NA  NA  OPEN  NA  0  0  DZ  NA  0  NA  0.5  0  0  NA  NA  NA  NA  
''  5  1  4  4  NA  NA  OPEN  NA  0  0  DZ  NA  0  NA  0.5  0  0  NA  NA  NA  NA 
#WELL END#########################################

PROPS
##################################################
SWOF
#           Sw         Krw       Krow       Pcow(=Po-Pw)
       0.15109           0           1         400
       0.15123           0     0.99997      359.19
       0.15174           0     0.99993      257.92

#PROPS END########################################

SOLUTION
##################################################

EQUILPAR
# Ref_dep    Ref_p    GWC/OWC  GWC_pc/OWC_pc   dh
  9035       3600      9950        0.0         2
# GOC       GOC_pc
  8800        0.0    
PBVD
   5000        3600
   9000        3600

#SOLUTION END######################################
"""
    keyword_map = {
        "GRID": ("##################################################", "#GRID END#########################################"),
        "WELL": ("##################################################", "#WELL END#########################################"),
        "PROPS": ("##################################################", "#PROPS END########################################"),
        "SOLUTION": ("##################################################", "#SOLUTION END######################################")
    }

    _segments = ListUtils.split_segment(data.splitlines(), keyword_map)

    for i, segment in enumerate(_segments):
        print(f"Segment {i + 1}:")
        for line in segment:
            print(line)
        print()