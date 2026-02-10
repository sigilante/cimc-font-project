% U+002B PLUS SIGN (+)
beginfig(43) ;
  pickup loz_pen;
  path hbar;
  hbar := (-(1/2)*x_radius, Oy)
          -- ((1/2)*x_radius, Oy);
  draw hbar;

  pickup loz_pen rotated 90;
  path vbar;
  vbar := (Ox, (1/2)*y_radius)
          -- (Ox, -(1/2)*y_radius);
  draw vbar;
endfig;
