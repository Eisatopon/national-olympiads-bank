"""Record-by-record mathematical comparison repairs. No solutions are imported."""
import re
REPLACE={
 (1938,'A7'):[('(page 82)','')],
 (1938,'B1'):[('(page 86)','')],
 (1939,'A5'):[('(page 101)','')],
 (1939,'A6'):[('(page 105)','')],
 (1939,'A7'):[('(page 109)','')],
 (1939,'B6'):[('(page 123)','')],
 (1941,'B6'):[('d x d y d z=', 'd z d y d x=')],
}
OVERRIDE={
 (1938,'B6'):r'''Find the shortest distance between the plane $Ax+By+Cz+1=0$ and the ellipsoid $x^2/a^2+y^2/b^2+z^2/c^2=1$. (For brevity, let $h=1/\sqrt{A^2+B^2+C^2}$ and $m=\sqrt{a^2A^2+b^2B^2+c^2C^2}$.) State algebraically the condition that the plane shall lie outside the ellipsoid.''',
 (1939,'A3'):r'''Find the cubic equation whose roots are the cubes of the roots of $x^3+ax^2+bx+c=0$.''',
 (1940,'A8'):r'''A triangle is bounded by the lines $A_ix+B_iy+C_i=0$, $i=1,2,3$. Show that its area, disregarding sign, is
$$\frac{\Delta^2}{2|(A_2B_3-A_3B_2)(A_3B_1-A_1B_3)(A_1B_2-A_2B_1)|},$$
where $\Delta=\det\begin{pmatrix}A_1&B_1&C_1\\A_2&B_2&C_2\\A_3&B_3&C_3\end{pmatrix}$.''',
 (1940,'B5'):r'''Determine all rational values for which $a,b,c$ are the roots of $x^3+ax^2+bx+c=0$.''',
 (1940,'B6'):r'''Prove that the determinant of the $n\times n$ matrix whose entries are $a_ia_j$ for $i\neq j$ and $a_i^2+k$ for $i=j$ is divisible by $k^{n-1}$, and find its other factor.''',
 (1941,'A7'):r'''Take either (i) or (ii).
(i) Prove that
$$\det\begin{pmatrix}1+a^2-b^2-c^2&2(ab+c)&2(ca-b)\\2(ab-c)&1+b^2-c^2-a^2&2(bc+a)\\2(ca+b)&2(bc-a)&1+c^2-a^2-b^2\end{pmatrix}=(1+a^2+b^2+c^2)^3.$$
(ii) A semi-ellipsoid of revolution is formed by revolving about the $x$-axis the area lying within the first quadrant of the ellipse $x^2/a^2+y^2/b^2=1$. Show that this semi-ellipsoid will balance in stable equilibrium, with its vertex resting on a horizontal plane, when and only when $b\sqrt8\geq a\sqrt5$.''',
 (1941,'B2'):r'''Evaluate the following limits:
(i) $\displaystyle\lim_{n\to\infty}\sum_{i=1}^{n}\frac1{\sqrt{n^2+i^2}}$;
(ii) $\displaystyle\lim_{n\to\infty}\sum_{i=1}^{n}\frac1{\sqrt{n^2+i}}$;
(iii) $\displaystyle\lim_{n\to\infty}\sum_{i=1}^{n^2}\frac1{\sqrt{n^2+i}}$.''',
 (1942,'A3'):r'''Is the series $\displaystyle\sum_{n=0}^{\infty}\frac{n!}{(n+1)^n}\left(\frac{19}{7}\right)^n$ convergent or divergent?''',
}
NOTES={
 (1938,'A3'):'Source convention: the maximum at t=0 is a local maximum of speed, not a global maximum on the whole real line.',
 (1940,'B4'):'Unresolved source error: Scholes explicitly retains only the necessary director-sphere condition and identifies the converse in the longer statement as problematic. The longer statement is retained here as a historical transcription, not as a mathematically certified assertion.',
 (1941,'B6'):'Incomplete source condition: continuity on the open interval alone does not ensure that the stated integrals exist. The source wording is retained; convergence or appropriate endpoint regularity is needed for a finite-integral interpretation.',
}
VARIANTS={
 (1939,'A5'):'The longer transcription times the passage from the horizontal to the lowest position. Scholes instead starts the timing near the unstable upper equilibrium. The longer, mathematically consistent timing is retained.',
 (1940,'A3'):'The longer transcription uses indefinite integrals with suitably chosen constants and exponent n; Scholes uses definite integrals, a fixed real exponent, and additional regularity. These formulations are not certified as identical.',
 (1940,'A7'):'The longer statement specifies an integer exponent p>=2. This integer restriction is retained; Scholes does not spell it out.',
 (1940,'B3'):'The discriminant term is cubic in (2p-a) in the longer transcription; the secondary page prints a square. The cubic is retained and independently checked from the normal-line cubic.',
 (1941,'A2'):'The longer transcription includes the factor exp(n t) in the integrand, which is absent from the secondary page. This difference remains explicitly recorded.',
 (1941,'A7'):'The secondary page has y^2 b^2 in its ellipse equation; the longer transcription gives y^2/b^2. The quotient is retained, consistent with the stated semi-axis lengths and balance condition.',
 (1942,'A5'):'The longer transcription specifies b>a. This hypothesis is retained even though the secondary page omits it.',
}
def native(text):
 text=re.sub(r'^\s*(?:(?:Problem\s+)?[AB][-−]?\d+|\d+)[.]?\s*','',text)
 text=re.sub(r'\(page\s+\d+\)','',text)
 return text.replace(r'\(', '$').replace(r'\)', '$').replace(r'\[','$$').replace(r'\]','$$').strip()
