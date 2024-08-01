import sys
from pathlib import Path
import io

csvfile = sys.argv[1]
filename_without_extension = Path(csvfile).stem
outfile = filename_without_extension+".h"


with open(csvfile, 'r') as f, open(outfile, 'w') as out:
    f.readline() #skip header

    lines =[ "{%s}" % line.strip() for line in f if line]
    nl = len(lines)
    body = ",\n".join(lines)

    header_tag = "__%s_H" % filename_without_extension
    out.write("#ifndef %s\n" % header_tag)
    out.write("#define %s\n" % header_tag)
    out.write('const int %s_len = %d;\n' % (filename_without_extension, nl))
    out.write('const float %s[][2] = {\n' % filename_without_extension)
    out.write(body)
    out.write('};\n')
    out.write("#endif /* %s */" % header_tag)