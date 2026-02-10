% Test harness for prototypes

% Base font parameters
numeric font_size, pen_height, x_height;
font_size  := 72pt;
pen_height := 0.21 * font_size;

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

% Format parameters
outputtemplate := "%j-%c.svg";
outputformat := "svg";

% Include prototypes
input src/letters/U10408_prototype.mp;
input src/letters/U10409_prototype.mp;
input src/letters/U10426_prototype.mp;
input src/letters/Ue004_prototype.mp;
input src/letters/Ue005_prototype.mp;

end