REVIEWED={(y,'regular',label) for y,na,nb in [(1938,7,6),(1939,7,7),(1940,8,7),(1941,7,7),(1942,6,5)] for session,count in [('A',na),('B',nb)] for label in [f'{session}{i}' for i in range(1,count+1)]}
CATEGORIES={1938:'GGXGXX AXGGGG',1939:'XGAGXG GX XAGXXX',1940:'NGXGGA XG XGGANA X',1941:'AXGAGX AGXXXGXX',1942:'GAXGGG GGXXX'}
CATEGORIES.update({1938:'GGXGXGGAXXGGG',1939:'XGAGXGGGXAGXXA',1940:'NGXGGAXGXGGGAAX',1941:'AXGAGXAXXXGXXA',1942:'GAXGGGGGXXX',1946:'XAGXGXGGXXNX',1947:'XAGXAAXXGANG',1948:'AGX XAX AGNX XA',1949:'GGXGAXNXGAXG'})
REPLACE.update({
 (1948,'A4'):[(r'\lim _{d \rightarrow 0}',r'\lim _{\delta \rightarrow 0}')],
 (1948,'B6'):[(r'z_{2^{2}}+z_{3^{2}}',r'z_{2}^{2}+z_{3}^{2}')],
 (1949,'B2'):[(r'^{-12}',r'^{-1/2}')],
 (1949,'B5'):[(r'\lim _{n \rightarrow \infty} \sup',r'\limsup _{n \rightarrow \infty}')],
})
OVERRIDE.update({
 (1946,'B5'):r'''Show that the integer next above $(\sqrt3+1)^{2n}$ is divisible by $2^{n+1}$.''',
 (1947,'A3'):r'''Let $V_1,V_2,V_3$ be the vertices of a triangle and let $V_4$ be an interior point. Let $s_1,\ldots,s_6$ be the six segments joining pairs of these four vertices. Given any two points $Q_1,Q_2$ in the plane not on these segments, show that there does not exist a polygonal line $P$ joining $Q_1$ to $Q_2$ such that:
(i) $P$ crosses each $s_i$, $i=1,\ldots,6$, exactly once;
(ii) $P$ does not intersect itself;
(iii) $P$ does not pass through any vertex $V_1,V_2,V_3,V_4$.''',
 (1947,'B2'):r'''Let $f(x)$ be a differentiable function defined on the closed interval $[0,1]$ and such that $|f'(x)|\leq M$ for $0<x<1$. Prove that
$$\left|\int_0^1 f(x)\,dx-\frac1n\sum_{k=1}^{n}f\left(\frac{k}{n}\right)\right|\leq\frac{M}{n}.$$''',
 (1948,'A5'):r'''If $x_1,\ldots,x_n$ denote the $n$th roots of unity, evaluate $\displaystyle\prod_{i<j}(x_i-x_j)^2$.''',
 (1948,'B3'):r'''If $n$ is a positive integer, prove that $[\sqrt n+\sqrt{n+1}]=[\sqrt{4n+2}]$, where $[x]$ denotes the greatest integer not exceeding $x$.''',
 (1949,'A6'):r'''Prove that for every real or complex $x$,
$$\prod_{k=1}^{\infty}\frac{1+2\cos(2x/3^k)}{3}=\frac{\sin x}{x}.$$''',
 (1949,'B4'):r'''Show that the coefficients $a_1,a_2,a_3,\ldots$ in the expansion
$$\frac14\left[1+x-\sqrt{1-6x+x^2}\right]=a_1x+a_2x^2+a_3x^3+\cdots$$
are positive integers.''',
})
NOTES.update({
 (1947,'A2'):'Unresolved source error: the identically zero function satisfies the functional equation, but the displayed conclusion is undefined at x=0 without a separate zero-function case. The printed formulation is retained.',
 (1948,'A6'):'Source convention: the real power-series identity in alternative (ii) is interpreted on |x|<1, its interval of convergence.',
 (1949,'A6'):'Source convention: at x=0 the quotient sin(x)/x is interpreted by its removable extension.',
 (1949,'B6'):'Source convention: the perpendicular is the segment from O towards the tangent foot; its intersection on that side of O determines T(P). Choosing the opposite intersection would describe a different iteration.',
})
VARIANTS.update({
 (1947,'A3'):'The original transcription refers to an unavailable six-edge figure. Its configuration has been made explicit from the secondary source: a triangle, an interior vertex, and all six connecting segments. Infinite supporting lines are not substituted for the six segments.',
 (1947,'B2'):'The longer transcription says closed interval but prints (0,1). The endpoints are required by the sampled value f(1). The closed interval is transcribed as [0,1], without changing the derivative bound on its interior.',
})
REVIEWED.update((y,'regular',f'{s}{n}') for y in range(1946,1950) for s in 'AB' for n in range(1,7))
REPLACE.update({
 (1950,'A3'):[(r'\lim _{n-\infty}',r'\lim _{n\to\infty}')],
 (1950,'A4'):[(r'e^{-t^{2 / 2}}',r'e^{-t^{2}/2}')],
 (1950,'B2'):[(r'(a b)^{12}',r'\sqrt{ab}')],
 (1952,'B7'):[(r'\lim _{j-\infty}',r'\lim _{j\to\infty}')],
 (1953,'B4'):[(r'point \( (1,1 \), 1)',r'point \( (1,1,1) \)')],
 (1954,'A2'):[(r'P_{i} \) and \( P_{i}',r'P_{i} \) and \( P_{j}')],
})
OVERRIDE.update({
 (1951,'A3'):r'''Find the sum to infinity of the series $\displaystyle\sum_{n=0}^{\infty}\frac{(-1)^n}{3n+1}$.''',
 (1951,'A4'):r'''Trace the curve whose equation is $y^4-x^4-96y^2+100x^2=0$.''',
 (1951,'A7'):r'''Show that if the series $a_1+a_2+a_3+\cdots$ converges, then the series $a_1+a_2/2+a_3/3+\cdots+a_n/n+\cdots$ converges also.''',
 (1951,'B3'):r'''Show that if $x$ is positive, then $\log_e(1+1/x)>1/(1+x)$.''',
 (1951,'B6'):r'''Assuming that all roots of $x^3+ax^2+bx+c=0$ are real, show that the difference between the greatest and least roots is not less than $\sqrt{a^2-3b}$ or greater than $2\sqrt{a^2-3b}/\sqrt3$.''',
 (1952,'A5'):r'''Let $a_j$, $j=1,\ldots,n$, be entirely arbitrary numbers except that none is equal to unity. Prove
$$a_1+\sum_{i=2}^{n}a_i\prod_{j=1}^{i-1}(1-a_j)=1-\prod_{j=1}^{n}(1-a_j).$$''',
 (1953,'A6'):r'''Show that the sequence
$$\sqrt7,\quad\sqrt{7-\sqrt7},\quad\sqrt{7-\sqrt{7+\sqrt7}},\quad\sqrt{7-\sqrt{7+\sqrt{7-\sqrt7}}},\quad\ldots$$
converges, and evaluate its limit.''',
 (1953,'B5'):r'''Show that the roots of $x^4+ax^3+bx^2+cx+d=0$, if suitably numbered, satisfy $r_1/r_2=r_3/r_4$, provided $a^2d=c^2\neq0$.''',
 (1953,'B6'):r'''Let $P,Q$ be points inside a circle with center $C$, such that $CP=CQ$. Determine the location of a point $Z$ on the circle such that $PZ+QZ$ is a minimum.''',
})
VARIANTS.update({
 (1950,'A4'):'The longer transcription specifies a right prism; this restriction is retained. The exponent in the integral is -t^2/2, not -t^(2/2), as confirmed by the secondary identity.',
 (1950,'B1'):'Multiple boys at one house are retained as separate contributions to total walking distance. The secondary version allows repeated points, which is the equivalent weighted configuration.',
 (1950,'B5'):'The longer version concerns convergence of sequences s_n and s_n+2s_(n+1). The secondary version concerns series. The sequence formulation is retained rather than replacing it with a different question.',
 (1951,'B6'):'Repeated real roots are allowed in the longer version, whose lower inequality is non-strict. The secondary version assumes distinct roots and gives a strict lower inequality. The original non-strict formulation is retained.',
 (1952,'B3'):'The nonzero coefficient restriction a_i!=0 in the longer version is retained; it is omitted from the secondary wording.',
 (1953,'B6'):'The longer transcription has a corrupted equality between PZ and QZ. The secondary statement explicitly minimizes their sum. The sum PZ+QZ is restored while retaining CP=CQ and both points inside the circle.',
})
NOTES.update({
 (1950,'B3'):'Source convention: calendar probability is interpreted as relative frequency in the repeating 400-year Gregorian calendar cycle, not a uniform probability distribution on all positive integers.',
 (1954,'B3'):'Source notation: parentheses (a,b) are explicitly defined here to mean a closed interval; this historical convention is retained.',
})
REVIEWED.update((y,'regular',f'{s}{n}') for y in range(1950,1955) for s in 'AB' for n in range(1,7 if y==1950 else 8))
CATEGORIES.update({1950:'GXXGNNGGCGXG',1951:'AGXGNGXXXXGGAG',1952:'NGAGANXGXAGXGX',1953:'XCAXGXAXNXGAGN',1954:'CGXXXXNNXAGXNX'})
REPLACE.update({
 (1956,'A4'):[(r'z^{\prime \prime}',r'z^{n}')],
 (1957,'A3'):[('a positive integer','an integer greater than 1')],
 (1958,'Spring','A5'):[('f(u, v) d u d v','f(u, v) d v d u')],
 (1958,'Spring','B3'):[(r'(n-1)(n)(2 n-1)^{\prime} 6',r'\frac{(n-1)n(2n-1)}{6}')],
 (1958,'Fall','A7'):[(r'\lim _{n-\infty}',r'\lim _{n\to\infty}'),(r'\sum_{y=1}^{n}',r'\sum_{q=1}^{n}')],
})
OVERRIDE.update({
 (1955,'B2'):r'''Suppose that $f$ has two continuous derivatives and $f(0)=0$. Prove that the function $g$, defined by $g(0)=f'(0)$ and $g(x)=f(x)/x$ for $x\neq0$, has a continuous derivative.''',
 (1956,'B2'):r'''Suppose that each set $X$ of points in the plane has an associated set $\bar X$, called its cover. Suppose further that
$$\overline{X\cup Y}\supseteq\overline{\bar X}\cup\bar Y\cup Y.\tag{1}$$
Here $\cup$ denotes union and $\supseteq$ denotes set inclusion. Prove:
(i) $\bar X\supseteq X$;
(ii) $\overline{\bar X}=\bar X$;
(iii) $X\supseteq Y$ implies $\bar X\supseteq\bar Y$.
Prove conversely that (i), (ii) and (iii) imply (1).''',
})
NOTES.update({
 (1955,'A4'):'Source convention: the intersections counted are inside the circle, excluding the n selected endpoints, as made explicit by the secondary source.',
 (1956,'B5'):'Source convention: a triangle means a 3-cycle in the joining graph; a nonzero geometric area is not part of the graph assertion.',
 (1956,'B7'):'Incomplete source condition: unequal constant polynomials can satisfy both empty-root-set conditions. The standard nonconstant-polynomial interpretation is required; it is not explicitly stated in either available transcription.',
 (1957,'A3'):'Editorial correction: k>1 is required for the strict inequality. The longer transcription says positive integer, which would include k=1 and give 0<0. The secondary source explicitly excludes that case.',
 (1958,'Spring','A3'):'Source convention: successive random choices are independent and uniform on [0,1].',
 (1958,'Spring','A6'):'Source convention: a positive annual interest rate is assumed for a finite perpetuity investment.',
 (1958,'Spring','B4'):'Source convention: the two points are independently uniform with respect to surface area.',
 (1958,'Fall','B5'):'Source convention: successive turns have the same directed angle. The phrase if there is one retains the possible absence of a finite limiting point.',
})
VARIANTS.update({
 (1955,'B4'):'The longer question asks for one million consecutive integers; the secondary inclusive indexing gives one million and one. The explicit count in the longer question is retained.',
 (1956,'B2'):'A missing overline and set-inclusion sign in the first condition are restored from the secondary closure-operator formulation. Inclusion is non-strict.',
 (1957,'A6'):'Both available versions initialize the second term separately from the subsequent accumulation. The longer transcription is retained without inserting a missing initial summand into all later terms.',
 (1957,'B7'):'Covering is by congruent copies, allowing translations and rotations as made explicit by the secondary version. The longer wording does not allow a dilation.',
})
REVIEWED.update((y,'regular',f'{s}{n}') for y in range(1955,1958) for s in 'AB' for n in range(1,8))
REVIEWED.update((1958,e,f'{s}{n}') for e in ['Spring','Fall'] for s in 'AB' for n in range(1,8))
CATEGORIES.update({1955:'NGXCGNXGXGNCXG',1956:'XNX XCGC XAGACNA',1957:'GXXAGXNNXXCAXG',(1958,'Spring'):'AXCAXXGGNCGNGX',(1958,'Fall'):'CXXACXNCNGXXCC'})
# Edition is part of every 1958 identity and repair key.
def prepare(y,n,text,edition='regular'):
 key=(y,edition,n)
 if key not in OVERRIDE and key not in REPLACE:key=(y,n)
 if key in OVERRIDE:return OVERRIDE[key]
 for a,b in REPLACE.get(key,[]):text=text.replace(a,b)
 text=re.sub(r'\(?\s*\\text\s*\{\s*page\s*\}\s*\d+\s*\)?','',text)
 text=re.sub(r'\(?\s*\\text\s*\{\s*\(?page\s+\d+\)?\s*\}\s*\)?','',text)
 text=re.sub(r'\\quad\s*\(\s*(?=\\\])','',text)
 return native(text)
