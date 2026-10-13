"""Focused source-grounded editorial repairs and notes; no solutions."""
import re
from putnam_tex_native import native
NOTES={
 (1985,'A6'):'Editorial notation repair: the displayed identity uses F(x), the polynomial defined immediately above. Both archive files define uppercase F but then print lowercase f in that identity.',
 (1990,'A6'):'Editorial notation repair: |X| denotes cardinality. The archive sentence prints X for both the set and its size; the surrounding conditions already use cardinality bars.',
 (1990,'B6'):'Editorial notation repair: the two support lines are parallel to K. The archive introduces K but prints the undefined symbol K_1 in this clause.',
 (1992,'B6'):'Transcription repair: the final request to prove that the set contains at most n^2 matrices is restored from the complete archive TeX and university examination PDF.',
 (1993,'A1'):'Diagram provenance: the schematic is reconstructed from the explicit region descriptions in both archive and university transcriptions; it is not a crop of an original examination image.',
 (2005,'A2'):'Diagram provenance: the illustrative rook tour is recovered from the university examination PDF, page 1. The mathematical definition and question are retained.',
 (2007,'A6'):'Source comparison repair: each side of P belongs to exactly one triangle, as the university examination PDF explicitly states. The archive TeX omitted the words of P. The university version has no example figure in this statement.',
 (2011,'A1'):'Diagram provenance: the illustrative spiral is reconstructed from the complete directed-step definition; it is not an original examination figure.',
 (2013,'A6'):'Native table transcription: all 25 entries and the row/column labels are retained from the source table, checked visually in the archive PDF. The table is mathematical text, not an image.',
 (2020,'A6'):'Source notation clarification: f_N is the corrected lowercase function name in the archive. Its TeX footnote records that the original used uppercase F_N; that source note is retained here rather than exposed as a typesetting command.',
 (2020,'A1'):'Historical edition note: the 2020 examination was postponed to February 20, 2021 and held unofficially; the archive\u2019s 2020 edition label is retained.',
 (2024,'B2'):'Diagram provenance: the partner-quadrilateral figure is recovered from the Session B question reproduced in a public GitHub document; only the question diagram is imported.',
}
TABLE=r'''$$\begin{array}{c|rrrrr}
a\backslash b&-2&-1&0&1&2\\\hline
-2&-1&-2&2&-2&-1\\
-1&-2&4&-4&4&-2\\
0&2&-4&12&-4&2\\
1&-2&4&-4&4&-2\\
2&-1&-2&2&-2&-1
\end{array}$$'''
def prepare(y,n,text):
 if (y,n)==(1989,'A6'):
  text=re.sub(r'\\parbox\{2in\}\{if every block of zeros in the binary expansion of \$n\$\s*has an even number of zeros in the block\}',lambda m:r'\text{if every block of zeros in the binary expansion of }n\text{ has an even number of zeros in the block}',text)
  text=text.replace(r'\\[.3in]',r'\\')
 if (y,n)==(1985,'A6'):text=text.replace(r'\Gamma(f(x)^n)',r'\Gamma(F(x)^n)')
 if (y,n)==(1990,'A6'):text=text.replace('let $X$ denote','let $|X|$ denote')
 if (y,n)==(1990,'B6'):text=text.replace('$K_1$','$K$')
 if (y,n)==(1993,'A1'):text=text.replace('[Figure not included. The first region','[The first region')
 if (y,n)==(2003,'A5'):text=re.sub(r'\\begin\{center\}\s*\\begin\{tikzpicture\}[\s\S]*?\\end\{tikzpicture\}\s*\\end\{center\}','',text)
 if (y,n)==(2005,'A2'):text=text.replace('was depicted in the original.','is shown below.')
 if (y,n)==(2007,'A6'):
  text=text.replace('each side is a side','each side of $P$ is a side');text=re.sub(r'For example,\s*\[figure\s*omitted\.\]','',text)
 if (y,n)==(2011,'A1'):text=text.replace('[Picture omitted.]','')
 if (y,n)==(2013,'A6'):text=re.sub(r'\\begin\{center\}\s*\\begin\{tabular\}[\s\S]*?\\end\{tabular\}\s*\\end\{center\}',lambda m:TABLE,text)
 if (y,n)==(2016,'A4'):text=re.sub(r'\\\[\s*\\setlength[\s\S]*?\\end\{picture\}\s*\\\]','',text)
 if (y,n)==(2020,'A6'):text=re.sub(r'\\footnote\{[^{}]*\}','',text)
 if (y,n)==(2024,'B2'):text=text.replace('[A diagram has been omitted.]','')
 return native(text)
