"""Native card conversion for document-level TeX. Never delete statement tails."""
import re

def normalize_nested_text_math(text):
 offset=0
 while True:
  match=re.search(r'\\(?:mbox|text)\s*\{',text[offset:])
  if not match:break
  start=offset+match.start();begin=offset+match.end();end=begin;depth=1
  while end<len(text) and depth:
   if text[end]=='{' and (end==0 or text[end-1]!='\\'):depth+=1
   if text[end]=='}' and (end==0 or text[end-1]!='\\'):depth-=1
   end+=1
  if depth:raise ValueError('Unbalanced text macro')
  body=text[begin:end-1];chunks=re.split(r'(?<!\\)\$',body)
  if len(chunks)>1:
   if len(chunks)%2==0:raise ValueError('Unbalanced nested text math')
   replacement=''.join((r'\text{'+c+'}' if i%2==0 else c) for i,c in enumerate(chunks) if c)
   text=text[:start]+replacement+text[end:];offset=start+len(replacement)
  else:offset=end
 return text

def native(text):
 for a,b in {r'\bA':r'\mathbf{A}',r'\bB':r'\mathbf{B}',r'\MM':r'\mathcal{M}',r'\RR':r'\mathbb{R}',r'\FF':r'\mathbb{F}',r'\Z':r'\mathbb{Z}'}.items():
  text=re.sub(re.escape(a)+r'(?![A-Za-z])',lambda m:b,text)
 text=re.sub(r'\{\\cal\s+([A-Za-z])\}',r'\\mathcal{\1}',text)
 text=re.sub(r'\{\\em\s+([^{}]*)\}',r'\1',text)
 text=re.sub(r'\\(?:emph|textbf|textit)\{([^{}]*)\}',r'\1',text)
 for env in ['itemize','enumerate','center','verse']:
  text=text.replace(r'\begin{'+env+'}','').replace(r'\end{'+env+'}','')
 text=re.sub(r'\\item\s*\[([^]]+)\]',lambda m:'\n\n'+m[1]+' ',text)
 text=re.sub(r'\\item\b','\n\n• ',text).replace(r'\noindent','')
 for env,target in [('align*','aligned'),('gather*','gathered')]:
  text=text.replace(r'\begin{'+env+'}', '$$\n'+r'\begin{'+target+'}').replace(r'\end{'+env+'}',r'\end{'+target+'}'+'\n$$')
 text=text.replace(r'\[','$$').replace(r'\]','$$').replace(r'\(','$').replace(r'\)','$')
 text=text.replace(r'\%','%').replace(r'\medskip','').replace(r'\smallskip','')
 text=re.sub(r'\\textsuperscript\{([^{}]*)\}',r'\1',text)
 text=normalize_nested_text_math(text)
 return re.sub(r'\n\s*\n\s*\n','\n\n',text).strip()