REPLACE.update({
 (1959,'A4'):[(r'\mid x y-f(x)- \) \( g(y) \mid',r'\left|xy-f(x)-g(y)\right|')],
 (1960,'B1'):[('m(x \\neq m)','m(n \\neq m)')],
 (1960,'B3'):[('snape','shape')],
 (1961,'A7'):[('every.closed','every closed')],
 (1961,'B4'):[('i . j=1','i,j=1')],
 (1961,'B6'):[(r'=- \) \( (1+\sqrt{x})',r'=-(1+\sqrt{x})')],
 (1963,'A4'):[(r'\lim _{n \rightarrow \infty} \sup',r'\limsup _{n \rightarrow \infty}')],
 (1964,'B1'):[('a sequence of integers','a sequence of positive integers')],
})
OVERRIDE.update({
 (1960,'A3'):r'''Show that if $t_1,t_2,t_3,t_4,t_5$ are real numbers, then
$$\sum_{j=1}^{5}(1-t_j)\exp\left(\sum_{k=1}^{j}t_k\right)\leq e^{e^{e^{e}}}.$$''',
 (1960,'B2'):r'''Evaluate the double series $\displaystyle\sum_{j=0}^{\infty}\sum_{k=0}^{\infty}2^{-3k-j-(k+j)^2}$.''',
 (1960,'B7'):r'''Let $g(t)$ and $h(t)$ be real continuous functions for $t\geq0$. Show that every differentiable function $v$ satisfying
$$v'(t)+g(t)v(t)\geq h(t),\qquad v(0)=c,$$
satisfies $v(t)\geq u(t)$, where $u'(t)+g(t)u(t)=h(t)$ and $u(0)=c$.
Deduce that, for sufficiently small $t>0$, the solution of $v'(t)+g(t)v(t)=v(t)^2$, $v(0)=c_1$, may be written
$$v(t)=\max_w\left[c_1e^{-\int_0^t(g(s)-2w(s))\,ds}-\int_0^t e^{-\int_s^t(g(r)-2w(r))\,dr}w(s)^2\,ds\right],$$
where the maximum is over all continuous real-valued functions $w$ on an interval $[0,t_0]$.''',
 (1962,'B5'):r'''Prove that, for every integer $n>1$,
$$\frac{3n+1}{2n+2}<\sum_{r=1}^{n}\left(\frac rn\right)^n<2.$$''',
 (1962,'B6'):r'''Let $f(x)=\sum_{k=0}^{n}(a_k\sin kx+b_k\cos kx)$, where $n$ is a positive integer and $a_k,b_k$ are real constants. Suppose $|f(x)|\leq1$ for $0\leq x\leq2\pi$, and $|f(x)|=1$ at exactly $2n$ distinct points in $[0,2\pi)$. Show that $f(x)=\cos(nx+a)$ for some real constant $a$.''',
 (1963,'B1'):r'''For what integer $a$ does $x^2-x+a$ divide $x^{13}+x+90$?''',
 (1964,'A5'):r'''Prove that there is a constant $K$ such that, for every sequence of positive numbers $a_1,a_2,\ldots$,
$$\sum_{n=1}^{\infty}\frac{n}{a_1+\cdots+a_n}\leq K\sum_{n=1}^{\infty}\frac1{a_n}.$$''',
})
VARIANTS.update({
 (1959,'A5'):'Both predators pursue the sparrow in the longer statement. The secondary page says that the eagle pursues the hawk, contradicting its simultaneous arrival condition. The longer pursuit specification is retained.',
 (1959,'B5'):'The first line has y=2t+4 in the longer transcription and y=2t-4 in Scholes. Neither sign can be independently certified from the available transcriptions. The longer version is retained with an explicit unresolved-variant warning.',
 (1960,'A3'):'The longer transcription gives the four-level exponential tower. Scholes gives the same approximate magnitude but prints inconsistent recursive definitions of its bound; the displayed tower is retained.',
 (1960,'B2'):'The squared term (k+1)^2 in the longer transcription is restored to (k+j)^2 from the secondary double-series formula.',
 (1960,'B7'):'The inner exponent in the second integral must run from the integration variable s to t. This convolution factor is restored from the secondary h(t)-h(s) formula and checked against the integrating-factor identity.',
 (1962,'A2'):'The longer statement uses the geometric mean itself. Scholes replaces that equation with its square, which can introduce negative-average variants. The longer geometric-mean condition is retained.',
 (1962,'B6'):'The longer version only specifies 2n equality points, allowing a constant counterexample. Scholes explicitly requires exactly 2n equality points; that restriction is included in this edited version.',
 (1963,'A3'):'The longer version has an order-n differential operator and n initial conditions. Scholes uses the equivalent order-(n+1) indexing with n+1 conditions. The longer indexing is retained consistently.',
 (1964,'B1'):'Positivity of the integers, made explicit by Scholes, is restored. Arbitrary signed integers do not support the counting conclusion.',
})
NOTES.update({
 (1959,'B5'):'Unresolved source variant: the sign of the constant in the first line differs between the two available transcriptions (+4 versus -4). This published record retains +4 and is not certified against an original examination.',
 (1960,'A6'):'Source convention: throws of the six-sided die are independent and each face has probability 1/6, as made explicit by the secondary version.',
 (1961,'B2'):'Source convention: both points are chosen independently and uniformly along the segment.',
 (1962,'A2'):'Source convention: the geometric mean is the nonnegative square root and the stated averages must exist. No squared-equation variant is substituted.',
 (1962,'B3'):'Source convention: region means an open region. Scholes makes openness explicit; the boundedness assertion fails for arbitrary non-open convex sets.',
 (1962,'B6'):'Editorial correction: exactly 2n equality points are required, as specified by Scholes, to exclude constant functions. This is an edited formulation, not a claim about the exact printed examination wording.',
 (1964,'B1'):'Editorial correction: the sequence consists of positive integers, as specified by the secondary source.',
})
REVIEWED.update((y,'regular',f'{s}{n}') for y in range(1959,1965) for s in 'AB' for n in range(1,8 if y<1962 else 7))
CATEGORIES.update({1959:'AGXXGAXCXCGNNA',1960:'NGXGACNNXXXNXX',1961:'XXXXCAGXCGCXXX',1962:'GXGXCAACGCXX',1963:'GNXXGGAXXGXC',1964:'GXXNXGXCXGN G'})

REPLACE[(1958,'Fall','A5')]=[(r'. \quad(\text { page 481) }','.') ]
