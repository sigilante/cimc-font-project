% U+002A ASTERISK (*)
beginfig(42) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pair center;
  center := (Ox, (1/2)*y_radius);

  numeric arm;
  arm := (1/3)*y_radius;

  % Five arms radiating from center at 72-degree intervals
  save i, ang;
  for i = 0 upto 4:
    ang := 90 + i * 72;
    pickup loz_pen rotated (ang);
    draw center -- (center + arm * dir(ang));
  endfor
endfig;
