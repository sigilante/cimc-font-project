% Base font parameters
numeric font_size, pen_height, x_height;
font_size  := 72pt;
pen_height := 0.21 * font_size;
warningcheck := 0;  % fig numbers use codepoint mod 32768, safe for SVG output

numeric x_radius, y_radius, Ox, Oy;
x_radius := 0.45 * font_size;
y_radius := 0.5 * font_size;
x_height := x_radius;
Ox := 0;
Oy := 0;

% Pens
pen peg_pen ;    peg_pen    = pensquare scaled pen_height;
pen thin_pen ;   thin_pen   = pencircle scaled pen_height;
pen flat_pen ;   flat_pen   = makepen ((0,0)--(pen_height,0));
pen tall_pen ;   tall_pen   = makepen ((0,0)--(0,pen_height));
pen loz_pen ;    loz_pen    = makepen (fullcircle xscaled (0.25 * pen_height) yscaled pen_height);

% Force integer RGB values instead of percentages
outputformat := "svg";
outputtemplate := "%j-%c.svg";

% Override default color output
def rgbcolor(expr r, g, b) = 
  (r, g, b)
enddef;

% Macro for drawing with rotating pen using overlapping strokes
vardef rotatingdraw(expr p, start_ang, end_ang, n, overlap) =
  save i, t_start, t_end, ang, plen;
  plen := length(p);
  for i = 0 upto n-1:
    t_start := max(0, (i - overlap)/n) * plen;
    t_end := min(plen, (i + 1 + overlap)/n) * plen;
    ang := start_ang + (end_ang - start_ang) * (i + 0.5)/n;
    pickup loz_pen rotated ang;
    draw subpath (t_start, t_end) of p;
  endfor
enddef;

% Format parameters
outputtemplate := "%j-%c.svg";
outputformat := "svg";

% Letters
input src/letters/U10400.mp; % Deseret Capital Letter Long I (𐐀)
input src/letters/U10401.mp; % Deseret Capital Letter Long E (𐐁)
input src/letters/U10402.mp; % Deseret Capital Letter Long A (𐐂)
input src/letters/U10403.mp; % Deseret Capital Letter Long Ah (𐐃)
input src/letters/U10404.mp; % Deseret Capital Letter Long O (𐐄)
input src/letters/U10405.mp; % Deseret Capital Letter Long Oo (𐐅)
input src/letters/U10406.mp; % Deseret Capital Letter Short I (𐐆)
input src/letters/U10407.mp; % Deseret Capital Letter Short E (𐐇)
input src/letters/U10408.mp; % Deseret Capital Letter Short A (𐐈)
input src/letters/U10409.mp; % Deseret Capital Letter Short Ah (𐐉)
input src/letters/U1040a.mp; % Deseret Capital Letter Short O (𐐊) 4000
input src/letters/U1040b.mp; % Deseret Capital Letter Short Oo (𐐋) 4001
input src/letters/U1040c.mp; % Deseret Capital Letter Ay (𐐌) 4002
input src/letters/U1040d.mp; % Deseret Capital Letter Ow (𐐍) 4003
input src/letters/U1040e.mp; % Deseret Capital Letter W (𐐎) 4004
input src/letters/U1040f.mp; % Deseret Capital Letter Yee (𐐏) 4005
input src/letters/U10410.mp; % Deseret Capital Letter H (𐐐)
input src/letters/U10411.mp; % Deseret Capital Letter Pe (𐐑)
input src/letters/U10412.mp; % Deseret Capital Letter Bee (𐐒)
input src/letters/U10413.mp; % Deseret Capital Letter Tee (𐐓)
input src/letters/U10414.mp; % Deseret Capital Letter Dee (𐐔)
input src/letters/U10415.mp; % Deseret Capital Letter Chee (𐐕)
input src/letters/U10416.mp; % Deseret Capital Letter Jee (𐐖)
input src/letters/U10417.mp; % Deseret Capital Letter Kay (𐐗)
input src/letters/U10418.mp; % Deseret Capital Letter Gay (𐐘)
input src/letters/U10419.mp; % Deseret Capital Letter Ef (𐐙)
input src/letters/U1041a.mp; % Deseret Capital Letter Vee (𐐚) 4006
input src/letters/U1041b.mp; % Deseret Capital Letter Eth (𐐛) 4007
input src/letters/U1041c.mp; % Deseret Capital Letter Thee (𐐜) 4008
input src/letters/U1041d.mp; % Deseret Capital Letter Es (𐐝) 4009
input src/letters/U1041e.mp; % Deseret Capital Letter Zee (𐐞) 4010
input src/letters/U1041f.mp; % Deseret Capital Letter Esh (𐐟) 4011
input src/letters/U10420.mp; % Deseret Capital Letter Zhee (𐐠)
input src/letters/U10421.mp; % Deseret Capital Letter Er (𐐡)
input src/letters/U10422.mp; % Deseret Capital Letter El (𐐢)
input src/letters/U10423.mp; % Deseret Capital Letter Em (𐐣)
input src/letters/U10424.mp; % Deseret Capital Letter En (𐐤)
input src/letters/U10425.mp; % Deseret Capital Letter Eng (𐐥)
input src/letters/U10426.mp; % Deseret Capital Letter Oi (𐐦)
input src/letters/U10427.mp; % Deseret Capital Letter Ew (𐐧)

