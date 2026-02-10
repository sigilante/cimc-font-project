% U+002D HYPHEN-MINUS (-)
beginfig(45) ;
  pickup loz_pen;
  path hyphen;
  hyphen := (-(1/3)*x_radius, Oy)
            -- ((1/3)*x_radius, Oy);
  draw hyphen;
endfig;
