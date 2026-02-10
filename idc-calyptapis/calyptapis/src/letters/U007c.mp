% U+007C VERTICAL LINE (|)
beginfig(124) ;
  pickup loz_pen rotated 90;
  path vbar;
  vbar := (Ox, y_radius)
          -- (Ox, -y_radius);
  draw vbar;
endfig;