input src/letters/Ue000.mp; % Deseret Capital Letter Variant MULE 4012
input src/letters/Ue001.mp; % Deseret Capital Letter Variant CHOICE 4013
input src/letters/Ue002.mp; % Deseret Capital Letter SQUARE 4014
input src/letters/Ue003.mp; % Deseret Capital Letter Variant Open Vee 4015
input src/letters/Ue004.mp; % Deseret Capital Letter Variant Looped Short Ah 4016
input src/letters/Ue005.mp; % Deseret Capital Letter Variant Looped Shart A 4017
input src/letters/Ue00c.mp; % Deseret Capital Letter Variant 4018

% Numerals
input src/letters/U0030.mp; % Digit Zero (0)
input src/letters/U0031.mp; % Digit One (1)
input src/letters/U0032.mp; % Digit Two (2)
input src/letters/U0033.mp; % Digit Three (3)
input src/letters/U0034.mp; % Digit Four (4)
input src/letters/U0035.mp; % Digit Five (5)
input src/letters/U0036.mp; % Digit Six (6)
input src/letters/U0037.mp; % Digit Seven (7)
input src/letters/U0038.mp; % Digit Eight (8)
input src/letters/U0039.mp; % Digit Nine (9)

% Punctuation
input src/letters/U0021.mp; % Exclamation Mark (!)
input src/letters/U0022.mp; % Quotation Mark (")
input src/letters/U0023.mp; % Number Sign (#)
input src/letters/U0024.mp; % Dollar Sign ($)
input src/letters/U0027.mp; % Apostrophe (')
input src/letters/U0028.mp; % Left Parenthesis (()
input src/letters/U0029.mp; % Right Parenthesis ())
input src/letters/U002a.mp; % Asterisk (*) 4019
input src/letters/U002b.mp; % Plus Sign (+) 4020
input src/letters/U002c.mp; % Comma (,) 4021
input src/letters/U002d.mp; % Hyphen-Minus (-) 4022
input src/letters/U002e.mp; % Full Stop (.) 4023
input src/letters/U002f.mp; % Solidus (/) 4024
input src/letters/U003a.mp; % Colon (:) 4025
input src/letters/U003b.mp; % Semicolon (;) 4026
input src/letters/U003c.mp; % Less-Than Sign (<) 4030
input src/letters/U003d.mp; % Equals Sign (=) 4027
input src/letters/U003e.mp; % Greater-Than Sign (>) 4031
input src/letters/U003f.mp; % Question Mark (?) 4028
input src/letters/U0040.mp; % Commercial At (@)
input src/letters/U005b.mp; % Left Square Bracket ([) 4032
input src/letters/U005c.mp; % Reverse Solidus (\) 4029
input src/letters/U005d.mp; % Right Square Bracket (]) 4033
input src/letters/U007c.mp; % Vertical Line (|) 4034

end
